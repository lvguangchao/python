# -*- coding: utf-8 -*-
from eom_common.eomcore.logger import *
from eom_common.eomcore.logger import *
from .base import SwxJsonHandler
from eom_app.orm.tables import User, AdmRole, AdmMenu, AdmRoleMenu
from .helper import randomCode
from sqlalchemy import func, or_
import json, os, base64, datetime, tornado, random
from  eom_app.orm.JSONEncoder import AlchemyEncoder
from eom_common.eomcore.logger import log
from eom_app.controller.helper.uploadManager import app_upManager
from eom_app.app.configs import app_cfg
from eom_app.controller.helper.identity import app_map
from eom_app.controller.helper.permision import permision

cfg = app_cfg()
import time, zipfile

app_upManager = app_upManager()


# 用户登陆
class LoginHandler(SwxJsonHandler):
    def get(self, *args, **kwargs):
        self.render('/auth/login.mako')

    def post(self, *args, **kwargs):
        input_code = self.params('input_code')
        randomCode = self.get_session(self._s_id + '_code')
        if (str(input_code)) != str(randomCode):
            self.write_json(-2)
        else:
            user_pass = self.params('user_pass')
            user_name = self.params("user_name")
            data = self.db_adm.query(User).filter(
                User.user_name == user_name, User.user_pwd == user_pass, User.enable == 1).first()
            if data:
                user = dict()
                user['id'] = data.user_id
                user['name'] = user_name
                user['nick_name'] = user_name
                user['role_id'] = data.role_id
                user['is_login'] = True
                # 菜单id
                role_menu = app_map().get_role_menu(data.role_id)
                # 菜单 以及菜单背后的url
                menu_scource = app_map().get_menu_scource(data.role_id)
                user['role_menu'] = role_menu
                user['menu_scource'] = menu_scource
                self.set_session(self._s_id, user)
                self.write_json(0)
                self.set_cookie('user_name', user_name)
            else:
                self.write_json(-1)
            self.db_adm.close()


# 退出
class SignOutHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        if self._s_id:
            self.del_session(self._s_id)
        self.redirect('/login')


# 密码修改
class PwdUpdateHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("/auth/update_pwd.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        raw_pwd = self.get_argument("raw_pwd", None)
        pwd_first = self.get_argument("pwd_first", None)
        pwd_second = self.get_argument("pwd_second", None)
        if not raw_pwd:
            self.write_json(-1, "原始密码不能为空")
            return

        if not pwd_first or not pwd_second:
            self.write_json(-1, "新密码不能为空")
            return

        if pwd_first != pwd_second:
            self.write_json(-1, "两密码不相同")
            return
        name = self.current_user["name"]
        user = self.db_adm.query(User).filter(User.user_name == name, User.user_pwd == raw_pwd).first()
        if not user:
            self.write_json(-1, "原始密码错误")
            self.db_adm.close()
        else:
            try:
                user.user_pwd = pwd_first
                self.db_adm.commit()
                self.write_json(0, "success")  # 将上传好的路径返回
            except Exception as  e:
                self.db_adm.rollback()
                log.e(e)
                self.write_json(500, "密码修改失败")
            finally:
                self.db_adm.close()


# 请求一个task 去上传文件,返回task_gen 标示
class getTask4UploadHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        temp_gen = app_upManager.create_task()
        self.write_json(0, "success", temp_gen)


class getTaskProcessHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        task_gen = self.get_argument("task_gen", None)
        if task_gen:
            process = app_upManager.find_Process(task_gen)
            self.write_json(0, "success", process)
        else:
            self.write_json(-1, "系统错误")


# 主页
class IndexHandler(SwxJsonHandler):
    """
    #@tornado.web.authenticated
     权限注解，没有current_user 自动跳转到login_url
    """

    @tornado.web.authenticated
    def get(self):
        role_menu = self.current_user['role_menu']
        self.render("/index.mako", role_menu=role_menu)


# 没有权限页面
class notPermissHander(SwxJsonHandler):
    def get(self):
        self.render("/not_permiss.mako")


# 验证码
class RandomCode(SwxJsonHandler):
    def get(self):
        code_img, strs = randomCode.create_validate_code()
        self.set_session(self._s_id + '_code', strs)
        # stream=BytesIO()
        # code_img.save(stream,"GIF")
        prex = ''.join([str(i) for i in random.sample(range(0, 9), 4)])
        file_name = "idencode" + prex + ".png"
        # error =》 多线程下，非原子性,加一个随机数后缀
        path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "..", "data", file_name))
        code_img.save(path)
        with open(path, 'rb') as f:
            ls_f = base64.b64encode(f.read())
            self.write_raw_json(bytes.decode(ls_f))
        # 删除文件
        try:
            os.remove(path)
        except Exception as e:
            pass


class UserHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/sys_manager/user/user_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = 'SELECT u.user_id,r.role_name,u.user_name,u.logtime,u.`enable`,u.role_id FROM' \
                  '	adm_sys_user u LEFT JOIN adm_role r ON u.role_id = r.role_id'
            offset = " ORDER BY user_id DESC LIMIT {},{}".format(limit['page_index'] * limit['per_page'],
                                                                limit['per_page'])
            datas = self.db_adm.execute(sql + offset).fetchall()
            head = ['user_id', 'role_name', 'user_name', 'logtime', 'enable','role_id']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['logtime'] = temp['logtime'].isoformat()
                lst.append(temp)
            count = self.db_adm.execute("select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1)
        finally:
            self.db_adm.close()



class AdmRole4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            results = self.db_adm.query(AdmRole).all()
        except Exception as e:
            log.e(e)
            results = []
        finally:
            self.db_adm.close()
        lst = list()
        for ret in results:
            lst.append(json.loads(json.dumps(ret, cls=AlchemyEncoder)))
        self.write_raw_json(lst)


class UserEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            user_id = args.get('user_id')
            role_id = args.get('role_id')
        self.db_adm.query(User).filter(User.user_id == user_id).update({
            User.role_id: int(role_id)
        })
        try:
            self.db_adm.commit()
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(-1)
            return
        finally:
            self.db_adm.close()
        self.write_json(0)

class UserAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            user_name = args.get('user_name')
            user_pwd = args.get('user_pwd')
            role_id = args.get('role_id')
        # 校验用户名是否重复
        repeat_flag = self.db_adm.query(User).filter(User.user_name == user_name).count() > 0
        if repeat_flag:
            self.write_json(-1, '用户名重复')
            return
        # 添加
        user = User()
        user.user_name = user_name
        user.user_pwd = user_pwd
        user.enable = 1
        user.role_id = role_id
        self.db_adm.add(user)
        try:
            self.db_adm.commit()
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(-1)
            return
        finally:
            self.db_adm.close()
        self.write_json(0)


class UserDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            user_id = args.get('user_id')
        self.db_adm.query(User).filter(User.user_id == user_id).update({
            User.enable: 0
        })
        try:
            self.db_adm.commit()
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(-1)
            return
        finally:
            self.db_adm.close()
        self.write_json(0)


class AdmMenu4TreeHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            results = self.db_adm.query(AdmMenu).all()
        except Exception as e:
            log.e(e)
            results = []
        finally:
            self.db_adm.close()
        head = ['id', 'pId', 'name']
        lst = list()
        for ret in results:
            id = ret.menu_id
            pId = ret.parent_id
            name = ret.meun_name
            lst.append(dict(zip(head, (id, pId, name))))
        self.write_raw_json(lst)


class RoleEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        menu = self.get_arguments('menus')
        role_id = self.get_argument('role_id')

        # first 删除此角色 对应的 菜单信息
        self.db_adm.query(AdmRoleMenu).filter(AdmRoleMenu.role_id == role_id). \
            delete(synchronize_session=False)
        for m in menu:
            arm = AdmRoleMenu()
            arm.role_id = role_id
            arm.menu_id = m
            arm.create_time = datetime.datetime.now()
            self.db_adm.add(arm)
        try:
            self.db_adm.commit()
        except Exception as e:
            log.e(e)
            self.db_adm.rollback()
            self.write_json(-1)
            return
        finally:
            self.db_adm.close()
        self.write_json(0)


class getRoleMenuByRoleIdHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        role_id = self.get_argument('role_id')

        try:
            results = self.db_adm.query(AdmRoleMenu).filter(AdmRoleMenu.role_id == role_id).all()
        except Exception as e:
            log.e(e)
            self.db_adm.rallback()
            self.db_adm.close()
            results = []
        finally:
            self.db_adm.close()
        data = list()
        for u in results:
            data.append(json.loads(json.dumps(u, cls=AlchemyEncoder)))
        self.write_raw_json(data)
