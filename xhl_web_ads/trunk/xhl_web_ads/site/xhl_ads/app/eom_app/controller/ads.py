#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@file: ads.py
@time: 2017/11/7 13:58
"""
import datetime
import json
import math
import os
import re
import ssl
import time
import urllib.parse
from urllib import request

import tornado
import xlrd
from eom_app.app.configs import app_cfg
from eom_app.controller.export import export, exportIncome, exportPlayRecord, export_acoount_balance_select_list, \
    exportAnchor, export_task_list_update
from eom_app.controller.helper.ExcelImportManager import getplaylogDict, getplaylogAutoDict, getplaylogExport
from eom_app.controller.helper.identity import app_map
from eom_app.controller.helper.permision import permision
from eom_app.controller.helper.uploadManager import app_upManager
from eom_app.orm.JSONEncoder import AlchemyEncoder
from eom_app.orm.tables import AdsInfo, ContractPackInfo, NeedInfo, NeedGroupInfo, AdsContractInfo, \
    GroupNeedMap, AdsConfigAnchorWhitelist, AdsConfigAnchorBlacklist, \
    NeedSchedule, TLogWithdrawAnchor, BaseUser, TIdentityPersonal, TaskPlayLog, AdsNeedPlanInfo, AdsOpLog, AdsTask, \
    PlayLogAuto, \
    Adresult, PackageNeedMap, PackageInfo, BasePlatformsGuild, DashboardTask, TAccountAnchor, BaseRoom, BaseUnion, \
    AgentInfo, TLogIncomeAnchor, AdsUnionGroup, AdmRole, AdsPackageInfoSchedule, RoomInfo, AdsAgentUserMap, \
    Tlogwithdrawanchoridentityinfo
from eom_common.eomcore.logger import *
from eom_common.eomcore.logger import log
from sqlalchemy import func, or_, and_, distinct, case, desc

from .base import SwxJsonHandler

cfg = app_cfg()
from decimal import *
from tornado.concurrent import run_on_executor
import calendar

app_upManager = app_upManager()
app_playlog = getplaylogDict()
app_playlogAuto = getplaylogAutoDict()
app_playlogExport = getplaylogExport()


# ---------------广告----------------
class AdsInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        order_id = self.get_argument('order_id', None)
        self.render(
            "/ads_manager/ads_info/adsinfo_list.mako",
            order_id=order_id)

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = "SELECT ads_id,ads_name,ads_materialurl,ads_materialurl_md5," \
                  "ads_thumbnailurl,ads_contents,logtime,ads_time  from ads_info where 1=1"

            filter = args["filter"]
            name = ""
            if "search" in filter.keys():
                name = filter["search"]
            if name:
                sql = sql + " and ads_name like '%" + name.strip() + "%'"
            offset = " ORDER BY ads_id DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'ads_id',
                'ads_name',
                'ads_materialurl',
                'ads_materialurl_md5',
                'ads_thumbnailurl',
                'ads_contents',
                'logtime',
                'ads_time']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['logtime'] = temp['logtime'].isoformat()
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


class AdsinfoAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        file_metas_pic = self.request.files.get("file_pic", None)  # 获取上传图片信息
        task_gen = self.get_argument("task_gen", None)
        ads_contents = self.get_argument("ads_contents", None)
        ads_name = self.get_argument("ads_name", None)
        ads_time = self.get_argument("ads_time", None)
        order_id = self.get_argument("order_id", None)
        if not task_gen:
            self.write_json(-1, "系统错误,请重试")
            return

        adsinfo = AdsInfo()
        adsinfo.ads_contents = ads_contents
        adsinfo.ads_name = ads_name
        adsinfo.ads_time = int(ads_time) if ads_time else 0
        try:
            self.db_ads.add(adsinfo)
            self.db_ads.commit()
        except Exception as e:
            self.db_ads.rollback()
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "添加失败")
            return

        if adsinfo.ads_id is None:
            self.write_json(-1, "系统错误")
            return

        # 如果是销售下单，需要管理这个表
        if order_id:
            self.db_adm.query(AdsPackageInfoSchedule).filter(
                AdsPackageInfoSchedule.order_id == order_id).update(
                {
                    AdsPackageInfoSchedule.adsinfo_id: adsinfo.ads_id})

        upload = app_upManager.find_task(task_gen).uploadSSH
        remotePath = cfg.file_remotePath + "/" + str(adsinfo.ads_id)  # 文件夹路径
        v_data = self.db_ads.query(AdsInfo).filter(
            AdsInfo.ads_id == adsinfo.ads_id).first()
        if file_metas_pic:
            for meta in file_metas_pic:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                (fn, extension) = os.path.splitext(file_name)
                t = int(time.time())
                file_name = "{}_{}{}".format(
                    str(adsinfo.ads_id), t, extension)  # 文件名称
                yield self.upload_task(upload, meta['body'], remotePath, file_name)
                import hashlib  # 计算文件的MD5
                md5_obj = hashlib.md5()
                md5_obj.update(meta['body'])
                hash_code = md5_obj.hexdigest()
                md5 = str(hash_code).upper()
                v_data.ads_thumbnailurl = file_name
                v_data.ads_thumbnailurl_md5 = md5

        try:
            self.db_adm.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "添加失败")
        finally:
            self.db_ads.close()
            self.db_adm.close()


class AdsinfoAdd4SaleHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        file_metas_pic = self.request.files.get("file_pic", None)  # 获取上传图片信息
        file_metas = self.request.files.get("file", None)  # 获取上传图片信息

        task_gen = self.get_argument("task_gen", None)
        ads_contents = self.get_argument("ads_contents", None)
        ads_name = self.get_argument("ads_name", None)
        ads_time = self.get_argument("ads_time", None)
        order_id = self.get_argument("order_id", None)
        if not task_gen:
            self.write_json(-1, "系统错误,请重试")
            return

        adsinfo = AdsInfo()
        adsinfo.ads_contents = ads_contents
        adsinfo.ads_name = ads_name
        adsinfo.ads_time = int(ads_time) if ads_time else 0
        try:
            self.db_ads.add(adsinfo)
            self.db_ads.commit()
        except Exception as e:
            self.db_ads.rollback()
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "添加失败")
            return

        if adsinfo.ads_id is None:
            self.write_json(-1, "系统错误")
            return

        # 如果是销售下单，需要管理这个表
        if order_id:
            self.db_adm.query(AdsPackageInfoSchedule).filter(
                AdsPackageInfoSchedule.order_id == order_id).update(
                {
                    AdsPackageInfoSchedule.adsinfo_id: adsinfo.ads_id})

        upload = app_upManager.find_task(task_gen).uploadSSH
        remotePath = cfg.file_remotePath + "/" + str(adsinfo.ads_id)  # 文件夹路径
        v_data = self.db_ads.query(AdsInfo).filter(
            AdsInfo.ads_id == adsinfo.ads_id).first()
        if file_metas_pic:
            for meta in file_metas_pic:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                (fn, extension) = os.path.splitext(file_name)
                t = int(time.time())
                file_name = "{}_{}{}".format(
                    str(adsinfo.ads_id), t, extension)  # 文件名称
                yield self.upload_task(upload, meta['body'], remotePath, file_name)
                import hashlib  # 计算文件的MD5
                md5_obj = hashlib.md5()
                md5_obj.update(meta['body'])
                hash_code = md5_obj.hexdigest()
                md5 = str(hash_code).upper()
                v_data.ads_thumbnailurl = file_name
                v_data.ads_thumbnailurl_md5 = md5
        if file_metas:
            for meta in file_metas:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                (fn, extension) = os.path.splitext(file_name)
                t = int(time.time())
                file_name = "{}_{}{}".format(
                    str(v_data.ads_id), t, extension)  # 文件名称
                yield self.upload_task(upload, meta['body'], remotePath, file_name)
                import hashlib  # 计算文件的MD5
                md5_obj = hashlib.md5()
                md5_obj.update(meta['body'])
                hash_code = md5_obj.hexdigest()
                md5 = str(hash_code).upper()
                v_data.ads_materialurl = file_name
                v_data.ads_materialurl_md5 = md5

        try:
            self.db_ads.commit()
            self.db_adm.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "添加失败")
        finally:
            self.db_adm.close()
            self.db_ads.close()


class AdsinfoEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        file_metas_pic = self.request.files.get("file_pic", None)  # 获取上传图片信息
        task_gen = self.get_argument("task_gen", None)
        ads_id = self.get_argument("ads_id", None)
        ads_contents = self.get_argument("ads_contents", None)
        ads_name = self.get_argument("ads_name", None)
        ads_time = self.get_argument("ads_time", None)
        if not task_gen:
            self.write_json(-1, "系统错误,请重试")
            return

        v_data = self.db_ads.query(AdsInfo).filter(
            AdsInfo.ads_id == ads_id).first()
        v_data.ads_contents = ads_contents
        v_data.ads_name = ads_name
        v_data.ads_time = int(ads_time) if ads_time is not None else 0

        upload = app_upManager.find_task(task_gen).uploadSSH
        remotePath = cfg.file_remotePath + "/" + str(v_data.ads_id)  # 文件夹路径

        if file_metas_pic:
            for meta in file_metas_pic:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                (fn, extension) = os.path.splitext(file_name)
                t = int(time.time())
                file_name = "{}_{}{}".format(
                    str(v_data.ads_id), t, extension)  # 文件名称
                yield self.upload_task(upload, meta['body'], remotePath, file_name)
                import hashlib  # 计算文件的MD5
                md5_obj = hashlib.md5()
                md5_obj.update(meta['body'])
                hash_code = md5_obj.hexdigest()
                md5 = str(hash_code).upper()
                v_data.ads_thumbnailurl = file_name
                v_data.ads_thumbnailurl_md5 = md5

        try:
            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "修改失败")
        finally:
            self.db_ads.close()


class AdsInfoVedioAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        file_metas = self.request.files.get("file", None)  # 获取上传视频信息
        task_gen = self.get_argument("task_gen", None)
        ads_id = self.get_argument("ads_id", None)
        upload = app_upManager.find_task(task_gen).uploadSSH
        remotePath = cfg.file_remotePath + "/" + str(ads_id)  # 文件夹路径
        v_data = self.db_ads.query(AdsInfo).filter(
            AdsInfo.ads_id == int(ads_id)).first()
        if v_data is None:
            self.write_json(-1, '没有找到对应的素材数据')
            self.db_ads.close()
            return
        if file_metas:
            for meta in file_metas:  # 循环文件信息
                file_name = meta['filename']  # 获取文件的名称
                (fn, extension) = os.path.splitext(file_name)
                t = int(time.time())
                file_name = "{}_{}{}".format(str(ads_id), t, extension)  # 文件名称
                yield self.upload_task(upload, meta['body'], remotePath, file_name)
                import hashlib  # 计算文件的MD5
                md5_obj = hashlib.md5()
                md5_obj.update(meta['body'])
                hash_code = md5_obj.hexdigest()
                md5 = str(hash_code).upper()
                v_data.ads_materialurl = file_name
                v_data.ads_materialurl_md5 = md5
                try:
                    self.db_ads.commit()
                    self.write_json(0)  # 将上传好的路径返回
                except Exception as e:
                    self.db_ads.rollback()
                    self.db_ads.close()
                    log.e(e)
                    self.write_json(500, "修改失败")
                finally:
                    self.db_ads.close()
        else:
            self.write_json(-1, '请添加上传视频')
            self.db_ads.close()


class AdsInfoDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(AdsInfo).filter(
                    AdsInfo.ads_id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_adm.query(AdsPackageInfoSchedule).filter(AdsPackageInfoSchedule.adsinfo_id.in_(
                    ids)).update({AdsPackageInfoSchedule.adsinfo_id: None}, synchronize_session=False)
                self.db_adm.commit()
                self.write_json(0, 'success')
                # self.db.close()
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()
            self.db_adm.close()


# ------------需求---------------------
class NeedInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/need_info/needinfo_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = "SELECT  n.need_id,p.package_name,n.need_play_type,n.anchor_level,n.position," \
                  "n.ads_id,n.enable,n.logtime,n.description,n.need_name,ads_interval " \
                  " from ads_need_info n  LEFT JOIN ads_contract_package_info p ON " \
                  " n.package_id=p.package_id where 1=1"

            filter = args["filter"]
            name = ""
            if "search" in filter.keys():
                name = filter["search"]
            if name:
                sql = sql + " and n.need_name like '%" + name.strip() + "%' "
            offset = " ORDER BY n.need_id DESC LIMIT {},{}" .format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'need_id',
                'package_name',
                'need_play_type',
                'anchor_level',
                'position',
                'ads_id',
                'enable',
                'logtime',
                'description',
                'need_name',
                'ads_interval']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['logtime'] = temp['logtime'].isoformat()
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


class AdsInfoFindByIdHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            id = self.get_argument("id", None)
            data = self.db_ads.query(AdsInfo).filter(
                AdsInfo.ads_id == id).first()
            lst = json.loads(json.dumps(data, cls=AlchemyEncoder))
            self.write_raw_json(lst)
        except Exception as e:
            log.e(e)
            self.db_ads.close()
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


# 素材List
class AdsInfoSelect4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            ads_list = self.db_ads.query(AdsInfo).all()
            lst = list()
            for ptype in ads_list:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
        except Exception as e:
            log.e(e)
            self.db_ads.close()
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


class GroupInfoSelect4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            group_list = self.db_ads.query(NeedGroupInfo).all()
            lst = list()
            for group in group_list:
                lst.append(json.loads(json.dumps(group, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


# ContractPackInfo    List
class ContPackInfoSelect4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        ads_list = self.db_ads.query(ContractPackInfo).all()
        lst = list()
        for ptype in ads_list:
            lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
        self.write_raw_json(lst)

        self.db_ads.close()


# ---------------合同-------------------
class ContractInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/contract_info/contractinfo_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        contract_name = ''
        try:
            if "search" in filter.keys():
                contract_name = filter["search"]
            query = self.db_ads.query(AdsContractInfo)
            if contract_name:
                contract_name = '%' + contract_name + '%'
                query = query.filter(
                    AdsContractInfo.contract_name.like(contract_name))
            total = query.count()
            query = query.order_by(AdsContractInfo.contract_id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()

            lst = list()
            for item in query_result:
                lst.append({
                    'contract_id': item.contract_id or '',
                    'contract_name': item.contract_name or '',
                    'contract_price': item.contract_price or '',
                    'adsver_id': item.adsver_id or '',
                    'contract_desc': item.contract_desc or '',
                    'create_time': item.create_time.isoformat() or '',
                })
            ret = self.set_page_params(total, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "contractInfoHander查询失败")
        finally:
            self.db_ads.close()

        self.db_ads.close()


class ContractAddInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        contract_name = self.get_argument("contract_name", None)
        contract_price = self.get_argument("contract_price", None)
        adsver_id = self.get_argument("adsver_id", None)
        contract_desc = self.get_argument("contract_desc", None)

        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            contract_name = args["contract_name"]
            contract_price = args["contract_price"]
            adsver_id = args["adsver_id"]
            contract_desc = args["contract_desc"]

        try:
            date_now = datetime.datetime.now()
            item = AdsContractInfo(
                contract_name=contract_name,
                contract_price=contract_price,
                adsver_id=adsver_id,
                contract_desc=contract_desc,
                create_time=date_now)
            self.db_ads.add(item)
            self.db_ads.commit()

            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class ContractDelInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(AdsContractInfo).filter(
                    AdsContractInfo.contract_id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class ContractEdInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        contract_id = self.get_argument("contract_id", None)
        contract_name = self.get_argument("contract_name", None)
        contract_price = self.get_argument("contract_price", None)
        adsver_id = self.get_argument("adsver_id", None)
        contract_desc = self.get_argument("contract_desc", None)

        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            contract_id = args["contract_id"]
            contract_name = args["contract_name"]
            contract_price = args["contract_price"]
            adsver_id = args["adsver_id"]
            contract_desc = args["contract_desc"]

        try:
            self.db_ads.query(AdsContractInfo).filter(AdsContractInfo.contract_id == contract_id).update(
                {AdsContractInfo.contract_name: contract_name, AdsContractInfo.contract_price: contract_price,
                 AdsContractInfo.adsver_id: adsver_id, AdsContractInfo.contract_desc: contract_desc})
            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class NeedInfoFindByIdIdHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        try:
            data = self.db_ads.query(NeedInfo).filter(
                NeedInfo.need_id == id).first()
            lst = json.loads(json.dumps(data, cls=AlchemyEncoder))
            self.write_raw_json(lst)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "NeedInfoFindByIdIdHander查询失败")
        finally:
            self.db_ads.close()

        self.db_ads.close()


class NeedInfoAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        package_id = args["package_id"]
        need_play_type = args["need_play_type"]
        anchor_level = args["anchor_level"]
        position = args["position"]
        ads_id = args["ads_id"]
        description = args["description"]
        enable = args["enable"]
        need_name = args["need_name"]
        needinfo = NeedInfo()
        needinfo.package_id = package_id
        needinfo.need_play_type = need_play_type
        needinfo.anchor_level = anchor_level
        needinfo.position = position
        needinfo.ads_id = ads_id
        position_count = len(position.split(
            ",")) if position is not None else 0
        needinfo.position_count = position_count
        needinfo.description = description
        needinfo.enable = enable
        needinfo.need_name = need_name
        self.db_ads.add(needinfo)
        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class NeedInfoEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        package_id = args["package_id"]
        need_play_type = args["need_play_type"]
        anchor_level = args["anchor_level"]
        position = args["position"]
        ads_id = args["ads_id"]
        description = args["description"]
        enable = args["enable"]
        need_name = args["need_name"]
        id = args["id"]
        v_data = self.db_ads.query(NeedInfo).filter(
            NeedInfo.need_id == id).first()
        v_data.package_id = package_id
        v_data.need_play_type = need_play_type
        v_data.anchor_level = anchor_level
        v_data.position = position
        v_data.ads_id = ads_id
        v_data.description = description
        v_data.enable = enable
        v_data.need_name = need_name
        position_count = len(position.split(
            ",")) if position is not None else 0
        v_data.position_count = position_count
        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class NeedInfoDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(NeedInfo).filter(
                    NeedInfo.need_id.in_(ids)).delete(
                    synchronize_session=False)

                self.db_ads.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


# needinfo  List
class NeedInfo4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        anchor_level = self.get_argument("anchor_level", None)
        package_id = self.get_argument("package_id", None)
        query = self.db_ads.query(NeedInfo)
        if anchor_level is not None and anchor_level != "":
            query = query.filter(NeedInfo.anchor_level == anchor_level)
        if package_id is not None and package_id != "":
            query = query.filter(NeedInfo.package_id == package_id)
        ni_list = query.all()
        lst = list()
        for n in ni_list:
            lst.append(json.loads(json.dumps(n, cls=AlchemyEncoder)))
        self.write_raw_json(lst)
        self.db_ads.close()


class NeedGroupInfoHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/need_group/needgroup_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        sql = "SELECT group_name,ads_need_group_id,comment," \
              "(SELECT GROUP_CONCAT(a.ads_need_id)  as need_ids FROM ads_group_need_map a where" \
              " a.ads_group_id=b.ads_need_group_id) as need_id," \
              "logtime,anchor_level from ads_group_info b where 1=1"
        filter = args["filter"]
        name = ""
        if "search" in filter.keys():
            name = filter["search"]
        if name:
            sql = sql + " and group_name like '%" + name.strip() + "%' "
        offset = " ORDER BY ads_need_group_id DESC LIMIT {},{}" \
            .format(limit['page_index'] * limit['per_page'], limit['per_page'])
        try:
            datas = self.db_ads.execute(sql + offset).fetchall()
            lst = list()
            head = [
                'group_name',
                'ads_need_group_id',
                'comment',
                'need_id',
                'logtime',
                'anchor_level']
            for data in datas:
                temp = dict(zip(head, data))
                temp['logtime'] = temp['logtime'].isoformat()
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
        except Exception as e:
            log.e(e)
        finally:
            self.db_ads.close()
        ret = self.set_page_params(count, limit, lst)
        self.write_json(0, data=ret)


class NeedGroupInfoAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        group_name = args["group_name"]
        comment = args["comment"]
        anchor_level = args["anchor_level"]
        if group_name is not None:
            num = self.db_ads.query(NeedGroupInfo).filter(
                NeedGroupInfo.group_name == group_name).count()
            if num > 0:
                self.write_json(-1, "分组名称不能重复")
                return
        ng = NeedGroupInfo()
        ng.group_name = group_name
        ng.comment = comment
        ng.anchor_level = anchor_level
        self.db_ads.add(ng)
        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class NeedGroupInfoEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        group_name = args["group_name"]
        comment = args["comment"]
        anchor_level = args["anchor_level"]
        id = args["id"]
        v_data = self.db_ads.query(NeedGroupInfo).filter(
            NeedGroupInfo.ads_need_group_id == id).first()

        # 如果等级发生改变删除所有 映射map
        if anchor_level != v_data.anchor_level:
            self.db_ads.query(GroupNeedMap).filter(
                GroupNeedMap.ads_group_id == id).delete(
                synchronize_session=False)
        v_data.group_name = group_name
        v_data.comment = comment
        v_data.anchor_level = anchor_level

        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class NeedGroupInfoAllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        ngi_list = self.db_ads.query(NeedGroupInfo) \
            .order_by(NeedGroupInfo.ads_need_group_id.desc()).all()
        lst = list()
        for ngi in ngi_list:
            lst.append(json.loads(json.dumps(ngi, cls=AlchemyEncoder)))
        self.write_raw_json(lst)
        self.db_ads.close()


class NeedGroupInfoDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(NeedGroupInfo).filter(
                    NeedGroupInfo.ads_need_group_id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class NeedScheduleHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/need_schedule/needschedule_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):

        limit, args = self.get_pages_args()
        sql = "SELECT  s.schedule_id,g.group_name,s.count,s.anchor_if_exp," \
              "s.lv_priority,s.logtime,s.schedule_create_time,s.start_alloc_time,s.schedule_name," \
              "g.ads_need_group_id from ads_need_schedule s" \
              " LEFT JOIN ads_group_info g on s.group_id=g.ads_need_group_id where 1=1"
        filter = args["filter"]
        name = ""
        begintime = ""
        if "search" in filter.keys():
            name = filter["search"]
        if "begintime" in filter.keys():
            begintime = filter["begintime"]

        if name is not None and name != "":
            sql = sql + " and s.schedule_name like '%" + name.strip() + "%' "

        if begintime is not None and begintime != "":
            start = begintime + " 00:00:00"
            end = begintime + " 23:59:59"
            sql = sql + \
                " and s.start_alloc_time > '{}' and s.start_alloc_time < '{}' ".format(start, end)

        offset = " ORDER BY s.schedule_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        try:
            datas = self.db_ads.execute(sql + offset).fetchall()
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
            self.db_ads.close()

        lst = list()
        head = [
            'schedule_id',
            'group_name',
            'count',
            'anchor_if_exp',
            'lv_priority',
            'logtime',
            'schedule_create_time',
            'start_alloc_time',
            'schedule_name',
            'ads_need_group_id']
        for data in datas:
            temp = dict(zip(head, data))
            temp['schedule_create_time'] = temp['schedule_create_time'].isoformat(
            ) if temp['schedule_create_time'] else ''
            temp['start_alloc_time'] = temp['start_alloc_time'].isoformat(
            ) if temp['start_alloc_time'] else ''
            temp['logtime'] = temp['logtime'].isoformat(
            ) if temp['logtime'] else ''
            lst.append(temp)

        try:
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
            self.db_ads.close()

        ret = self.set_page_params(count, limit, lst)
        self.write_json(0, data=ret)
        self.db_ads.close()


class NeedScheduleHander_shchedule(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        sql = "SELECT  s.schedule_id,g.group_name,s.count,s.anchor_if_exp,s.lv_priority,s.logtime,s.schedule_create_time" \
              " from ads_need_schedule s LEFT JOIN ads_group_info g on s.group_id=g.ads_need_group_id where 1=1"
        # filter = args["filter"]
        # name = ""
        sql = sql + " and s.schedule_id = " + id + ""
        datas = self.db_ads.execute(sql).fetchone()
        if datas:
            schedule_id = datas[0]
            group_name = datas[1]
            count = datas[2]
            anchor_if_exp = datas[3]
            lv_priority = datas[4]
            logtime = datas[5].isoformat()
            schedule_create_time = datas[6].isoformat()
            lst = {
                "schedule_id": schedule_id,
                "group_name": group_name,
                "count": count,
                "anchor_if_exp": anchor_if_exp,
                "lv_priority": lv_priority,
                "logtime": logtime,
                "schedule_create_time": schedule_create_time}
            self.write_json(0, '', lst)
            self.db_ads.close()
        else:
            self.write_json(-1, '没有对应的schedule数据')
            self.db_ads.close()
            return


# 输入group_id 获取对应信息
class NeedScheduleHander_group(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        sql = "SELECT group_name,ads_need_group_id,comment,(SELECT GROUP_CONCAT(a.ads_need_id)  as need_ids FROM " \
              " ads_group_need_map a where a.ads_group_id=b.ads_need_group_id) as need_id," \
              " logtime,anchor_level from ads_group_info b where 1=1"
        sql = sql + " and b.ads_need_group_id = " + id + ""
        datas = self.db_ads.execute(sql).fetchone()

        group_name = datas[0]
        ads_need_group_id = datas[1]
        comment = datas[2]
        need_id = datas[3]
        logtime = datas[4].isoformat()
        anchor_level = datas[5]
        lst = {
            "group_name": group_name,
            "ads_need_group_id": ads_need_group_id,
            "comment": comment,
            "need_id": need_id,
            "logtime": logtime,
            "anchor_level": anchor_level}
        self.write_json(0, '', lst)
        self.db_ads.close()


class NeedScheduleAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/need_schedule/needshcdule_create.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        param = self.get_argument("param")
        if param is not None:
            param = json.loads(param)
            for p in param:
                group_name = p["group_name"]
                group_id = p["group_id"]
                count = p["count"]
                anchor_if_exp = p["anchor_if_exp"]
                lv_priority = p["lv_priority"]
                create_time = p["create_time"]
                assign_flag = p["assign_flag"]
                number = 1
                msg = ''
                flag = False
                if 'delidays' in p:
                    number = p['delidays']
                    msg = p['msg']
                    flag = True

                for i in range(1, int(number) + 1):
                    ns = NeedSchedule()
                    ns.group_id = int(group_id)
                    ns.count = int(count)
                    ns.anchor_if_exp = anchor_if_exp
                    ns.lv_priority = lv_priority
                    today = create_time[0:10] if create_time != "" else ""
                    date_time = datetime.datetime.strptime(
                        today.strip(), '%Y-%m-%d')
                    create_timeStr = datetime.datetime.strptime(
                        create_time.strip(), '%Y-%m-%d %H:%M:%S')
                    create_timeStr = create_timeStr + \
                        datetime.timedelta(days=i - 1)
                    if flag:
                        group_nameStr = group_name + str(create_timeStr.month).zfill(2) \
                            + str(create_timeStr.day).zfill(2) + str(create_timeStr.hour).zfill(2) \
                            + str(create_timeStr.minute).zfill(2) + '【新手任务{}】'.format(msg)
                    else:
                        group_nameStr = group_name

                    tomorrow = date_time + datetime.timedelta(days=i)
                    tomorrowstr = tomorrow.strftime("%Y-%m-%d")

                    today = date_time + datetime.timedelta(days=i - 1)
                    todayStr = today.strftime("%Y-%m-%d")

                    ns.schedule_create_time = create_timeStr
                    ns.schedule_destroy_time = tomorrowstr + " 05:00:00"
                    ns.start_alloc_time = create_timeStr
                    ns.start_play_time = create_timeStr
                    ns.end_play_time = create_timeStr
                    ns.end_alloc_time = todayStr + " 23:59:00"
                    ns.assign_flag = '0'
                    ns.flag = '0'
                    ns.schedule_state = '0'
                    ns.assign_flag = assign_flag
                    ns.description = group_nameStr
                    ns.schedule_name = group_nameStr
                    ns.schedule_enable = '1'
                    ns.enable = '1'
                    self.db_ads.add(ns)
                    try:
                        self.db_ads.commit()
                        oplog = AdsOpLog()
                        oplog.op_type = 5
                        user = self.get_current_user()
                        oplog.op_user_id = user["id"]
                        oplog.op_user_name = user["name"]
                        oplog.op_desc = '添加 schedule schedule_id:' + \
                            str(ns.schedule_id)
                        oc = {
                            "schedule_id": ns.schedule_id,
                            "count": count,
                            "anchor_if_exp": anchor_if_exp,
                            "create_time": create_time}
                        oplog.op_content = str(oc)
                        oplog.createtime = datetime.datetime.now()
                        self.db_adm.add(oplog)
                        self.db_adm.commit()

                    except Exception as e:
                        self.db_adm.rollback()
                        log.e(e)
                        self.write_json(500, "添加失败")
                        return
                    finally:
                        self.db_ads.close()
                        self.db_adm.close()
            self.write_json(0)
        else:
            self.write_json(-1, "没有需要添加的schedule数据")


class NeedScheduleUpdateHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument("args")
        if args is not None:
            args = json.loads(args)
            group_name = args["group_name"]
            count = args["count"]
            anchor_if_exp = args["anchor_if_exp"]
            lv_priority = args["lv_priority"]
            schedule_create_time = args["schedule_create_time"]
            id = args["id"]

            today = schedule_create_time[0:10] if schedule_create_time != "" else ""
            date_time = datetime.datetime.strptime(today.strip(), '%Y-%m-%d')
            tomorrow = date_time + datetime.timedelta(days=1)
            tomorrowstr = tomorrow.strftime("%Y-%m-%d")

            ns = self.db_ads.query(NeedSchedule).filter(
                NeedSchedule.schedule_id == id).first()
            ns.group_id = int(group_name)
            ns.count = int(count)
            ns.anchor_if_exp = anchor_if_exp
            ns.lv_priority = lv_priority
            ns.schedule_create_time = schedule_create_time
            ns.start_play_time = schedule_create_time
            ns.end_play_time = schedule_create_time
            ns.schedule_destroy_time = tomorrowstr + " 05:00:00"
            ns.start_alloc_time = schedule_create_time
            ns.end_alloc_time = today + " 23:59:00"

            try:
                self.db_ads.commit()
                self.write_json(0)
            except Exception as e:
                self.db_ads.rollback()
                log.e(e)
                self.write_json(500, "修改失败")
            finally:
                self.db_ads.close()


class NeedScheduleDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(NeedSchedule).filter(
                    NeedSchedule.schedule_id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class NeedScheduleRetractHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            schedule_id = args["schedule_id"]
        try:
            if schedule_id:
                self.db_ads.query(AdsNeedPlanInfo).filter(
                    AdsNeedPlanInfo.schedule_id == schedule_id,
                    AdsNeedPlanInfo.task_id == 0).delete(
                    synchronize_session=False)

                oplog = AdsOpLog()
                oplog.op_type = 1
                user = self.get_current_user()
                oplog.op_user_id = user["id"]
                oplog.op_user_name = user["name"]
                oplog.op_desc = '撤回 schedule schedule_id:' + str(schedule_id)
                oc = {"schedule_id": schedule_id}
                oplog.op_content = str(oc)
                oplog.createtime = datetime.datetime.now()
                self.db_adm.add(oplog)
                self.db_adm.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()
            self.db_adm.close()


class NeedScheduleIMInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        schedule_id = self.get_argument("schedule_id", None)
        sql_session = None
        session_anchor = None
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径
        try:
            # 提取表单中‘name’为‘infile’的文件元数据
            file_metas = self.request.files['infile']
            data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 根据公会名，查询公会的id
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for meta in file_metas:
                filename = data_now_str + '(' + meta['filename'] + ')'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            # 读取文件
            workbook = xlrd.open_workbook(filepath)
            os.remove(os.path.join(upload_path, filename))
            # 拿到表名
            sheets = workbook.sheet_names()

            # 第一个表
            worksheet = workbook.sheet_by_name(sheets[0])
            # 行数
            nrows = worksheet.nrows
            if nrows <= 1:
                self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
                return
            ret = list()
            for i in range(1, worksheet.nrows):
                temp = dict()
                temp['plat_id'] = int(worksheet.cell(i, 0).value)
                temp['room_id'] = int(worksheet.cell(i, 1).value)
                temp['comment'] = str(worksheet.cell(i, 3).value)
                query = self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                    and_(AdsConfigAnchorWhitelist.plat_id == temp['plat_id'],
                         AdsConfigAnchorWhitelist.room_id == temp['room_id'],
                         AdsConfigAnchorWhitelist.ads_schedule_id == schedule_id)).all()
                if query:
                    print('该次重复,room_id:' + str(temp['room_id']))
                else:
                    ret.append(temp)

            import_time = data_now_str
            for item in ret:
                item = AdsConfigAnchorWhitelist(
                    plat_id=item['plat_id'],
                    room_id=item['room_id'],
                    ads_schedule_id=schedule_id,
                    comment=item['comment'])
                self.db_ads.add(item)
                self.db_ads.commit()

            self.write_json(1, '上传成功')
            return
        # 认证公会审核通过（4.0）
        except Exception as e:
            # session.rollback()
            log.e('admin.roomImportAdsInfo_error:' + str(e))
            self.write_json(
                0, 'excel数据格式错误,请查看 url 模式 roomid 模式是否写反,error:{}'.format(e))
            return
        finally:
            self.db_ads.close()


class NeedScheduleSEWhiteAll(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        try:
            lst = []
            if id:
                query = self.db_entourage.query(AdsConfigAnchorWhitelist).filter(
                    AdsConfigAnchorWhitelist.ads_schedule_id == id).order_by(
                    AdsConfigAnchorWhitelist.id.desc())
                query_schedule = query.all()
                if query_schedule:
                    for ptype in query_schedule:
                        lst.append({
                            'id': ptype.id or '',
                            'plat_id': ptype.plat_id or 0,
                            'room_id': ptype.room_id or '',
                            'ads_schedule_id': str(ptype.ads_schedule_id) or '',
                            'comment': str(ptype.comment) or '',
                            'create_time': ptype.create_time.isoformat() or '',
                            'logtime': ptype.logtime.isoformat() or '',
                        })
                    self.write_json(0, '', lst)

                    self.db_entourage.close()
                else:
                    self.write_json(-1, '没有对应的白名单数据', lst)
                    self.db_entourage.close()
        except Exception as e:
            self.db_entourage.rollback()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            self.db_entourage.close()
        self.db_entourage.close()


# ---------------合同(对应的套餐包)-------------------
class ContractPackageInfoHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        data = self.db_ads.query(ContractPackInfo).filter(
            ContractPackInfo.contract_id == id).first()
        lst = json.loads(json.dumps(data, cls=AlchemyEncoder))
        if data:
            need_desc = json.loads(data.need_desc)
            if need_desc:
                lst['S'] = str(need_desc['S'])
                lst['A'] = str(need_desc['A'])
                lst['B'] = str(need_desc['B'])
                lst['C'] = str(need_desc['C'])
                lst['D'] = str(need_desc['D'])
            else:
                self.write_json(-1, '没有对应的套餐数据')
                self.db_ads.close()
                return
        else:
            self.write_json(-1, '没有对应的套餐数据')
            self.db_ads.close()
            return
        self.write_json(0, '', lst)
        self.db_ads.close()


# ---------------套餐---------------------------------
class ContractPackageInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render(
            "/ads_manager/contractpackage_info/contractpackage_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        packagename = ''
        try:
            if "search" in filter.keys():
                packagename = filter["search"]
            query = self.db_ads.query(ContractPackInfo)
            if packagename:
                packagename = '%' + packagename + '%'
                query = query.filter(
                    ContractPackInfo.package_name.like(packagename))
            query = query.filter(ContractPackInfo.enable == 1)
            total = query.count()
            query = query.order_by(ContractPackInfo.package_id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            lst = list()
            S = 0
            A = 0
            B = 0
            C = 0
            D = 0

            for item in query_result:
                if query_result:
                    if item.need_desc:
                        need_desc_json = json.loads(item.need_desc)
                        S = str(need_desc_json['S'])
                        A = str(need_desc_json['A'])
                        B = str(need_desc_json['B'])
                        C = str(need_desc_json['C'])
                        D = str(need_desc_json['D'])
                    else:
                        S = 0
                        A = 0
                        B = 0
                        C = 0
                        D = 0
                lst.append({
                    'package_id': item.package_id or '',
                    'affairs_num': item.affairs_num or '',
                    'package_name': item.package_name or '',
                    'contract_id': item.contract_id or '',
                    'package_price': str(item.package_price) or '',
                    'begin_time': item.begin_time.isoformat() or '',
                    'end_time': item.end_time.isoformat() or '',
                    'anchor_need': item.anchor_need or '',
                    'anchor_play_count': item.anchor_play_count or '',
                    'need_desc': item.need_desc or '',
                    'status': item.status or '',
                    'S': S,
                    'A': A,
                    'B': B,
                    'C': C,
                    'D': D,
                })
            ret = self.set_page_params(total, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "ContractPackageInfoHanderAll查询失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class ContractAddPackageInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        package_name = self.get_argument("package_name", None)
        contract_id = self.get_argument("contract_id", None)
        package_price = self.get_argument("package_price", None)
        begin_time = self.get_argument("begin_time", None)
        end_time = self.get_argument("end_time", None)
        anchor_need = self.get_argument("anchor_need", None)
        anchor_play_count = self.get_argument("anchor_play_count", None)
        affairs_num = self.get_argument("affairs_num", None)
        S = self.get_argument("S", None)
        A = self.get_argument("A", None)
        B = self.get_argument("B", None)
        C = self.get_argument("C", None)
        D = self.get_argument("D", None)
        need_desc = {}
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            package_name = args["package_name"]
            contract_id = args["contract_id"]
            package_price = args["package_price"]
            begin_time = args["begin_time"]
            end_time = args["end_time"]
            anchor_need = args["anchor_need"]
            anchor_play_count = args["anchor_play_count"]
            affairs_num = args["affairs_num"]
            S = args["S"]
            A = args["A"]
            B = args["B"]
            C = args["C"]
            D = args["D"]
            need_desc = {
                "S": S,
                "A": A,
                "B": B,
                "C": C,
                "D": D
            }
            need_desc = json.dumps(need_desc)

        try:
            date_now = datetime.datetime.now()
            item = ContractPackInfo(
                package_name=package_name,
                contract_id=contract_id,
                package_price=package_price,
                begin_time=begin_time,
                end_time=end_time,
                anchor_need=anchor_need,
                status=1,
                affairs_num=affairs_num,
                anchor_play_count=anchor_play_count,
                need_desc=need_desc,
                create_time=date_now,
                enable=1,
                rate=100)
            self.db_ads.add(item)
            self.db_ads.commit()

            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "新增失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class ContractDelPackageInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(ContractPackInfo).filter(ContractPackInfo.package_id.in_(
                    ids)).update({ContractPackInfo.enable: 0}, synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class ContractEdPackageInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            package_id = args["package_id"]
            package_name = args["package_name"]
            contract_id = args["contract_id"]
            package_price = args["package_price"]
            begin_time = args["begin_time"]
            end_time = args["end_time"]
            anchor_need = args["anchor_need"]
            anchor_play_count = args["anchor_play_count"]
            affairs_num = args["affairs_num"]
            S = args["S"]
            A = args["A"]
            B = args["B"]
            C = args["C"]
            D = args["D"]
            need_desc = {
                "S": S,
                "A": A,
                "B": B,
                "C": C,
                "D": D
            }
            need_desc = json.dumps(need_desc)

        try:
            self.db_ads.query(ContractPackInfo).filter(
                ContractPackInfo.package_id == package_id).update(
                {
                    ContractPackInfo.package_name: package_name,
                    ContractPackInfo.contract_id: contract_id,
                    ContractPackInfo.end_time: end_time,
                    ContractPackInfo.anchor_need: anchor_need,
                    ContractPackInfo.anchor_play_count: anchor_play_count,
                    ContractPackInfo.need_desc: need_desc,
                    ContractPackInfo.affairs_num: affairs_num,
                    ContractPackInfo.package_price: package_price,
                    ContractPackInfo.begin_time: begin_time})
            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class ContractEdAffairsInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            package_id = args["package_id"]
            affairs_num = args["affairs_num"]
        try:
            self.db_ads.query(ContractPackInfo).filter(ContractPackInfo.package_id == package_id).update(
                {ContractPackInfo.affairs_num: affairs_num})
            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class GroupNeedMapUpdateHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            need_id = args["need_id"]
            group_id = args["group_id"]
            ifselect = args["ifselect"]
            type = args["type"]
            old_need_id = args["old_need_id"]

        if ifselect == False and need_id != "":
            # 删除
            self.db_ads.query(GroupNeedMap).filter(
                GroupNeedMap.ads_group_id == group_id,
                GroupNeedMap.ads_need_id == need_id).delete(
                synchronize_session=False)

        elif ifselect and old_need_id != "":

            num = self.db_ads.query(GroupNeedMap).filter(
                GroupNeedMap.ads_need_id == need_id,
                GroupNeedMap.ads_group_id == group_id).count()
            if num > 0:
                self.write_json(-1, "该分组已包含need_id")
                return

            v_data = self.db_ads.query(GroupNeedMap).filter(
                GroupNeedMap.ads_need_id == old_need_id,
                GroupNeedMap.ads_group_id == group_id).first()
            if v_data is not None and type == "update":
                # 修改
                v_data.ads_need_id = need_id

        elif ifselect and type == "insert" and need_id != "":
            num = self.db_ads.query(GroupNeedMap).filter(
                GroupNeedMap.ads_need_id == need_id,
                GroupNeedMap.ads_group_id == group_id).count()
            if num > 0:
                self.write_json(-1, "该分组已包含need_id")
                return

            gnm = GroupNeedMap()
            gnm.ads_group_id = group_id
            gnm.ads_need_id = need_id
            gnm.create_time = datetime.datetime.now()
            self.db_ads.add(gnm)

        try:
            self.db_ads.commit()
            self.write_json(0, 'success')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class GroupNeedMapSelectByIdHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        groupid = self.get_argument("groupid", None)
        self.db_ads.query(GroupNeedMap).filter()
        sql = "SELECT i.anchor_level, i.need_id, i.ads_id from ads_group_need_map m " \
              " LEFT JOIN  ads_need_info  i  on i.need_id = m.ads_need_id where 1=1"
        if groupid is not None and groupid != "":
            sql = sql + " and m.ads_group_id = " + groupid + ""
        result = self.db_ads.execute(sql).fetchall()
        lst = list()
        for g in result:
            anchor_level = g[0]
            need_id = g[1]
            ads_id = g[2]
            lst.append({"anchor_level": anchor_level,
                        "need_id": need_id, "ads_id": ads_id})
        self.write_raw_json(lst)
        self.db_ads.close()


class NeedInfoSelectById(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        if id is not None and id != "":
            sql = "SELECT p.package_name,n.need_play_type,n. ENABLE,n.description," \
                  "n.need_name FROM	ads_need_info n LEFT JOIN ads_contract_package_info p " \
                  "ON n.package_id = p.package_id	where n.need_id=" + id

            result = self.db_ads.execute(sql).fetchall()
            lst = list()
            for g in result:
                package_name = g[0]
                need_play_type = g[1]
                enable = g[2]
                description = g[3]
                need_name = g[4]
                lst.append({"package_name": package_name,
                            "need_play_type": need_play_type,
                            "enable": enable,
                            "description": description,
                            "need_name": need_name})
            self.write_raw_json(lst)
            self.db_ads.close()


# ---------------白名单---------------------------------
class WhitelistInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/whitelist_info/whitelist_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        id = ''
        if "search" in filter.keys():
            id = filter["search"]
        try:
            query = self.db_ads.query(AdsConfigAnchorWhitelist)
            if id:
                query = query.filter(AdsConfigAnchorWhitelist.room_id == id)
            total = query.count()
            query = query.order_by(AdsConfigAnchorWhitelist.id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            # total = query.count()
            lst = list()
            for item in query_result:
                # shch_id = ''
                # if item.ads_schedule_id_list:
                #     shch_id = str(item.ads_schedule_id_list).split(',')
                lst.append({
                    'id': item.id or 0,
                    'plat_id': item.plat_id or 0,
                    'room_id': item.room_id or '',
                    'ads_schedule_id_list': item.ads_schedule_id or '',
                    # 'need_id_list': item.need_id_list or '',
                    'comment': item.comment or '',
                    'create_time': item.create_time.isoformat() or '',
                    'logtime': item.logtime.isoformat() or '',
                })
            ret = self.set_page_params(total, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "WhitelistInfoHanderAll查询失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class WhitelistAddInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        # id = self.get_argument("id", None)
        plat_id = self.get_argument("plat_id", None)
        room_id = self.get_argument("room_id", None)
        ads_schedule_id_list = self.get_argument("ads_schedule_id_list", None)
        comment = self.get_argument("comment", None)

        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            # id = args["id"]
            plat_id = args["plat_id"]
            room_id = args["room_id"]
            ads_schedule_id_list = args["ads_schedule_id_list"]
            comment = args["comment"]
        try:
            date_now = datetime.datetime.now()
            query_count = self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                and_(
                    AdsConfigAnchorWhitelist.plat_id == plat_id,
                    AdsConfigAnchorWhitelist.room_id == room_id,
                    AdsConfigAnchorWhitelist.ads_schedule_id == ads_schedule_id_list)).count()
            if query_count > 0:
                self.write_json(500, '白名单已有此人')
            else:
                item = AdsConfigAnchorWhitelist(
                    plat_id=plat_id,
                    room_id=room_id,
                    ads_schedule_id=ads_schedule_id_list,
                    comment=comment,
                    logtime=date_now,
                    create_time=date_now)
                self.db_ads.add(item)
                self.db_ads.commit()
                self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class WhitelistDelInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        ids = self.get_argument("ids", None)
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                    AdsConfigAnchorWhitelist.id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
                # self.db.close()
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class WhitelistEdInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        # id = self.get_argument("id", None)
        plat_id = self.get_argument("plat_id", None)
        room_id = self.get_argument("room_id", None)
        ads_schedule_id_list = self.get_argument("ads_schedule_id_list", None)
        comment = self.get_argument("comment", None)
        shchedule_id_old = self.get_argument("shchedule_id_old", None)
        plat_id_old = self.get_argument("plat_id_old", None)
        room_id_old = self.get_argument("room_id_old", None)

        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            # id = args["id"]
            plat_id = args["plat_id"]
            room_id = args["room_id"]
            ads_schedule_id_list = args["ads_schedule_id_list"]
            comment = args["comment"]
            shchedule_id_old = args["shchedule_id_old"]
            plat_id_old = args["plat_id_old"]
            room_id_old = args["room_id_old"]

        try:
            date_now = datetime.datetime.now()
            self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                and_(
                    AdsConfigAnchorWhitelist.plat_id == plat_id_old,
                    AdsConfigAnchorWhitelist.room_id == room_id_old,
                    AdsConfigAnchorWhitelist.ads_schedule_id == shchedule_id_old)).update(
                {
                    AdsConfigAnchorWhitelist.plat_id: plat_id,
                    AdsConfigAnchorWhitelist.room_id: room_id,
                    AdsConfigAnchorWhitelist.ads_schedule_id: str(ads_schedule_id_list),
                    AdsConfigAnchorWhitelist.comment: comment,
                    AdsConfigAnchorWhitelist.logtime: date_now})

            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class WhitelistIMInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        sql_session = None
        session_anchor = None
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径

        # aa=os.path.dirname(os.getcwd())
        try:

            # 提取表单中‘name’为‘infile’的文件元数据
            file_metas = self.request.files['infile']
            data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 根据公会名，查询公会的id
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for meta in file_metas:
                filename = data_now_str + '(' + meta['filename'] + ')'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            # 读取文件
            workbook = xlrd.open_workbook(filepath)
            os.remove(os.path.join(upload_path, filename))
            # 拿到表名
            sheets = workbook.sheet_names()

            # 第一个表
            worksheet = workbook.sheet_by_name(sheets[0])
            # 行数
            nrows = worksheet.nrows
            if nrows <= 1:
                self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
                return
            ret = list()

            for i in range(1, worksheet.nrows):
                temp = dict()
                temp['plat_id'] = int(worksheet.cell(i, 0).value)
                temp['room_id'] = int(worksheet.cell(i, 1).value)
                temp['ads_schedule_id'] = int(worksheet.cell(i, 2).value)
                temp['comment'] = str(worksheet.cell(i, 3).value)
                # date = xldate_as_tuple(worksheet.cell(i, 4).value, 0)
                # temp['create_time'] = datetime.datetime(*date)
                query = self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                    and_(AdsConfigAnchorWhitelist.plat_id == temp['plat_id'],
                         AdsConfigAnchorWhitelist.room_id == temp['room_id'],
                         AdsConfigAnchorWhitelist.ads_schedule_id == temp['ads_schedule_id'])).all()
                if query:
                    print('该次重复,room_id:' + str(temp['room_id']))
                else:
                    ret.append(temp)

            import_time = data_now_str
            for item in ret:
                query_count = self.db_ads.query(AdsConfigAnchorWhitelist).filter(
                    and_(AdsConfigAnchorWhitelist.plat_id == item['plat_id'],
                         AdsConfigAnchorWhitelist.room_id == item['room_id'],
                         AdsConfigAnchorWhitelist.ads_schedule_id == item['ads_schedule_id'])).count()

                if query_count == 0:
                    item = AdsConfigAnchorWhitelist(
                        plat_id=item['plat_id'],
                        room_id=item['room_id'],
                        ads_schedule_id=item['ads_schedule_id'],
                        comment=item['comment'])
                    self.db_ads.add(item)
                    self.db_ads.commit()

            self.write_json(1, '上传成功')
            return
        # 认证公会审核通过（4.0）
        except Exception as e:
            # session.rollback()
            log.e('admin.roomImportAdsInfo_error:' + str(e))
            self.write_json(0, 'excel数据格式错误,error:{}'.format(e))
            return
        finally:
            self.db_ads.close()


class Seleteshchedule(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        # group_id = self.get_argument("group_id", None)
        try:
            lst = []
            ads_list = ''

            if id == '1':
                ads_list = self.db_ads.query(NeedSchedule).filter(
                    NeedSchedule.assign_flag == '0').all()
            elif id == '0':
                ads_list = self.db_ads.query(NeedSchedule).filter(
                    NeedSchedule.enable == 1).all()
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
            for ptype in ads_list:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class Seleteshchedulegroup(SwxJsonHandler):
    def get(self, *args, **kwargs):
        level = self.get_argument("level", None)
        try:
            lst = []
            ads_list = ''
            if level:
                ads_list = self.db_ads.query(NeedGroupInfo).filter(
                    NeedGroupInfo.anchor_level == level).all()
            else:
                ads_list = self.db_ads.query(NeedGroupInfo).all()
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
            for ptype in ads_list:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


# ---------------黑名单---------------------------------
class BlacklistInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/blacklist_info/blacklist_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        id = ''
        if "search" in filter.keys():
            id = filter["search"]
        try:
            query = self.db_ads.query(AdsConfigAnchorBlacklist)
            if id:
                query = query.filter(AdsConfigAnchorBlacklist.room_id == id)
            total = query.count()
            query = query.order_by(AdsConfigAnchorBlacklist.id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            # total = query.count()
            lst = list()
            for item in query_result:
                # shch_id = ''
                # if item.ads_schedule_id:
                #     shch_id = str(item.ads_schedule_id).split(',')
                lst.append({
                    'id': item.id or 0,
                    'plat_id': item.plat_id or 0,
                    'room_id': item.room_id or '',
                    'ads_schedule_id': str(item.ads_schedule_id) or '',
                    'comment': item.comment or '',
                    'create_time': item.create_time.isoformat() or '',
                    'logtime': item.logtime.isoformat() or '',
                })
            ret = self.set_page_params(total, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "BlacklistInfoHanderAll查询失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class BlacklistAddInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        # id = self.get_argument("id", None)
        plat_id = self.get_argument("plat_id", None)
        room_id = self.get_argument("room_id", None)
        ads_schedule_id_list = self.get_argument("ads_schedule_id", None)
        comment = self.get_argument("comment", None)

        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            # id = args["id"]
            plat_id = args["plat_id"]
            room_id = args["room_id"]
            ads_schedule_id_list = args["ads_schedule_id"]
            comment = args["comment"]

        try:
            # date_now = datetime.datetime.now()
            query_count = self.db_ads.query(AdsConfigAnchorBlacklist).filter(
                and_(
                    AdsConfigAnchorBlacklist.plat_id == plat_id,
                    AdsConfigAnchorBlacklist.room_id == room_id,
                    AdsConfigAnchorBlacklist.ads_schedule_id == ads_schedule_id_list)).count()
            if query_count > 0:
                self.write_json(500, '黑名单已有此人')
            else:
                item = AdsConfigAnchorBlacklist(
                    plat_id=plat_id,
                    room_id=room_id,
                    ads_schedule_id=ads_schedule_id_list,
                    comment=str(comment))
                self.db_ads.add(item)
                self.db_ads.commit()

                self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class BlacklistDelInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
        try:
            if ids:
                self.db_ads.query(AdsConfigAnchorBlacklist).filter(
                    AdsConfigAnchorBlacklist.id.in_(ids)).delete(
                    synchronize_session=False)
                self.db_ads.commit()
                self.write_json(0, 'success')
                # self.db.close()
            else:
                self.write_json(-1, '没有选中删除项')
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "删除失败")
        finally:
            self.db_ads.close()


class BlicklistEdInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        id = self.get_argument("id", None)
        plat_id = self.get_argument("plat_id", None)
        room_id = self.get_argument("room_id", None)
        ads_schedule_id_list = self.get_argument("ads_schedule_id", None)
        comment = self.get_argument("comment", None)
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)

            id = args["id"]
            plat_id = args["plat_id"]
            room_id = args["room_id"]
            ads_schedule_id_list = args["ads_schedule_id"]
            comment = args["comment"]

        try:
            date_now = datetime.datetime.now()
            self.db_ads.query(AdsConfigAnchorBlacklist).filter(AdsConfigAnchorBlacklist.id == id).update(
                {AdsConfigAnchorBlacklist.plat_id: plat_id, AdsConfigAnchorBlacklist.room_id: room_id,
                 AdsConfigAnchorBlacklist.ads_schedule_id: str(ads_schedule_id_list),
                 AdsConfigAnchorBlacklist.comment: str(comment),
                 AdsConfigAnchorBlacklist.logtime: date_now})
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})

            self.db_ads.commit()
            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class BlacklistIMInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        sql_session = None
        session_anchor = None
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径

        # aa=os.path.dirname(os.getcwd())
        try:
            # 提取表单中‘name’为‘infile’的文件元数据
            file_metas = self.request.files['infile']
            data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 根据公会名，查询公会的id
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for meta in file_metas:
                filename = data_now_str + '(' + meta['filename'] + ')'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            # 读取文件
            workbook = xlrd.open_workbook(filepath)
            os.remove(os.path.join(upload_path, filename))
            # 拿到表名
            sheets = workbook.sheet_names()

            # 第一个表
            worksheet = workbook.sheet_by_name(sheets[0])
            # 行数
            nrows = worksheet.nrows
            if nrows <= 1:
                self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
                return
            ret = list()

            for i in range(1, worksheet.nrows):
                temp = dict()
                temp['plat_id'] = int(worksheet.cell(i, 0).value)
                temp['room_id'] = int(worksheet.cell(i, 1).value)
                temp['ads_schedule_id'] = int(worksheet.cell(i, 2).value)
                temp['comment'] = str(worksheet.cell(i, 3).value)
                # date = xldate_as_tuple(worksheet.cell(i, 4).value, 0)
                # temp['create_time'] = datetime.datetime(*date)
                query = self.db_ads.query(AdsConfigAnchorBlacklist).filter(
                    and_(AdsConfigAnchorBlacklist.plat_id == temp['plat_id'],
                         AdsConfigAnchorBlacklist.room_id == temp['room_id'],
                         AdsConfigAnchorBlacklist.ads_schedule_id == temp['ads_schedule_id'])).all()
                if query:
                    print('该次重复,room_id:' + str(temp['room_id']))
                else:
                    ret.append(temp)

            import_time = data_now_str
            for item in ret:
                query_count = self.db_ads.query(AdsConfigAnchorBlacklist).filter(
                    and_(AdsConfigAnchorBlacklist.plat_id == item['plat_id'],
                         AdsConfigAnchorBlacklist.room_id == item['room_id'],
                         AdsConfigAnchorBlacklist.ads_schedule_id == item['ads_schedule_id'])).count()

                if query_count == 0:
                    item = AdsConfigAnchorBlacklist(
                        plat_id=item['plat_id'],
                        room_id=item['room_id'],
                        ads_schedule_id=item['ads_schedule_id'],
                        comment=item['comment'])
                    self.db_ads.add(item)
                    self.db_ads.commit()

            self.write_json(1, '上传成功')
            return
        # 认证公会审核通过（4.0）
        except Exception as e:
            # session.rollback()
            log.e('black.BlacklistIMInfoHanderAll:' + str(e))
            self.write_json(
                0, 'excel数据格式错误,请查看 url 模式 roomid 模式是否写反,error:{}'.format(e))
            return
        finally:
            self.db_ads.close()


# ---------------用户提现---------------------------------
class WithdrawanchorInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/withdrawanchor_info/withdrawanchor_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]
        id = ''
        phone = ''
        income_from = ''
        user_id = ''
        start_time = ''
        start_time2 = ''
        end_time = ''
        end_time2 = ''
        bank_name = ''
        bank_name_list = []
        if "id" in filter.keys():
            id = filter["id"]
            phone = filter["phone"]
            income_from = filter["income_from"]
            user_id = filter["user_id"]
            start_time = filter["start_time"]
            end_time = filter["end_time"]
            bank_name = filter["bank_name"]
            start_time2 = filter["start_time2"]
            end_time2 = filter["end_time2"]
        try:
            query = self.db_wealth.query(
                TLogWithdrawAnchor,
                Tlogwithdrawanchoridentityinfo).join(
                Tlogwithdrawanchoridentityinfo,
                TLogWithdrawAnchor.id == Tlogwithdrawanchoridentityinfo.withdraw_cash_id)
            # query_guild = self.db_guild.query(BaseUser)
            # query_bank_name = self.db_wealth.query(TIdentityPersonal)
            # query_adsunion_group = self.db_ads.query(AdsUnionGroup
            #                                          ).filter(AdsUnionGroup.apply_status != 50)

            data_now = datetime.datetime.now().strftime('%Y-%m-%d')
            if id:
                query = query.filter(TLogWithdrawAnchor.id == id)
            if phone:
                # query_guild = query_guild.filter(BaseUser.u_mobile_number == phone).first()
                # user_id_v2 = query_guild.user_id
                query = query.filter(
                    Tlogwithdrawanchoridentityinfo.u_mobile_number == phone)
            if bank_name:
                # query_bank_name = query_bank_name.filter(TIdentityPersonal.bank_name == bank_name).all()
                # for item in query_bank_name:
                #     bank_name_list.append(item.user_id)
                query = query.filter(
                    Tlogwithdrawanchoridentityinfo.bank_name == bank_name)
            if income_from:
                query = query.filter(
                    TLogWithdrawAnchor.apply_state == income_from)

            if user_id:
                query = query.filter(TLogWithdrawAnchor.user_id == user_id)
            if start_time and end_time == '' and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= data_now,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= start_time))
            if end_time and start_time == '' and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= data_now))
            if start_time and end_time and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= start_time))
            if start_time2 and end_time2 == '' and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= data_now,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= start_time2))
            if end_time2 and start_time2 == '' and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= end_time2,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= data_now))
            if start_time2 and end_time2 and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= end_time2,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= start_time2))
            total = query.count()
            query = query.order_by(TLogWithdrawAnchor.id.desc()).limit(
                int(limit['per_page'])).offset((int(limit['page_index'] * limit['per_page'])))

            query_result = query.all()

            lst = list()
            for item in query_result:
                lst.append({
                    'id': item[0].id or 0,
                    'user_id': item[0].user_id or 0,
                    'money': str(item[0].money) or '',
                    'remark': str(item[0].remark) or '',
                    'sevice_money': str(item[0].sevice_money) or '',
                    'money_balance': str(item[0].money_balance) or '',
                    'sevice_money_balance': str(item[0].sevice_money_balance) or '',
                    'money_rp': str(item[0].money_rp) or '',
                    'sevice_money_rp': str(item[0].sevice_money_rp) or '',
                    'apply_state': item[0].apply_state or '',
                    'create_time': item[0].create_time.isoformat() or '',
                    'logtime': item[0].logtime.isoformat() or '',
                    'id_user_name': str(item[1].id_user_name) or '',
                    'id_number': str(item[1].id_number) or '',
                    'id_img_front': str(item[1].id_img_front) or '',
                    'id_img_back': str(item[1].id_img_back) or '',
                    'bank_name': str(item[1].bank_name) or '',
                    'bank_card_number': str(item[1].bank_card_number) or '',
                    'hold_user_name': str(item[1].hold_user_name) or '',
                    'bank_sub_name': str(item[1].bank_sub_name) or '',
                    'qq_number': str(item[1].qq_number) or '',
                    'identity_id': str(item[1].id) or '',
                    'u_mobile_number': str(item[1].u_mobile_number) or '',
                })
            ret = dict()
            # withdraw_list = app_map().TLogWithdrawAnchor()
            # guild_list = app_map().Baseuser()
            adsuniongroup = app_map().Adsuniongroup()
            # union_list = app_map().Baseunion()
            ret['page_index'] = limit['page_index']
            ret['total'] = total
            ret['data'] = lst

            for info_data in ret['data']:
                # for info_p in withdraw_list:
                # if info_data['user_id'] in withdraw_list:
                #     info_data['id_user_name'] = withdraw_list[info_data['user_id']]['id_user_name']
                #     info_data['id_number'] = withdraw_list[info_data['user_id']]['id_number']
                #     info_data['id_img_front'] = withdraw_list[info_data['user_id']]['id_img_front']
                #     info_data['id_img_back'] = withdraw_list[info_data['user_id']]['id_img_back']
                #     info_data['bank_name'] = withdraw_list[info_data['user_id']]['bank_name']
                #     info_data['bank_card_number'] = withdraw_list[info_data['user_id']]['bank_card_number']
                #     info_data['hold_user_name'] = withdraw_list[info_data['user_id']]['hold_user_name']
                #     info_data['bank_sub_name'] = withdraw_list[info_data['user_id']]['bank_sub_name']
                #     info_data['qq_number'] = withdraw_list[info_data['user_id']]['qq_number']
                # else:
                #     anchor_list_bank = query_bank_name.filter(TIdentityPersonal.user_id == info_data['user_id']).first()
                #
                #     if anchor_list_bank:
                #         info_data['id_user_name'] = anchor_list_bank.id_user_name
                #         info_data['id_number'] = anchor_list_bank.id_number
                #         info_data['id_img_front'] = anchor_list_bank.id_img_front
                #         info_data['id_img_back'] = anchor_list_bank.id_img_back
                #         info_data['bank_name'] = anchor_list_bank.bank_name
                #         info_data['bank_card_number'] = anchor_list_bank.bank_card_number
                #         info_data['hold_user_name'] = anchor_list_bank.hold_user_name
                #         info_data['bank_sub_name'] = anchor_list_bank.bank_sub_name
                #         info_data['qq_number'] = anchor_list_bank.qq_number
                # if info_data['user_id'] in guild_list:
                #     info_data['u_mobile_number'] = guild_list[info_data['user_id']]['u_mobile_number']
                # else:
                #     anchor_list_phone = query_guild.filter(BaseUser.user_id == info_data['user_id']).first()
                #     if anchor_list_phone:
                #         info_data['u_mobile_number'] = anchor_list_phone.u_mobile_number

                if str(info_data['user_id']) in adsuniongroup:
                    ads_union_id_data = adsuniongroup[str(
                        info_data['user_id'])]['union_id']
                    ads_room_url_data = adsuniongroup[str(
                        info_data['user_id'])]['source_link']
                    # union_name_data = union_list[ads_union_id_data]['union_name']
                    info_data['room_url'] = ads_room_url_data
                    info_data['union_name'] = ads_union_id_data
                else:
                    info_data['room_url'] = '-'
                    info_data['union_name'] = '-'

                withdraw_yes_no = self.db_wealth.query(TLogWithdrawAnchor).filter(
                    and_(TLogWithdrawAnchor.user_id == info_data['user_id'],
                         TLogWithdrawAnchor.apply_state == 40)).all()
                if withdraw_yes_no:
                    info_data['withdraw_yes_no'] = '是'
                else:
                    info_data['withdraw_yes_no'] = '否'

                if info_data['apply_state'] == 10:
                    info_data['apply_name'] = '未处理'
                elif info_data['apply_state'] == 15:
                    info_data['apply_name'] = '已审核'
                elif info_data['apply_state'] == 11:
                    info_data['apply_name'] = '审核未通过'
                elif info_data['apply_state'] == 20:
                    info_data['apply_name'] = '已提交财务'
                elif info_data['apply_state'] == 30:
                    info_data['apply_name'] = '打款异常'
                elif info_data['apply_state'] == 35:
                    info_data['apply_name'] = '打款异常已处理'
                elif info_data['apply_state'] == 40:
                    info_data['apply_name'] = '已完成'

                # if 'u_mobile_number' not in info_data:
                #     info_data['u_mobile_number'] = '-'
                # if 'id_user_name' not in info_data:
                #     info_data['id_user_name'] = '-'
                #     info_data['id_number'] = '-'
                #     info_data['id_img_front'] = '-'
                #     info_data['id_img_back'] = '-'
                #     info_data['bank_name'] = '-'
                #     info_data['bank_card_number'] = '-'
                #     info_data['hold_user_name'] = '-'
                #     info_data['bank_sub_name'] = '-'
                #     info_data['qq_number'] = '-'
                if 'union_name' not in info_data:
                    info_data['room_url'] = '-'
                    info_data['union_name'] = '-'
            # for item in app_map().TLogWithdrawAnchor():
            self.write_json(0, data=ret)
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()
        except Exception as e:
            # session.rollback()
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()
            log.e('WithdrawanchorInfoHanderAll:' + str(e))
            self.write_json(500, '提现查询失败')
            return
        finally:
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()


class WithdrawanchorUpInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self):
        # limit = self.get_pages_args()
        id = self.get_argument("id", None)
        phone = self.get_argument("phone", None)
        income_from = self.get_argument("income_from", None)
        user_id = self.get_argument("user_id", None)
        bank_name = self.get_argument("bank_name", None)
        start_time = self.get_argument("start_time", None)
        end_time = self.get_argument("end_time", None)
        start_time2 = self.get_argument("start_time2", None)
        end_time2 = self.get_argument("end_time2", None)
        # bank_name_list = []
        query = self.db_wealth.query(
            TLogWithdrawAnchor,
            Tlogwithdrawanchoridentityinfo).join(
            Tlogwithdrawanchoridentityinfo,
            TLogWithdrawAnchor.id == Tlogwithdrawanchoridentityinfo.withdraw_cash_id)
        # query_guild = self.db_guild.query(BaseUser)
        # query_bank_name = self.db_wealth.query(TIdentityPersonal)
        # query_adsunion_group = self.db_ads.query(AdsUnionGroup
        #                                          ).filter(AdsUnionGroup.apply_status != 50)

        data_now = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            if id:
                query = query.filter(TLogWithdrawAnchor.id == id)
            if phone:
                # query_guild = query_guild.filter(BaseUser.u_mobile_number == phone).first()
                # user_id_v2 = query_guild.user_id
                query = query.filter(
                    Tlogwithdrawanchoridentityinfo.u_mobile_number == phone)
            if bank_name:
                # query_bank_name = query_bank_name.filter(TIdentityPersonal.bank_name == bank_name).all()
                # for item in query_bank_name:
                #     bank_name_list.append(item.user_id)
                query = query.filter(
                    Tlogwithdrawanchoridentityinfo.bank_name == bank_name)
            if income_from:
                query = query.filter(
                    TLogWithdrawAnchor.apply_state == income_from)
            if user_id:
                query = query.filter(TLogWithdrawAnchor.user_id == user_id)
            # if bank_name:
            #     query_bank_name = query_bank_name.filter(TIdentityPersonal.bank_name == bank_name).all()
            #     for item in query_bank_name:
            #         bank_name_list.append(item.user_id)
            #     query = query.filter(TLogWithdrawAnchor.user_id.in_(bank_name_list))
            if start_time and end_time == '' and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= data_now,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= start_time))
            if end_time and start_time == '' and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= data_now))
            if start_time and end_time and start_time2 == '' and end_time2 == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            TLogWithdrawAnchor.create_time,
                            '%Y-%m-%d') >= start_time))
            if start_time2 and end_time2 == '' and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= data_now,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= start_time2))
            if end_time2 and start_time2 == '' and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= end_time2,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= data_now))
            if start_time2 and end_time2 and start_time == '' and end_time == '':
                query = query.filter(
                    and_(
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') <= end_time2,
                        func.date_format(
                            TLogWithdrawAnchor.logtime,
                            '%Y-%m-%d') >= start_time2))
            query = query.order_by(TLogWithdrawAnchor.id.desc())
            query_result = query.all()
            total = query.count()
            lst = list()

            for item in query_result:
                lst.append({
                    'id': item[0].id or 0,
                    'user_id': item[0].user_id or 0,
                    'money': str(item[0].money) or '',
                    'remark': str(item[0].remark) or '',
                    'sevice_money': str(item[0].sevice_money) or '',
                    'money_balance': str(item[0].money_balance) or '',
                    'sevice_money_balance': str(item[0].sevice_money_balance) or '',
                    'money_rp': str(item[0].money_rp) or '',
                    'sevice_money_rp': str(item[0].sevice_money_rp) or '',
                    'apply_state': item[0].apply_state or '',
                    'create_time': item[0].create_time.isoformat() or '',
                    'logtime': item[0].logtime.isoformat() or '',
                    'id_user_name': str(item[1].id_user_name) or '',
                    'id_number': str(item[1].id_number) or '',
                    'id_img_front': str(item[1].id_img_front) or '',
                    'id_img_back': str(item[1].id_img_back) or '',
                    'bank_name': str(item[1].bank_name) or '',
                    'bank_card_number': str(item[1].bank_card_number) or '',
                    'hold_user_name': str(item[1].hold_user_name) or '',
                    'bank_sub_name': str(item[1].bank_sub_name) or '',
                    'qq_number': str(item[1].qq_number) or '',
                    'identity_id': str(item[1].id) or '',
                    'u_mobile_number': str(item[1].u_mobile_number) or '',
                })
            ret = dict()
            # withdraw_list = app_map().TLogWithdrawAnchor()
            # guild_list = app_map().Baseuser()

            adsuniongroup = app_map().Adsuniongroup()
            print(adsuniongroup)
            # union_list = app_map().Baseunion()
            # ret['page_index'] = limit['page_index']
            ret['total'] = total
            ret['data'] = lst
            for info_data in ret['data']:
                # if info_data['user_id'] in withdraw_list:
                #     info_data['id_user_name'] = withdraw_list[info_data['user_id']]['id_user_name']
                #     info_data['id_number'] = withdraw_list[info_data['user_id']]['id_number']
                #     info_data['id_img_front'] = withdraw_list[info_data['user_id']]['id_img_front']
                #     info_data['id_img_back'] = withdraw_list[info_data['user_id']]['id_img_back']
                #     info_data['bank_name'] = withdraw_list[info_data['user_id']]['bank_name']
                #     info_data['bank_card_number'] = withdraw_list[info_data['user_id']]['bank_card_number']
                #     info_data['hold_user_name'] = withdraw_list[info_data['user_id']]['hold_user_name']
                #     info_data['bank_sub_name'] = withdraw_list[info_data['user_id']]['bank_sub_name']
                #     info_data['qq_number'] = withdraw_list[info_data['user_id']]['qq_number']
                # else:
                #     anchor_list_bank = query_bank_name.filter(TIdentityPersonal.user_id == info_data['user_id']).first()
                #     if anchor_list_bank:
                #         info_data['id_user_name'] = anchor_list_bank.id_user_name
                #         info_data['id_number'] = anchor_list_bank.id_number
                #         info_data['id_img_front'] = anchor_list_bank.id_img_front
                #         info_data['id_img_back'] = anchor_list_bank.id_img_back
                #         info_data['bank_name'] = anchor_list_bank.bank_name
                #         info_data['bank_card_number'] = anchor_list_bank.bank_card_number
                #         info_data['hold_user_name'] = anchor_list_bank.hold_user_name
                #         info_data['bank_sub_name'] = anchor_list_bank.bank_sub_name
                #         info_data['qq_number'] = anchor_list_bank.qq_number

                # if info_data['user_id'] in guild_list:
                #     info_data['u_mobile_number'] = guild_list[info_data['user_id']]['u_mobile_number']
                # else:
                #     anchor_list_phone = query_guild.filter(BaseUser.user_id == info_data['user_id']).first()
                #     if anchor_list_phone:
                #         info_data['u_mobile_number'] = anchor_list_phone.u_mobile_number

                # if info_data['user_id'] in user_room_list:
                #     room_id_data = user_room_list[info_data['user_id']]['room_id']
                #     platform_id_data = user_room_list[info_data['user_id']]['platform_id']
                #     if (str(platform_id_data) + '_' + str(room_id_data)) in adsuniongroup:
                #         ads_union_id_data = adsuniongroup[str(platform_id_data) + '_' + str(room_id_data)]['union_id']
                #         ads_room_url_data = adsuniongroup[str(platform_id_data) + '_' + str(room_id_data)][
                #             'source_link']
                #         union_name_data = union_list[ads_union_id_data]['union_name']
                #         info_data['room_url'] = ads_room_url_data
                #         info_data['union_name'] = union_name_data
                # else:
                #     info_data['room_url'] = '-'
                #     info_data['union_name'] = '-'

                if info_data['user_id'] in adsuniongroup:
                    ads_union_id_data = adsuniongroup[str(
                        info_data['user_id'])]['union_id']
                    ads_room_url_data = adsuniongroup[str(
                        info_data['user_id'])]['source_link']
                    # union_name_data = union_list[ads_union_id_data]['union_name']
                    info_data['room_url'] = ads_room_url_data
                    info_data['union_name'] = ads_union_id_data
                else:
                    info_data['room_url'] = '-'
                    info_data['union_name'] = '-'

                if info_data['apply_state'] == 10:
                    info_data['apply_name'] = '未处理'
                elif info_data['apply_state'] == 15:
                    info_data['apply_name'] = '已审核'
                elif info_data['apply_state'] == 11:
                    info_data['apply_name'] = '审核未通过'
                elif info_data['apply_state'] == 20:
                    info_data['apply_name'] = '已提交财务'
                elif info_data['apply_state'] == 30:
                    info_data['apply_name'] = '打款异常'
                elif info_data['apply_state'] == 35:
                    info_data['apply_name'] = '打款异常已处理'
                elif info_data['apply_state'] == 40:
                    info_data['apply_name'] = '已完成'

                withdraw_yes_no = self.db_wealth.query(TLogWithdrawAnchor).filter(
                    and_(TLogWithdrawAnchor.user_id == info_data['user_id'],
                         TLogWithdrawAnchor.apply_state == 40)).all()
                if withdraw_yes_no:
                    info_data['withdraw_yes_no'] = '是'
                else:
                    info_data['withdraw_yes_no'] = '否'

                # if 'u_mobile_number' not in info_data:
                #     info_data['u_mobile_number'] = '-'
                # if 'id_user_name' not in info_data:
                #     info_data['id_user_name'] = '-'
                #     info_data['id_number'] = '-'
                #     info_data['id_img_front'] = '-'
                #     info_data['id_img_back'] = '-'
                #     info_data['bank_name'] = '-'
                #     info_data['bank_card_number'] = '-'
                #     info_data['hold_user_name'] = '-'
                #     info_data['bank_sub_name'] = '-'
                #     info_data['qq_number'] = '-'
                if 'union_name' not in info_data:
                    info_data['union_name'] = '-'
                    info_data['room_url'] = '-'
            # for item in app_map().TLogWithdrawAnchor():
            list_name = [
                '提现ID',
                '用户ID',
                '手机号',
                '实际需打款金额',
                '广告收入提现金额(已扣除服务费)',
                '广告收入提现服务费',
                '红包提现金额',
                '申请时间',
                '银行名称',
                '银行卡号',
                '支行名',
                '持卡人姓名',
                '身份证号',
                '身份证正面照片',
                '身份证背面照片',
                'qq号',
                '当前余额',
                '状态:审核中(10),审核未通过(11),已审核(15), 打款中(20),打款异常(30),打款异常已处理(35),已完成(40)',
                '公会名称',
                '房间地址',
                '是否有已支付提现']

            els_url = export(ret['data'], list_name, list_name)
            self.write_json(0, data=els_url)
            # self.db_wealth.close()
            # self.db_guild.close()
            # self.db_ads.close()
            # return
        except Exception as e:
            # session.rollback()
            # self.db_wealth.close()
            # self.db_guild.close()
            # self.db_ads.close()
            log.e('WithdrawanchorUpInfoHanderAll:' + str(e))
            self.write_json(500, '提现导出失败')
            return
        finally:
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()


class WithdrawanchorEdInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            ids = args["ids"]
            type = args["type"]
        log_list = list()
        try:
            date_now = datetime.datetime.now()
            query = self.db_wealth.query(TLogWithdrawAnchor)
            user = self.get_current_user()

            if ids:
                for item in ids:
                    query_list = query.filter(
                        TLogWithdrawAnchor.id == item).first()
                    if query_list.apply_state == 10:
                        if type == 11 or type == 15:
                            query.filter(TLogWithdrawAnchor.id == item).update(
                                {TLogWithdrawAnchor.apply_state: str(type),
                                 TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)
                    elif query_list.apply_state == 11:
                        if type == 15:
                            query.filter(TLogWithdrawAnchor.id == item).update(
                                {TLogWithdrawAnchor.apply_state: str(type),
                                 TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)
                    elif query_list.apply_state == 15:
                        if type == 20:
                            query.filter(TLogWithdrawAnchor.id == item).update(
                                {TLogWithdrawAnchor.apply_state: str(type),
                                 TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)
                    elif query_list.apply_state == 20:
                        if type == 30 or type == 40 or type == 35:
                            if type == 40:
                                query.filter(TLogWithdrawAnchor.id == item).update(
                                    {TLogWithdrawAnchor.apply_state: str(type),
                                     TLogWithdrawAnchor.finish_time: date_now,
                                     TLogWithdrawAnchor.logtime: date_now})
                            else:
                                query.filter(TLogWithdrawAnchor.id == item).update(
                                    {TLogWithdrawAnchor.apply_state: str(type),
                                     TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)
                    elif query_list.apply_state == 30:
                        if type == 35:
                            query.filter(TLogWithdrawAnchor.id == item).update(
                                {TLogWithdrawAnchor.apply_state: str(type),
                                 TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)
                    elif query_list.apply_state == 35:
                        if type == 40 or type == 30 or type == 20:
                            if type == 40:
                                query.filter(TLogWithdrawAnchor.id == item).update(
                                    {TLogWithdrawAnchor.apply_state: str(type),
                                     TLogWithdrawAnchor.finish_time: date_now,
                                     TLogWithdrawAnchor.logtime: date_now})
                            else:
                                query.filter(TLogWithdrawAnchor.id == item).update(
                                    {TLogWithdrawAnchor.apply_state: str(type),
                                     TLogWithdrawAnchor.logtime: date_now})
                        else:
                            log_list.append(item)

                    elif query_list.apply_state == 40:
                        log_list.append(item)

                if user['role_id'] == 9:
                    if type != 10 and type != 15 and type != 11 and type != 30 and type != 35:
                        self.write_json(-3, '您是运营没有权限修改')
                    else:
                        self.db_wealth.commit()
                        oplog = AdsOpLog()
                        oplog.op_type = 3
                        user = self.get_current_user()
                        oplog.op_user_id = user["id"]
                        oplog.op_user_name = user["name"]
                        oplog.op_desc = '修改提现状态 user_id:' + str(ids) + " 对应的apply_state:" + str(
                            type) + " 失败无效的提现id(此状态对应的修改不对):" + str(log_list)
                        co = {"id": ids, "对应的apply_state": type}
                        oplog.op_content = str(co)
                        oplog.createtime = datetime.datetime.now()
                        self.db_adm.add(oplog)
                        self.db_adm.commit()
                        if len(log_list) > 0:
                            self.write_json(-2, str(log_list))
                        else:
                            self.write_json(0, '修改成功')

                elif user['role_id'] == 3:
                    if type != 20 and type != 30 and type != 35 and type != 40:
                        self.write_json(-3, '您是财务没有权限修改')
                    else:
                        self.db_wealth.commit()
                        oplog = AdsOpLog()
                        oplog.op_type = 3
                        user = self.get_current_user()
                        oplog.op_user_id = user["id"]
                        oplog.op_user_name = user["name"]
                        oplog.op_desc = '修改提现状态 user_id:' + str(ids) + " 对应的apply_state:" + str(
                            type) + " 失败无效的提现id(此状态对应的修改不对):" + str(log_list)
                        co = {"id": ids, "对应的apply_state": type}
                        oplog.op_content = str(co)
                        oplog.createtime = datetime.datetime.now()
                        self.db_adm.add(oplog)
                        self.db_adm.commit()
                        if len(log_list) > 0:
                            self.write_json(-2, str(log_list))
                        else:
                            self.write_json(0, '修改成功')
                        self.db_adm.close()
                elif user['role_id'] == 0:
                    self.db_wealth.commit()
                    oplog = AdsOpLog()
                    oplog.op_type = 3
                    user = self.get_current_user()
                    oplog.op_user_id = user["id"]
                    oplog.op_user_name = user["name"]
                    oplog.op_desc = '修改提现状态 user_id:' + str(ids) + " 对应的apply_state:" + str(
                        type) + " 失败无效的提现id(此状态对应的修改不对):" + str(log_list)
                    co = {"id": ids, "对应的apply_state": type}
                    oplog.op_content = str(co)
                    oplog.createtime = datetime.datetime.now()
                    self.db_adm.add(oplog)
                    self.db_adm.commit()
                    if len(log_list) > 0:
                        self.write_json(-2, str(log_list))
                    else:
                        self.write_json(0, '修改成功')
                else:
                    self.write_json(-3, '您没有权限修改')

            else:
                self.write_json(-1, '没有选中修改项')
        except Exception as e:
            self.db_wealth.rollback()
            log.e(e)
            self.write_json(500, "修改失败")
        finally:
            self.db_wealth.close()
            self.db_adm.close()


class WithdrawanchorEdCommitHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            id = args["id"]
            commit = args["commit"]
        log_list = list()
        try:
            date_now = datetime.datetime.now()
            query = self.db_wealth.query(TLogWithdrawAnchor)
            if id:
                query.filter(TLogWithdrawAnchor.id == id).update(
                    {TLogWithdrawAnchor.remark: str(commit),
                     TLogWithdrawAnchor.logtime: date_now})
                self.db_wealth.commit()
                oplog = AdsOpLog()
                oplog.op_type = 3
                user = self.get_current_user()
                oplog.op_user_id = user["id"]
                oplog.op_user_name = user["name"]
                oplog.op_desc = '修改提现备注 user_id:' + \
                    str(id) + " 对应的remark:" + str(commit)
                co = {"id": id, "对应的remark": commit}
                oplog.op_content = str(co)
                oplog.createtime = datetime.datetime.now()
                self.db_adm.add(oplog)
                self.db_adm.commit()
                if len(log_list) > 0:
                    self.write_json(-2, str(log_list))
                else:
                    self.write_json(0, '修改成功')
            else:
                self.write_json(-1, '没有选中修改项')
        except Exception as e:
            log.e(e)
            self.write_json(500, "修改失败")
        finally:
            self.db_wealth.close()
            self.db_adm.close()


class WithdrawanchorEdIdentityHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            id = args["id"]
            id_user_name = args["id_user_name"]
            id_number = args["id_number"]
            bank_name = args["bank_name"]
            bank_card_number = args["bank_card_number"]
            hold_user_name = args["hold_user_name"]
            bank_sub_name = args["bank_sub_name"]
            qq_number = args["qq_number"]
            apply_name = args["apply_name"]

        log_list = list()
        user = self.get_current_user()

        try:
            date_now = datetime.datetime.now()
            query = self.db_wealth.query(Tlogwithdrawanchoridentityinfo)
            if user['role_id'] == 9 or user['role_id'] == 0:
                if apply_name != '未处理' and apply_name != '审核未通过' and apply_name != '打款异常':
                    self.write_json(-3, '非 未处理,审核未通过,打款异常 此三个状态不可修改')
                else:
                    if id:
                        query.filter(Tlogwithdrawanchoridentityinfo.id == id).update(
                            {Tlogwithdrawanchoridentityinfo.id_user_name: str(id_user_name),
                             Tlogwithdrawanchoridentityinfo.id_number: str(id_number),
                             Tlogwithdrawanchoridentityinfo.bank_name: str(bank_name),
                             Tlogwithdrawanchoridentityinfo.bank_card_number: str(bank_card_number),
                             Tlogwithdrawanchoridentityinfo.hold_user_name: str(hold_user_name),
                             Tlogwithdrawanchoridentityinfo.bank_sub_name: str(bank_sub_name),
                             Tlogwithdrawanchoridentityinfo.qq_number: str(qq_number),
                             Tlogwithdrawanchoridentityinfo.logtime: date_now})
                        self.db_wealth.commit()
                        oplog = AdsOpLog()
                        oplog.op_type = 3
                        user = self.get_current_user()
                        oplog.op_user_id = user["id"]
                        oplog.op_user_name = user["name"]
                        oplog.op_desc = '修改提现备注 user_id:' + \
                            str(id) + " 对应的id_user_name:" + str(id_user_name)
                        co = {"id": id, "对应的id_user_name": id_user_name}
                        oplog.op_content = str(co)
                        oplog.createtime = datetime.datetime.now()
                        self.db_adm.add(oplog)
                        self.db_adm.commit()
                        if len(log_list) > 0:
                            self.write_json(-2, str(log_list))
                        else:
                            self.write_json(0, '修改成功')

                    else:
                        self.write_json(-1, '没有选中修改项')
            else:
                self.write_json(-4, '非高级运维用户不可修改')
        except Exception as e:
            self.db_wealth.rollback()
            log.e(e)
            self.write_json(500, "修改失败")
        finally:
            self.db_wealth.close()
            self.db_adm.close()


class WithdrawanchorIMInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        add_withdrawanchor_select = self.get_argument(
            "add_withdrawanchor_select", None)
        sql_session = None
        session_anchor = None
        user = self.get_current_user()
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径
        # aa=os.path.dirname(os.getcwd())
        try:
            # 提取表单中‘name’为‘infile’的文件元数据
            file_metas = self.request.files['infile']
            data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 根据公会名，查询公会的id
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for meta in file_metas:
                filename = data_now_str + '(' + meta['filename'] + ')'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            # 读取文件
            # print(filename)
            workbook = xlrd.open_workbook(filepath)
            os.remove(os.path.join(upload_path, filename))
            # 拿到表名
            sheets = workbook.sheet_names()
            # 第一个表
            worksheet = workbook.sheet_by_name(sheets[0])
            # 行数
            nrows = worksheet.nrows
            if nrows <= 1:
                self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
                return
            ret = list()
            for i in range(1, worksheet.nrows):
                temp = dict()
                temp['id'] = int(worksheet.cell(i, 0).value)
                # temp['apply_type'] = str(worksheet.cell(i, 16).value)
                # date = xldate_as_tuple(worksheet.cell(i, 4).value, 0)
                # temp['create_time'] = datetime.datetime(*date)
                ret.append(temp)

            import_time = data_now_str
            log_list = list()
            log_list_all = list()
            query = self.db_wealth.query(TLogWithdrawAnchor)
            add_withdrawanchor_select = int(add_withdrawanchor_select)
            for item in ret:
                query_list = query.filter(
                    TLogWithdrawAnchor.id == item['id']).first()
                log_list_all.append(item['id'])
                if query_list.apply_state == 10:
                    if add_withdrawanchor_select == 11 or add_withdrawanchor_select == 15:
                        query.filter(TLogWithdrawAnchor.id == item['id']).update(
                            {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                             TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])
                elif query_list.apply_state == 11:
                    if add_withdrawanchor_select == 15:
                        query.filter(TLogWithdrawAnchor.id == item['id']).update(
                            {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                             TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])
                elif query_list.apply_state == 15:
                    if add_withdrawanchor_select == 20:
                        query.filter(TLogWithdrawAnchor.id == item['id']).update(
                            {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                             TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])
                elif query_list.apply_state == 20:
                    if add_withdrawanchor_select == 30 or add_withdrawanchor_select == 40 or add_withdrawanchor_select == 35:
                        if add_withdrawanchor_select == 40:
                            query.filter(TLogWithdrawAnchor.id == item['id']).update(
                                {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                                 TLogWithdrawAnchor.finish_time: import_time,
                                 TLogWithdrawAnchor.logtime: import_time})
                        else:
                            query.filter(TLogWithdrawAnchor.id == item['id']).update(
                                {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                                 TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])
                elif query_list.apply_state == 30:
                    if add_withdrawanchor_select == 35:
                        query.filter(TLogWithdrawAnchor.id == item['id']).update(
                            {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                             TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])
                elif query_list.apply_state == 35:
                    if add_withdrawanchor_select == 40 or add_withdrawanchor_select == 30 or add_withdrawanchor_select == 20:
                        if add_withdrawanchor_select == 40:
                            query.filter(TLogWithdrawAnchor.id == item['id']).update(
                                {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                                 TLogWithdrawAnchor.finish_time: import_time,
                                 TLogWithdrawAnchor.logtime: import_time})
                        else:
                            query.filter(TLogWithdrawAnchor.id == item['id']).update(
                                {TLogWithdrawAnchor.apply_state: int(add_withdrawanchor_select),
                                 TLogWithdrawAnchor.logtime: import_time})
                    else:
                        log_list.append(item['id'])

                elif query_list.apply_state == 40:
                    log_list.append(item['id'])

            oplog = AdsOpLog()
            oplog.op_type = 3
            if user['role_id'] == 9:
                if add_withdrawanchor_select != 10 and add_withdrawanchor_select != 15 and add_withdrawanchor_select != 11 and add_withdrawanchor_select != 30 and add_withdrawanchor_select != 35:
                    self.write_json(-3, '您是运营没有权限修改')
                else:
                    user = self.get_current_user()
                    oplog.op_user_id = user["id"]
                    oplog.op_user_name = user["name"]
                    oplog.op_desc = '修改提现状态(批量) excel导入文件:' + filename + ", 对应的apply_state:" + str(
                        add_withdrawanchor_select) + ",错误无效的提现ID为: " + str(log_list)
                    co = {
                        "ID": str(log_list_all),
                        "对应的apply_state": add_withdrawanchor_select}
                    oplog.op_content = str(co)
                    oplog.createtime = datetime.datetime.now()
                    self.db_adm.add(oplog)
                    self.db_adm.commit()

                    if len(log_list) > 0:
                        self.write_json(-2, str(log_list))
                    else:
                        self.write_json(1, '上传修改成功')
                    self.db_wealth.commit()
            elif user['role_id'] == 3:
                if add_withdrawanchor_select != 20 and add_withdrawanchor_select != 30 and add_withdrawanchor_select != 35 and add_withdrawanchor_select != 40:
                    self.write_json(-3, '您是财务没有权限修改')
                else:
                    user = self.get_current_user()
                    oplog.op_user_id = user["id"]
                    oplog.op_user_name = user["name"]
                    oplog.op_desc = '修改提现状态(批量) excel导入文件:' + filename + ", 对应的apply_state:" + str(
                        add_withdrawanchor_select) + ",错误无效的提现ID为: " + str(log_list)
                    co = {
                        "ID": str(log_list_all),
                        "对应的apply_state": add_withdrawanchor_select}
                    oplog.op_content = str(co)
                    oplog.createtime = datetime.datetime.now()
                    self.db_adm.add(oplog)
                    self.db_adm.commit()

                    if len(log_list) > 0:
                        self.write_json(-2, str(log_list))
                    else:
                        self.write_json(1, '上传修改成功')
                    self.db_wealth.commit()
            elif user['role_id'] == 0:
                user = self.get_current_user()
                oplog.op_user_id = user["id"]
                oplog.op_user_name = user["name"]
                oplog.op_desc = '修改提现状态(批量) excel导入文件:' + filename + ", 对应的apply_state:" + str(
                    add_withdrawanchor_select) + ",错误无效的提现ID为: " + str(log_list)
                co = {"ID": str(log_list_all),
                      "对应的apply_state": add_withdrawanchor_select}
                oplog.op_content = str(co)
                oplog.createtime = datetime.datetime.now()
                self.db_adm.add(oplog)
                self.db_adm.commit()

                if len(log_list) > 0:
                    self.write_json(-2, str(log_list))
                else:
                    self.write_json(1, '上传修改成功')
                self.db_wealth.commit()
            else:
                self.write_json(-3, '您没有权限修改')
            # self.db_wealth.close()
            # self.db_adm.close()
            return
        # 认证公会审核通过（4.0）
        except Exception as e:
            # session.rollback()
            log.e('admin.roomImportAdsInfo_error:' + str(e))
            self.write_json(0, 'excel数据格式错误,error:{}'.format(e))
            return
        finally:
            self.db_wealth.close()
            self.db_adm.close()


class WithdrawanchorREInfoHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        add_withdrawanchor_select = self.get_argument(
            "add_withdrawanchor_select", None)
        sql_session = None
        session_anchor = None
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径
        # aa=os.path.dirname(os.getcwd())
        try:
            # 提取表单中‘name’为‘infile’的文件元数据
            file_metas = self.request.files['infile']
            data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            # 根据公会名，查询公会的id
            if not os.path.exists(upload_path):
                os.mkdir(upload_path)
            for meta in file_metas:
                filename = data_now_str + '(' + meta['filename'] + ')'
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                    up.write(meta['body'])
            # 读取文件
            # print(filename)
            workbook = xlrd.open_workbook(filepath)
            os.remove(os.path.join(upload_path, filename))
            # 拿到表名
            sheets = workbook.sheet_names()
            # 第一个表
            worksheet = workbook.sheet_by_name(sheets[0])
            # 行数
            nrows = worksheet.nrows
            if nrows <= 1:
                self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
                return
            num_remind = 0
            money_remind = 0.0
            for i in range(1, worksheet.nrows):
                money_remind = float(money_remind) + \
                    float(worksheet.cell(i, 1).value)
                num_remind = int(num_remind) + 1
                # temp['id'] = int(worksheet.cell(i, 1).value)

            self.write_json(
                1, '{num_remind},{money_remind}'.format(
                    num_remind=num_remind, money_remind=round(
                        money_remind, 2)))
            return
        # 认证公会审核通过（4.0）
        except Exception as e:
            # session.rollback()
            log.e('admin.roomImportAdsInfo_error:' + str(e))
            self.write_json(0, 'excel数据格式错误,error:{}'.format(e))
            return
        finally:
            if sql_session:
                sql_session.close()
            if session_anchor:
                session_anchor.close()
            self.db_wealth.close()


# -------------------------------结算---------------------------
class IncomePackListHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/income/incomePack_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        try:
            limit, args = self.get_pages_args()
            sql = "select  package_id,package_name,begin_time,end_time,anchor_balance,union_balance,balance_last_time,status,plat_balance" \
                  ",agent_balance,affairs_num ,rate from ads_contract_package_info where 1=1"
            filter = args["filter"]
            name = ""
            if "search" in filter.keys():
                name = filter["search"]
            status = filter["status"]
            begin_time = filter["begin_time"]
            end_time = filter["end_time"]
            financial_number = filter["financial_number"]

            if name:
                sql = sql + " and package_name like '%" + name.strip() + "%' "
            if financial_number:
                sql = sql + " and affairs_num like '%" + financial_number.strip() + "%' "
            if status:
                sql = sql + " and status = " + status.strip()
            if begin_time:
                start = begin_time + " 00:00:00"
                sql = sql + " and end_time >= '" + start + "'"
            if end_time:
                end = end_time + " 23:59:59"
                sql = sql + " and begin_time <= '" + end + "'"

            offset = " ORDER BY package_id DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            query_result = self.db_ads.execute(sql + offset).fetchall()
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            lst = list()
            for item in query_result:
                anchor_balance = str(
                    (item[4]).quantize(
                        Decimal('0.00'))) if item[4] is not None else ""
                union_balance = str(
                    (item[5]).quantize(
                        Decimal('0.00'))) if item[5] is not None else ""
                plat_balance = str(
                    (item[8]).quantize(
                        Decimal('0.00'))) if item[8] is not None else ""
                agent_balance = str(
                    (item[9]).quantize(
                        Decimal('0.00'))) if item[9] is not None else ""
                balance_last_time = item[6].isoformat(
                ) if item[6] is not None else ""
                lst.append({
                    'package_id': item[0],
                    'package_name': item[1],
                    'begin_time': item[2].isoformat(),
                    'end_time': item[3].isoformat(),
                    'anchor_balance': anchor_balance,
                    'union_balance': union_balance,
                    'balance_last_time': balance_last_time,
                    'status': item[7],
                    'plat_balance': plat_balance,
                    'agent_balance': agent_balance,
                    'affairs_num': item[10],
                })
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            # session.rollback()
            log.e('incomePackListHander:' + str(e))
            self.write_json(500, '结算查询失败')
        finally:
            # self.db_wealth.close()
            # self.db_guild.close()
            self.db_ads.close()


class IncomePackList4ClosedHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # account_type 1 关账前结算 2 关账后结算
        account_type = self.get_argument('account_type')
        url = '/ads_manager/{}/incomePack_list.mako'
        if str(account_type) == '1':
            url = url.format('income_close_account')
        elif str(account_type) == '2':
            url = url.format('income_other_account')
        self.render(url)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        account_type = self.get_argument(
            'account_type', None)  # account_type  1 关账之前结算，2关账之后结算
        try:
            limit, args = self.get_pages_args()
            sql = "select  package_id,package_name,begin_time,end_time,{} anchor_balance," \
                  "{} union_balance,balance_last_time,status,{} plat_balance" \
                  ",{} agent_balance,affairs_num ,rate,log_time from ads_contract_package_info where 1=1"

            if account_type == '1':
                sql = sql.format('anchor_balance_close', 'union_balance_close',
                                 'plat_balance_close', 'agent_balance_close')
            elif account_type == '2':
                sql = sql.format('anchor_balance_other', 'union_balance_other',
                                 'plat_balance_other', 'agent_balance_other')
            else:
                self.write_json(-1, 'account_type不能为空')
                return

            filter = args["filter"]
            name = ""
            if "search" in filter.keys():
                name = filter["search"]
            status = filter["status"]
            begin_time = filter["begin_time"]
            end_time = filter["end_time"]
            financial_number = filter["financial_number"]
            if name:
                sql = sql + " and package_name like '%" + name.strip() + "%' "
            if financial_number:
                sql = sql + " and affairs_num like '%" + financial_number.strip() + "%' "
            if status:
                sql = sql + " and status = " + status.strip()
            if begin_time:
                start = begin_time + " 00:00:00"
                sql = sql + " and end_time >= '" + start + "'"
            if end_time:
                end = end_time + " 23:59:59"
                sql = sql + " and begin_time <= '" + end + "'"

            offset = " ORDER BY package_id DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            query_result = self.db_ads.execute(sql + offset).fetchall()
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            lst = list()
            for item in query_result:
                anchor_balance = str(
                    (item[4]).quantize(
                        Decimal('0.00'))) if item[4] is not None else ""
                union_balance = str(
                    (item[5]).quantize(
                        Decimal('0.00'))) if item[5] is not None else ""
                plat_balance = str(
                    (item[8]).quantize(
                        Decimal('0.00'))) if item[8] is not None else ""
                agent_balance = str(
                    (item[9]).quantize(
                        Decimal('0.00'))) if item[9] is not None else ""
                balance_last_time = item[6].isoformat(
                ) if item[6] is not None else ""
                lst.append({
                    'package_id': item[0],
                    'package_name': item[1],
                    'begin_time': item[2].isoformat() if item[2] else '',
                    'end_time': item[3].isoformat() if item[3] else '',
                    'anchor_balance': anchor_balance,
                    'union_balance': union_balance,
                    'balance_last_time': balance_last_time,
                    'status': item[7],
                    'plat_balance': plat_balance,
                    'agent_balance': agent_balance,
                    'affairs_num': item[10],
                    'log_time': item[12].isoformat() if item[12] else '',
                })
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
            self.db_ads.close()
        except Exception as e:
            log.e('incomePackListHander:' + str(e))
            self.write_json(500, '结算查询失败')
        finally:
            self.db_ads.close()


class IncomeAnchorListHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        package_id = self.get_argument("package_id", None)
        package_name = self.get_argument("package_name", None)
        income_type = self.get_argument("type", None)
        total = self.get_argument("total", None)
        unionlist = app_map().getUnionList()

        if package_id is None:
            self.write_json(-1, "系统错误")
            return
        _, lst = app_map().get_platform_map_list()
        self.render(
            "/ads_manager/income/incomeAnchor_list.mako",
            package_id=package_id,
            platformList=lst,
            package_name=package_name,
            income_type=income_type,
            unionList=unionlist,
            total=total)

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]
        package_id = filter["package_id"]
        income_from = filter["income_from"]
        income_type = filter["income_type"]
        plat_id = filter["plat_id"]
        union_id = filter["unionid"]
        income_log_id = filter["income_log_id"]
        user_id = filter["user_id"]
        task_id = filter["task_id"]
        room_id = filter["room_id"]
        begintime = filter["begintime"]
        endtime = filter["endtime"]

        if package_id is None or package_id == "":
            self.write_json(-1, "系统错误")
            return

        # 找到套餐对应的need_id
        a = self.findNeedIdsByPackId(package_id)
        if not a:
            ret = dict()
            ret['page_index'] = limit['page_index']
            ret['total'] = 0
            ret['data'] = []
            self.write_json(0, data=ret)
            self.write_json(0, '该合同没有对应的套餐信息', ret)
            return

        rate = self.findRate4Package(package_id)
        rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))
        sql = "select a.income_log_id,a.income_from,a.union_id,a.user_id,a.task_id,a.task_create_time," \
              "a.room_id,a.logtime,a.income,a.play_id,a.plat_id,a.agent_id,a.income_type from" \
              "  T_log_income_anchor a  where 1=1 and need_id in ({})".format(a)

        sql_total_income = 'select sum(income) from T_log_income_anchor a where 1=1 and need_id in ({})'.format(
            a)
        # 组装sql
        sql_list = list()
        if income_type:
            if income_type == '4':
                sql_list.append(
                    " and ((a.income_type = '1' and a.agent_id=0) or a.income_type='2' ) ")
            else:
                sql_list.append(
                    " and a.income_type = " +
                    income_type.strip() +
                    " ")

        if income_from:
            sql_list.append(
                " and a.income_from like '%" +
                income_from.strip() +
                "%' ")

        if plat_id:
            sql_list.append(" and a.plat_id = " + plat_id.strip() + " ")

        if union_id:
            sql_list.append(" and a.union_id = " + union_id.strip() + " ")

        if income_log_id:
            sql_list.append(
                " and a.income_log_id like '%" +
                income_log_id.strip() +
                "%' ")

        if user_id:
            sql_list.append(" and a.user_id like '%" + user_id.strip() + "%' ")

        if task_id:
            sql_list.append(" and a.task_id like '%" + task_id.strip() + "%' ")

        if room_id:
            sql_list.append(" and a.room_id like '%" + room_id.strip() + "%' ")

        if begintime:
            sql_list.append(
                " and a.task_create_time >= '" +
                begintime.strip() +
                "'")

        if endtime:
            sql_list.append(
                " and a.task_create_time <= '" +
                endtime.strip() +
                " 23:59:59 '")

        sqlStr = "".join(sql_list)
        sql = sql + sqlStr
        sql_total_income = sql_total_income + sqlStr
        # total_income = 0
        offset = " ORDER BY a.income_log_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        try:

            query_result = self.db_wealth.execute(sql + offset).fetchall()
            total_income = self.db_wealth.execute(sql_total_income).scalar()
            count = self.db_wealth.execute(
                "select count(*) from T_log_income_anchor a "
                " where 1=1 and need_id in  ({}) {}".format(
                    a, sqlStr)).scalar()
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
            return
        finally:
            self.db_wealth.close()
        lst = list()

        head = [
            'income_log_id',
            'income_from',
            'union_id',
            'user_id',
            'task_id',
            'task_create_time',
            'room_id',
            'logtime',
            'income',
            'play_id',
            'plat_id',
            'agent_id',
            'income_type']

        for item in query_result:
            temp = dict(zip(head, item))
            temp['task_create_time'] = temp['task_create_time'].isoformat()
            temp['logtime'] = temp['logtime'].isoformat()
            union_name = ""
            if item[2]:
                union_name = app_map().getUnionName(item[2])

            temp['union_name'] = union_name
            anchor_name = ''
            source_link = ''
            roomInfo = app_map().getRoomInfoById(
                temp['room_id'], temp['plat_id'])
            if roomInfo:
                anchor_name = roomInfo["emcee"]
                source_link = roomInfo["source_link"]
            temp['anchor_name'] = anchor_name
            temp['source_link'] = source_link
            temp['income'] = str((item[8]).quantize(Decimal('0.00')))
            temp['plat_name'] = app_map().get_platform_name(temp['plat_id'])
            record_path = ''
            screen_shot_path = ''
            popularity = ''
            playlog = app_map().getPlayLog(item[9])
            if playlog:
                record_path = playlog[1]
                screen_shot_path = playlog[2]
                popularity = playlog[3]
            temp['record_path'] = record_path
            temp['screen_shot_path'] = screen_shot_path
            temp['popularity'] = popularity
            plat_id = item[11]
            agent_id = item[12]
            if income_type == '4':
                admplat = app_map().getAdmPlat(plat_id)
                if admplat:
                    income = str(
                        (item[8] * rate * Decimal(str(admplat[2] / 100))).quantize(Decimal('0.00')))
                    temp['income'] = income
            agent_name = ''
            if income_type == '2':
                income = str((item[8] * rate).quantize(Decimal('0.00')))
                temp['income'] = income
            if income_type == '3':
                admAgent = app_map().getAdmAgent(agent_id)
                agent_name = admAgent[1] if admAgent else ''
            temp['agent_name'] = agent_name
            lst.append(temp)
        if total_income and income_type == '4' or income_type == '2':
            total_income = str(
                (total_income *
                 rate).quantize(
                    Decimal('0.00'))) if total_income else 0
        else:
            total_income = str(
                total_income.quantize(
                    Decimal('0.00'))) if total_income else 0
        ret = dict()
        ret['page_index'] = limit['page_index']
        ret['total'] = count
        ret['data'] = lst
        ret['total_income'] = total_income
        self.write_json(0, data=ret)

    def findNeedIdsByPackId(self, package_id):
        sql_need = "SELECT need_id from  ads_need_info where package_id= {}".format(
            int(package_id))
        result = self.db_ads.execute(sql_need).fetchall()
        self.db_ads.close()
        a = list()
        for r in result:
            a.append(str(r[0]))
        a = ",".join(a)
        return a

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


class IncomeAnchor4closeListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        package_id = self.get_argument("package_id", None)
        package_name = self.get_argument("package_name", None)
        income_type = self.get_argument("type", None)
        total = self.get_argument("total", None)
        account_type = self.get_argument("account_type", None)
        unionlist = app_map().getUnionList()

        if package_id is None:
            self.write_json(-1, "系统错误")
            return
        _, lst = app_map().get_platform_map_list()

        self.db_wealth.close()

        url = '/ads_manager/{}/incomeAnchor_list.mako'
        if account_type == '1':
            url = url.format('income_close_account')
        if account_type == '2':
            url = url.format('income_other_account')
        self.render(
            url,
            package_id=package_id,
            platformList=lst,
            package_name=package_name,
            income_type=income_type,
            unionList=unionlist,
            total=total,
            account_type=account_type)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]

        package_id = filter["package_id"]
        income_from = filter["income_from"]
        income_type = filter["income_type"]
        plat_id = filter["plat_id"]
        union_id = filter["unionid"]
        income_log_id = filter["income_log_id"]
        user_id = filter["user_id"]
        task_id = filter["task_id"]
        room_id = filter["room_id"]
        begintime = filter["begintime"]
        endtime = filter["endtime"]
        account_type = filter["account_type"]  # 1 结账结算 2 结账后的结算

        if package_id is None or package_id == "":
            self.write_json(-1, "系统错误")
            return

        # 找到套餐对应的need_id
        a = self.findNeedIdsByPackId(package_id)
        if not a:
            ret = dict()
            ret['page_index'] = limit['page_index']
            ret['total'] = 0
            ret['data'] = []
            self.write_json(0, data=ret)
            self.write_json(0, '该合同没有对应的套餐信息', ret)
            return

        rate = self.findRate4Package(package_id)
        rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))

        sql = "select a.income_log_id,a.income_from,a.union_id,a.user_id,a.task_id,a.task_create_time," \
              "a.room_id,a.logtime,a.income,a.play_id,a.plat_id,a.agent_id,a.income_type from" \
              "  T_log_income_anchor a  where a.income_from{} and need_id in ({})"

        sql_total_income = 'select sum(income) from   T_log_income_anchor a where income_from{} and need_id in ({})'
        # 关账结算
        if account_type == '1':
            sql = sql.format('!=4', a)
            sql_total_income = sql_total_income.format('!=4', a)
        if account_type == '2':
            sql = sql.format('=4', a)
            sql_total_income = sql_total_income.format('=4', a)

        # 组装sql
        sql_list = list()
        if income_type:
            if income_type == '4':
                sql_list.append(
                    " and ((a.income_type = '1' and a.agent_id=0) or a.income_type='2' ) ")
            else:
                sql_list.append(
                    " and a.income_type = " +
                    income_type.strip() +
                    " ")

        if income_from:
            sql_list.append(
                " and a.income_from like '%" +
                income_from.strip() +
                "%' ")

        if plat_id:
            sql_list.append(" and a.plat_id = " + plat_id.strip() + " ")

        if union_id:
            sql_list.append(" and a.union_id = " + union_id.strip() + " ")

        if income_log_id:
            sql_list.append(
                " and a.income_log_id like '%" +
                income_log_id.strip() +
                "%' ")

        if user_id:
            sql_list.append(" and a.user_id like '%" + user_id.strip() + "%' ")

        if task_id:
            sql_list.append(" and a.task_id like '%" + task_id.strip() + "%' ")

        if room_id:
            sql_list.append(" and a.room_id like '%" + room_id.strip() + "%' ")

        if begintime:
            sql_list.append(
                " and a.task_create_time >= '" +
                begintime.strip() +
                "'")

        if endtime:
            sql_list.append(
                " and a.task_create_time <= '" +
                endtime.strip() +
                " 23:59:59 '")

        sqlStr = "".join(sql_list)
        sql = sql + sqlStr
        sql_total_income = sql_total_income + sqlStr
        # total_income = 0
        offset = " ORDER BY a.income_log_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        try:
            query_result = self.db_wealth.execute(sql + offset).fetchall()
            total_income = self.db_wealth.execute(sql_total_income).scalar()
            count = self.db_wealth.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()

        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
            return
        finally:
            self.db_wealth.close()
        lst = list()

        head = [
            'income_log_id',
            'income_from',
            'union_id',
            'user_id',
            'task_id',
            'task_create_time',
            'room_id',
            'logtime',
            'income',
            'play_id',
            'plat_id',
            'agent_id',
            'income_type']

        for item in query_result:
            temp = dict(zip(head, item))
            temp['task_create_time'] = temp['task_create_time'].isoformat()
            temp['logtime'] = temp['logtime'].isoformat()
            union_name = ""
            if item[2]:
                union_name = app_map().getUnionName(item[2])
            temp['union_name'] = union_name
            anchor_name = ''
            source_link = ''
            roomInfo = app_map().getRoomInfoById(
                temp['room_id'], temp['plat_id'])
            if roomInfo:
                anchor_name = roomInfo["emcee"]
                source_link = roomInfo["source_link"]
            temp['anchor_name'] = anchor_name
            temp['source_link'] = source_link
            temp['income'] = str((item[8]).quantize(Decimal('0.00')))
            temp['plat_name'] = app_map().get_platform_name(temp['plat_id'])
            record_path = ''
            screen_shot_path = ''
            popularity = ''
            playlog = app_map().getPlayLog(item[9])
            if playlog:
                record_path = playlog[1]
                screen_shot_path = playlog[2]
                popularity = playlog[3]
            temp['record_path'] = record_path
            temp['screen_shot_path'] = screen_shot_path
            temp['popularity'] = popularity
            plat_id = item[10]
            agent_id = item[11]
            if income_type == '4':
                admplat = app_map().getAdmPlat(plat_id)
                if admplat:
                    income = str(
                        (item[8] * rate * Decimal(str(admplat[2] / 100))).quantize(Decimal('0.00')))
                    temp['income'] = income
            agent_name = ''
            if income_type == '2':
                income = str((item[8] * rate).quantize(Decimal('0.00')))
                temp['income'] = income
            if income_type == '3':
                admAgent = app_map().getAdmAgent(agent_id)
                agent_name = admAgent[1] if admAgent else ''
            temp['agent_name'] = agent_name
            lst.append(temp)

        # total_income = (total_income*rate).quantize(Decimal('0.00')) if total_income  else 0
        if income_type == '4' or income_type == '2':
            total_income = str(
                (total_income *
                 rate).quantize(
                    Decimal('0.00'))) if total_income else 0
        else:
            total_income = str(
                total_income.quantize(
                    Decimal('0.00'))) if total_income else 0
        ret = dict()
        ret['page_index'] = limit['page_index']
        ret['total'] = count
        ret['data'] = lst
        ret['total_income'] = total_income
        self.write_json(0, data=ret)
        self.db_wealth.close()

    def findNeedIdsByPackId(self, package_id):
        sql_need = "SELECT need_id from  ads_need_info where package_id= {}".format(
            int(package_id))
        result = self.db_ads.execute(sql_need).fetchall()
        self.db_ads.close()
        a = list()
        for r in result:
            a.append(str(r[0]))
        a = ",".join(a)
        return a

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


# ---------------广告计划查询---------------------------------
class AdvertisingPlanListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render(
            "/ads_manager/advertising_plan_info/advertising_plan_list.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]
        level = ''
        schedule_id = ''
        plan_status = ''
        date = ''
        if "level" in filter.keys():
            level = filter["level"]
            schedule_id = filter["schedule_id"]
            plan_status = filter["plan_status"]
            date = filter["date"]
        try:
            query = self.db_entourage.query(AdsNeedPlanInfo)
            data_now = datetime.datetime.now().strftime('%Y-%m-%d')
            if level:
                query = query.filter(AdsNeedPlanInfo.anchor_level == level)
            if schedule_id:
                query = query.filter(
                    AdsNeedPlanInfo.schedule_id == schedule_id)
            if date:
                query = query.filter(AdsNeedPlanInfo.play_time == date)
            if plan_status == '1':
                query = query.filter(
                    or_(AdsNeedPlanInfo.plan_status == 1, AdsNeedPlanInfo.plan_status == 0))
            elif plan_status:
                query = query.filter(
                    AdsNeedPlanInfo.plan_status == plan_status)

            total = query.count()
            query = query.order_by(AdsNeedPlanInfo.need_plan_id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))

            query_result = query.all()

            lst = list()
            for item in query_result:
                lst.append({
                    'need_plan_id': item.need_plan_id or 0,
                    'task_id': item.task_id or 0,
                    'plan_status': item.plan_status or 0,
                    'schedule_id': item.schedule_id or '',
                    'group_id': item.group_id or '',
                    'flag': item.flag,
                    'anchor_level': item.anchor_level or '',
                    'create_time': item.create_time.isoformat() or '',
                    'logtime': item.logtime.isoformat() or '',
                    'play_time': str(item.play_time) or '',
                })

            ret = dict()
            ret['page_index'] = limit['page_index']
            ret['total'] = total
            ret['data'] = lst

            for info_data in ret['data']:
                if info_data['plan_status'] == 0:
                    info_data['plan_name'] = '未接'
                elif info_data['plan_status'] == 1:
                    info_data['plan_name'] = '未接'
                elif info_data['plan_status'] == 2:
                    info_data['plan_name'] = '已接'
                elif info_data['plan_status'] == 5:
                    info_data['plan_name'] = '完成'
            # for item in app_map().TLogWithdrawAnchor():
            self.write_json(0, data=ret)
            # self.db_wealth.close()
            self.db_entourage.close()
        except Exception as e:
            # session.rollback()
            log.e('incomePackListHander:' + str(e))
            self.write_json(500, '结算查询失败')
            return
        finally:
            # self.db_wealth.close()
            # self.db_guild.close()
            # self.db_ads.close()
            self.db_entourage.close()


class Seleteshcheduleadvertisting(SwxJsonHandler):
    def get(self, *args, **kwargs):
        level = self.get_argument("level", None)
        #
        try:
            lst = []
            query_schedule = ''
            if level:
                query = self.db_entourage.query(
                    distinct(
                        AdsNeedPlanInfo.schedule_id),
                    NeedSchedule.description).join(
                    NeedSchedule,
                    NeedSchedule.schedule_id == AdsNeedPlanInfo.schedule_id).filter(
                    and_(
                        AdsNeedPlanInfo.anchor_level == level,
                        NeedSchedule.enable == 1)).order_by(
                    AdsNeedPlanInfo.schedule_id.desc())
            else:
                query = self.db_entourage.query(
                    distinct(
                        AdsNeedPlanInfo.schedule_id),
                    NeedSchedule.description).join(
                    NeedSchedule,
                    NeedSchedule.schedule_id == AdsNeedPlanInfo.schedule_id).filter(
                    NeedSchedule.enable == 1).order_by(
                    AdsNeedPlanInfo.schedule_id.desc())

            query_schedule = query.all()
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
            for ptype in query_schedule:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_entourage.close()
        except Exception as e:
            self.db_entourage.rollback()
            self.db_entourage.close()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            self.db_entourage.close()


class GetRoomInfoHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        # roomInfoMap = app_map().getRoomInfo()
        roomId = self.get_argument("roomId", None)
        roomInfo = app_map().getRoomInfoById(roomId)
        if roomInfo:
            self.write_json(0, 'succeed', roomInfo)
        else:
            self.write_json(-1, '找不到对应的房间信息')


class IncomeAnchorExportHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # limit, args = self.get_pages_args()
        #
        # filter = args["filter"]
        filename = ''
        package_id = self.get_argument("package_id", None)
        package_name = self.get_argument("package_name", None)
        income_from = self.get_argument("income_from", None)
        plat_id = self.get_argument("plat_id", None)
        income_type = self.get_argument("income_type", None)
        union_id = self.get_argument("union_id", None)
        income_log_id = self.get_argument("income_log_id", None)
        user_id = self.get_argument("user_id", None)
        task_id = self.get_argument("task_id", None)
        room_id = self.get_argument("room_id", None)
        begin_time = self.get_argument("begin_time", None)
        end_time = self.get_argument("end_time", None)

        if package_id is None or package_id == "":
            self.write_json(-1, "系统错误")
            return

        # unionid2nameMap, name2unionidMap = app_map().unionid2nameMap()
        # 找到套餐对应的need_id
        need_ids = self.findNeedIdsByPackId(package_id)
        if not need_ids:
            self.write_json(-1, "没有数据")
            return

        rate = self.findRate4Package(package_id)
        rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))

        sql = "select a.income_log_id,a.income_from,a.union_id,a.user_id,a.task_id,a.task_create_time," \
              "a.room_id,a.logtime,a.income,a.play_id,a.plat_id,a.agent_id from  " \
              "T_log_income_anchor a  where " \
              " need_id in ({})".format(need_ids)

        if package_name:
            filename += "套餐名:" + urllib.parse.unquote(package_name)

        # 组装sql
        sql_list = list()
        if income_type:
            if income_type == '4':
                sql_list.append(
                    " and ((a.income_type = '1' and a.agent_id=0) or a.income_type = '2') ")
            else:
                sql_list.append(
                    " and a.income_type = " +
                    income_type.strip() +
                    " ")

        if income_from:
            sql_list.append(
                " and a.income_from like '%" +
                income_from.strip() +
                "%' ")

        if plat_id:
            sql_list.append(" and a.plat_id = " + plat_id.strip() + " ")

        if union_id:
            sql_list.append(" and a.union_id = " + union_id.strip() + " ")

        if income_log_id:
            sql_list.append(
                " and a.income_log_id like '%" +
                income_log_id.strip() +
                "%' ")

        if user_id:
            sql_list.append(" and a.user_id like '%" + user_id.strip() + "%' ")

        if task_id:
            sql_list.append(" and a.task_id like '%" + task_id.strip() + "%' ")

        if room_id:
            sql_list.append(" and a.room_id like '%" + room_id.strip() + "%' ")
        if begin_time:
            sql_list.append(
                " and a.task_create_time >= '" +
                begin_time.strip() +
                "'")

        if end_time:
            sql_list.append(
                " and a.task_create_time <= '" +
                end_time.strip() +
                " 23:59:59 '")

        sqlStr = "".join(sql_list)
        sql = sql + sqlStr

        offset = " ORDER BY a.income_log_id DESC"
        query_result = self.db_wealth.execute(sql + offset).fetchall()
        lst = list()
        for item in query_result:
            income_log_id = item[0]
            if item[1] == 1:
                income_from = "自然结算"
            elif item[1] == 2:
                income_from = "人工结算"
            else:
                income_from = "申诉结算"
            union_id = item[2]
            union_name = ""
            if item[2]:
                union_name = app_map().getUnionName(item[2])
            user_id = item[3]
            task_id = item[4]
            task_create_time = item[5].isoformat()
            if task_create_time is not None:
                task_create_time = task_create_time.replace("T", " ")

            room_id = item[6]
            plat_id = item[10]
            plat_name = app_map().get_platform_name(plat_id)
            record_path = ''
            screen_shot_path = ''
            popularity = ''
            playlog = app_map().getPlayLog(item[9])
            if playlog:
                record_path = playlog[1]
                screen_shot_path = playlog[2]
                popularity = playlog[3]
            anchor_name = ''
            room_url = ''
            roomInfo = app_map().getRoomInfoById(room_id, plat_id)
            if roomInfo:
                anchor_name = roomInfo["emcee"]
                room_url = roomInfo["source_link"]
            logtime = item[7].isoformat()
            income = str((item[8]).quantize(Decimal('0.00')))
            play_id = item[9]
            plat_id = item[10]
            agent_id = item[11]
            if income_type == '4':
                admplat = app_map().getAdmPlat(plat_id)
                if admplat:
                    income = str(
                        (item[8] * rate * Decimal(str(admplat[2] / 100))).quantize(Decimal('0.00')))

            if income_type == '2':
                income = str((item[8] * rate).quantize(Decimal('0.00')))

            agent_name = ''
            if income_type == '3':
                admAgent = app_map().getAdmAgent(agent_id)
                agent_name = admAgent[1] if admAgent else ''

            lst.append({"income_log_id": income_log_id,
                        "income_from": income_from,
                        "record_path": record_path,
                        "play_id": play_id,
                        "union_id": union_id,
                        "union_name": union_name,
                        "income": income,
                        "screen_shot_path": screen_shot_path,
                        "user_id": user_id,
                        "task_id": task_id,
                        "task_create_time": task_create_time,
                        "room_url": room_url,
                        "agent_name": agent_name,
                        "popularity": popularity,
                        "plat_name": plat_name,
                        "room_id": room_id,
                        "logtime": logtime,
                        "anchor_name": anchor_name})
        self.db_wealth.close()

        list_name = ''
        if income_type == '1' or income_type == '4':
            list_name = [
                '结算id',
                '平台',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']
        elif income_type == '2':
            list_name = [
                '结算工会id',
                '结算工会名称',
                '结算id',
                '平台',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']
        elif income_type == '3':
            list_name = [
                '结算id',
                '经纪公司名称',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']

        els_url = exportIncome(lst, list_name, filename, income_type)
        self.write_json(0, data=els_url)
        return

    def findNeedIdsByPackId(self, package_id):
        sql_need = "SELECT need_id from  ads_need_info where package_id= {}".format(
            int(package_id))
        result = self.db_ads.execute(sql_need).fetchall()
        self.db_ads.close()
        a = list()
        for r in result:
            a.append(str(r[0]))
        a = ",".join(a)
        return a

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


class IncomeAnchorExport4closeHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # limit, args = self.get_pages_args()
        #
        # filter = args["filter"]
        filename = ''
        package_id = self.get_argument("package_id", None)
        package_name = self.get_argument("package_name", None)
        income_from = self.get_argument("income_from", None)
        plat_id = self.get_argument("plat_id", None)
        income_type = self.get_argument("income_type", None)
        union_id = self.get_argument("union_id", None)
        income_log_id = self.get_argument("income_log_id", None)
        user_id = self.get_argument("user_id", None)
        task_id = self.get_argument("task_id", None)
        room_id = self.get_argument("room_id", None)
        account_type = self.get_argument("account_type", None)
        begin_time = self.get_argument("begin_time", None)
        end_time = self.get_argument("end_time", None)
        if package_id is None or package_id == "":
            self.write_json(-1, "系统错误")
            return

        # unionid2nameMap, name2unionidMap = app_map().unionid2nameMap()
        # 找到套餐对应的need_id
        need_ids = self.findNeedIdsByPackId(package_id)
        if not need_ids:
            self.write_json(-1, "没有数据")
            return

        rate = self.findRate4Package(package_id)
        rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))

        sql = "select a.income_log_id,a.income_from,a.union_id,a.user_id,a.task_id,a.task_create_time," \
              "a.room_id,a.logtime,a.income,a.play_id,a.plat_id,a.agent_id from  " \
              "T_log_income_anchor a  where a.income_from{} " \
              " and need_id in ({})"

        if account_type == '1':
            sql = sql.format('!=4', need_ids)
        elif account_type == '2':
            sql = sql.format('=4', need_ids)
        else:
            self.write_json(-1, 'account_type参数异常')
            return

        if package_name:
            filename += "套餐名:" + urllib.parse.unquote(package_name)

        # 组装sql
        sql_list = list()
        if income_type:
            if income_type == '4':
                sql_list.append(
                    " and ((a.income_type = '1' and a.agent_id=0) or a.income_type = '2') ")
            else:
                sql_list.append(
                    " and a.income_type = " +
                    income_type.strip() +
                    " ")

        if income_from:
            sql_list.append(
                " and a.income_from like '%" +
                income_from.strip() +
                "%' ")

        if plat_id:
            sql_list.append(" and a.plat_id = " + plat_id.strip() + " ")

        if union_id:
            sql_list.append(" and a.union_id = " + union_id.strip() + " ")

        if income_log_id:
            sql_list.append(
                " and a.income_log_id like '%" +
                income_log_id.strip() +
                "%' ")

        if user_id:
            sql_list.append(" and a.user_id like '%" + user_id.strip() + "%' ")

        if task_id:
            sql_list.append(" and a.task_id like '%" + task_id.strip() + "%' ")

        if room_id:
            sql_list.append(" and a.room_id like '%" + room_id.strip() + "%' ")
        if begin_time:
            sql_list.append(
                " and a.task_create_time >= '" +
                begin_time.strip() +
                "'")

        if end_time:
            sql_list.append(
                " and a.task_create_time <= '" +
                end_time.strip() +
                " 23:59:59 '")

        sqlStr = "".join(sql_list)
        sql = sql + sqlStr

        offset = " ORDER BY a.income_log_id DESC"
        query_result = self.db_wealth.execute(sql + offset).fetchall()
        lst = list()
        for item in query_result:
            income_log_id = item[0]
            income_from = ''
            if item[1] == 1:
                income_from = "自然结算"
            elif item[1] == 2:
                income_from = "人工结算"
            else:
                income_from = "申诉结算"
            union_id = item[2]
            union_name = ""
            if item[2]:
                union_name = app_map().getUnionName(item[2])
            user_id = item[3]
            task_id = item[4]
            task_create_time = item[5].isoformat()
            if task_create_time is not None:
                task_create_time = task_create_time.replace("T", " ")

            room_id = item[6]
            plat_id = item[10]
            plat_name = app_map().get_platform_name(plat_id)
            record_path = ''
            screen_shot_path = ''
            popularity = ''
            playlog = app_map().getPlayLog(item[9])
            if playlog:
                record_path = playlog[1]
                screen_shot_path = playlog[2]
                popularity = playlog[3]
            anchor_name = ''
            room_url = ''
            roomInfo = app_map().getRoomInfoById(room_id, plat_id)
            if roomInfo:
                anchor_name = roomInfo["emcee"]
                room_url = roomInfo["source_link"]
            logtime = item[7].isoformat()
            income = str((item[8]).quantize(Decimal('0.00')))
            play_id = item[9]
            plat_id = item[10]
            agent_id = item[11]
            if income_type == '4':
                admplat = app_map().getAdmPlat(plat_id)
                if admplat:
                    income = str(
                        (item[8] * rate * Decimal(str(admplat[2] / 100))).quantize(Decimal('0.00')))

            if income_type == '2':
                income = str((item[8] * rate).quantize(Decimal('0.00')))

            agent_name = ''
            if income_type == '3':
                admAgent = app_map().getAdmAgent(agent_id)
                agent_name = admAgent[1] if admAgent else ''

            lst.append({"income_log_id": income_log_id,
                        "income_from": income_from,
                        "record_path": record_path,
                        "play_id": play_id,
                        "union_id": union_id,
                        "union_name": union_name,
                        "income": income,
                        "screen_shot_path": screen_shot_path,
                        "user_id": user_id,
                        "task_id": task_id,
                        "task_create_time": task_create_time,
                        "room_url": room_url,
                        "agent_name": agent_name,
                        "popularity": popularity,
                        "plat_name": plat_name,
                        "room_id": room_id,
                        "logtime": logtime,
                        "anchor_name": anchor_name})
        self.db_wealth.close()

        list_name = ''
        if income_type == '1' or income_type == '4':
            list_name = [
                '结算id',
                '平台',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']
        elif income_type == '2':
            list_name = [
                '结算工会id',
                '结算工会名称',
                '结算id',
                '平台',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']
        elif income_type == '3':
            list_name = [
                '结算id',
                '经纪公司名称',
                '主播名称',
                '用户id',
                'play_id',
                '人气',
                '任务id',
                '结算逻辑',
                '结算金额',
                '房间地址']

        els_url = exportIncome(lst, list_name, filename, income_type)
        self.write_json(0, data=els_url)
        return

    def findNeedIdsByPackId(self, package_id):
        sql_need = "SELECT need_id from  ads_need_info where package_id= {}".format(
            int(package_id))
        result = self.db_ads.execute(sql_need).fetchall()
        self.db_ads.close()
        a = list()
        for r in result:
            a.append(str(r[0]))
        a = ",".join(a)
        return a

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


class PlayRecordHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/playRecord/playRecord_list.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):

        limit, args = self.get_pages_args()

        sql = "SELECT p.play_id,p.user_id,t.room_id,p.popularity,p.popularity_from,p.income," \
              " p.record_path,p.screen_shot_path,p.verify_status,p.verify_result,p.logtime,p.create_time," \
              " p.status,p.need_id,p.begin_time,p.verify_user ,p.close_account,n.package_id," \
              " p.is_count_money,p.task_id ,t.plat_id from ads_task_play_log p LEFT JOIN ads_task t on p.task_id=t.task_id" \
              " LEFT JOIN ads_need_info n on p.need_id=n.need_id  where 1=1"

        filter = args["filter"]
        room_id = filter.get('room_id', None)
        user_id = filter.get('user_id', None)
        status = filter.get('status', None)
        verify_status = filter.get('verify_status', None)
        begintime = filter.get('begintime', None)
        verify_result = filter.get('verify_result', None)
        task_id = filter.get('task_id', None)
        # endtime = filter["endtime"]
        package_id = ''
        is_account = ''
        play_id = ''
        if "package_id" in filter:
            package_id = filter['package_id']
        if "is_account" in filter:
            is_account = filter['is_account']
        if "play_id" in filter:
            play_id = filter['play_id']

        if play_id:
            sql = sql + " and p.play_id like '%" + play_id.strip() + "%'"
        if user_id:
            sql = sql + " and p.user_id like '%" + user_id.strip() + "%'"
        if room_id:
            sql = sql + " and t.room_id like '%" + room_id.strip() + "%'"
        if verify_status:
            sql = sql + " and p.verify_status = '" + verify_status.strip() + "'"
        if verify_result:
            if (verify_result == '0' or verify_result == '-1'):
                sql = sql + " and p.verify_result = '" + verify_result.strip() + "'"
            else:
                sql = sql + " and p.verify_result != '0'"
                sql = sql + " and p.verify_result != '-1'"

        if begintime:
            sql = sql + " and p.create_time = '" + begintime.strip() + "'"

        if status:
            if status == '3':
                sql = sql + " and (p.status = 1 or p.status=2)"
            else:
                sql = sql + " and p.status = '" + status.strip() + "'"

        if is_account:
            sql = sql + " and p.close_account='" + is_account + "'"

        if package_id:
            sql = sql + " and n.package_id='" + package_id + "'"
        if task_id:
            sql = sql + " and p.task_id='" + task_id + "'"

        offset = " ORDER BY p.play_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        try:
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'play_id',
                'user_id',
                'room_id',
                'popularity',
                'popularity_from',
                'income',
                'record_path',
                'screen_shot_path',
                'verify_status',
                'verify_result',
                'logtime',
                'create_time',
                'status',
                'need_id',
                'begin_time',
                'verify_user',
                'close_account',
                'package_id',
                'is_count_money',
                'task_id',
                'plat_id']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                income = str(data[5].quantize(Decimal('0.00'))
                             ) if data[5] is not None else ""
                temp['income'] = income
                temp['logtime'] = temp['logtime'].isoformat()
                temp['create_time'] = temp['create_time'].isoformat()
                temp['begin_time'] = temp['begin_time'].isoformat()
                room_id = data[2]
                plat_id = data[20]
                source_link = ''
                roomInfo = app_map().getRoomInfoById(room_id, plat_id)
                if roomInfo:
                    source_link = roomInfo["source_link"]
                temp['source_link'] = source_link
                package_id = data[17]
                package = app_map().getPack(package_id)
                package_name = ''
                if package:
                    package_name = package[1]
                temp['package_name'] = package_name
                verify_user = data[15]
                user = app_map().getLoginUser(verify_user)
                if user:
                    verify_user = user.user_name
                temp['verify_user'] = verify_user
                lst.append(temp)

            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            self.write_json(-1, '查询失败')
            log.e(e)
        finally:
            self.db_ads.close()


class PlayRecordReadHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        type = ''
        date = ''
        if "type" in self.request.arguments:
            type = self.get_argument('type', None)
        if "date" in self.request.arguments:
            date = self.get_argument('date', None)

        package_list = self.db_ads.query(
            ContractPackInfo.package_id,
            ContractPackInfo.package_name). order_by(
            desc(
                ContractPackInfo.package_id)).all()

        self.db_ads.close()

        lst = list()
        for ptype in package_list:
            lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))

        self.render(
            "/ads_manager/playRecordRead/playRecord_list.mako",
            type=type,
            date=date,
            package_list=lst)


class PlayRecordIncomeHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        type = ''
        date = ''
        if "type" in self.request.arguments:
            type = self.get_argument('type', None)
        if "date" in self.request.arguments:
            date = self.get_argument('date', None)

        package_list = self.db_ads.query(
            ContractPackInfo.package_id,
            ContractPackInfo.package_name). order_by(
            desc(
                ContractPackInfo.package_id)).all()
        lst = list()
        self.db_ads.close()
        for ptype in package_list:
            lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))

        self.render(
            "/ads_manager/playRecord4income/playRecord_list.mako",
            type=type,
            date=date,
            package_list=lst)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        sql = "SELECT p.play_id,p.user_id,t.room_id,p.popularity,p.popularity_from,p.income," \
              " p.record_path,p.screen_shot_path,p.verify_status,p.verify_result,p.logtime,p.create_time," \
              " p.status,p.need_id,p.begin_time,p.verify_user ,p.close_account,n.package_id," \
              " p.is_count_money,p.task_id,i.status as pstatus,t.plat_id from ads_task_play_log p LEFT JOIN ads_task t on p.task_id=t.task_id" \
              " LEFT JOIN ads_need_info n on p.need_id=n.need_id  LEFT JOIN ads_contract_package_info i ON " \
              " i.package_id=n.package_id where 1=1"

        filter = args["filter"]
        room_id = filter.get('room_id', None)
        user_id = filter.get('user_id', None)
        status = filter.get('status', None)
        verify_status = filter.get('verify_status', None)
        begintime = filter.get('begintime', None)
        verify_result = filter.get('verify_result', None)
        task_id = filter.get('task_id', None)
        # endtime = filter["endtime"]
        package_id = ''
        is_account = ''
        play_id = ''
        if "package_id" in filter:
            package_id = filter['package_id']
        if "is_account" in filter:
            is_account = filter['is_account']
        if "play_id" in filter:
            play_id = filter['play_id']

        if play_id:
            sql = sql + " and p.play_id like '%" + play_id.strip() + "%'"
        if user_id:
            sql = sql + " and p.user_id like '%" + user_id.strip() + "%'"
        if room_id:
            sql = sql + " and t.room_id like '%" + room_id.strip() + "%'"
        if verify_status:
            sql = sql + " and p.verify_status = '" + verify_status.strip() + "'"
        if verify_result:
            if (verify_result == '0' or verify_result == '-1'):
                sql = sql + " and p.verify_result = '" + verify_result.strip() + "'"
            else:
                sql = sql + " and p.verify_result != '0'"
                sql = sql + " and p.verify_result != '-1'"

        if begintime:
            sql = sql + " and p.create_time = '" + begintime.strip() + "'"

        if status:
            if status == '3':
                sql = sql + " and (p.status = 1 or p.status=2)"
            else:
                sql = sql + " and p.status = '" + status.strip() + "'"

        if is_account:
            sql = sql + " and p.close_account='" + is_account + "'"

        if package_id:
            sql = sql + " and n.package_id='" + package_id + "'"
        if task_id:
            sql = sql + " and p.task_id='" + task_id + "'"

        offset = " ORDER BY p.play_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        try:
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'play_id',
                'user_id',
                'room_id',
                'popularity',
                'popularity_from',
                'income',
                'record_path',
                'screen_shot_path',
                'verify_status',
                'verify_result',
                'logtime',
                'create_time',
                'status',
                'need_id',
                'begin_time',
                'verify_user',
                'close_account',
                'package_id',
                'is_count_money',
                'task_id',
                'pstatus',
                'plat_id']
            lst = list()
            for data in datas:
                play_id = data[0]
                temp = dict(zip(head, data))
                # income = str(data[5].quantize(Decimal('0.00'))) if data[5] is not None else ""
                temp['income'] = self.find_account_log(play_id)
                temp['logtime'] = temp['logtime'].isoformat()
                temp['create_time'] = temp['create_time'].isoformat()
                temp['begin_time'] = temp['begin_time'].isoformat()
                room_id = data[2]
                plat_id = data[21]
                source_link = ''
                roomInfo = app_map().getRoomInfoById(room_id, plat_id)
                if roomInfo:
                    source_link = roomInfo["source_link"]
                temp['source_link'] = source_link
                package_id = data[17]
                package = app_map().getPack(package_id)
                package_name = ''
                if package:
                    package_name = package[1]
                temp['package_name'] = package_name
                verify_user = data[15]
                user = app_map().getLoginUser(verify_user)
                if user:
                    verify_user = user.user_name
                temp['verify_user'] = verify_user
                lst.append(temp)

            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            self.write_json(-1, '查询失败')
            log.e(e)
        finally:
            self.db_ads.close()

    # 查找結算日志
    def find_account_log(self, play_id):
        sql = 'select income from T_log_income_anchor where play_id={}'.format(
            play_id)
        results = []
        try:
            results = self.db_wealth.execute(sql).fetchall()
        except Exception as e:
            log.e(e)
        finally:
            self.db_wealth.close()
        income_lst = [str(ret[0]) for ret in results if ret[0]]
        income_log = '+'.join(income_lst) if income_lst else 0
        return income_log


class PlayRecordAuditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        id = args["id"]
        verify_result = args["verify_result"]
        user = self.get_current_user()
        v_data = self.db_ads.query(TaskPlayLog).filter(
            TaskPlayLog.play_id == id).first()
        v_data.verify_status = 1
        v_data.verify_result = verify_result
        v_data.verify_user = user["id"]

        oplog = AdsOpLog()
        oplog.op_type = 4
        oplog.op_user_id = user["id"]
        oplog.op_user_name = user["name"]
        oplog.op_desc = '审核播放记录 play_id:' + \
            str(id) + "  verify_result:" + str(verify_result)
        co = {"play_id": id, "verify_result": verify_result}
        oplog.op_content = str(co)
        oplog.createtime = datetime.datetime.now()
        self.db_adm.add(oplog)
        try:
            self.db_adm.commit()
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "审核失败")
        finally:
            self.db_adm.close()
            self.db_ads.close()


class PlayRecordEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        income = args["income"]
        play_id = args["play_id"]
        v_data = self.db_ads.query(TaskPlayLog).filter(
            TaskPlayLog.play_id == play_id).first()
        v_data.income = income

        oplog = AdsOpLog()
        oplog.op_type = 2
        user = self.get_current_user()
        oplog.op_user_id = user["id"]
        oplog.op_user_name = user["name"]
        oplog.op_desc = '修改播放金额 play_id:' + \
            str(play_id) + " income:" + str(income)
        co = {"play_id": play_id, "income": income}
        oplog.op_content = str(co)
        oplog.createtime = datetime.datetime.now()
        self.db_adm.add(oplog)
        try:
            self.db_adm.commit()
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "补贴操作失败")
        finally:
            self.db_adm.close()
            self.db_ads.close()


class NeedinfoBatchAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/need_info/needinfo_create.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        param = self.get_argument("param")
        ifrepait = self.get_argument("ifrepait")
        package_name = self.get_argument("package_name")
        if ifrepait == '1':
            pi = PackageInfo()
            pi.package_name = package_name
            pi.anchor_alloc_type = 2
            pi.comment = package_name
            pi.create_time = datetime.datetime.now()
            self.db_ads.add(pi)
            try:
                self.db_ads.commit()
                # self.db_ads.merge(pi)
            except Exception as e:
                self.db_ads.rollback()
                log.e(e)
                self.write_json(500, "添加失败")
                self.db_ads.close()
                return

        if param is not None:
            param = json.loads(param)
            self.db_ads.begin_nested()
            try:
                for p in param:
                    ads_id = p["ads_id"]
                    position = p["position"]
                    description = p["description"]
                    package_id = p["package_id"]
                    need_name = p["need_name"]
                    need_play_type = p["need_play_type"]
                    anchor_level = p["anchor_level"]
                    enable = p["enable"]
                    ads_interval = p["ads_interval"]

                    ngp = NeedGroupInfo()
                    ngp.group_name = need_name
                    ngp.comment = need_name
                    ngp.anchor_level = anchor_level
                    self.db_ads.add(ngp)
                    try:
                        self.db_ads.commit()
                    except Exception as e:
                        self.db_ads.rollback()
                        log.e(e)
                        self.write_json(500, "添加失败")
                        self.db_ads.close()
                        return

                    ni = NeedInfo()
                    ni.ads_id = ads_id
                    ni.position = position
                    ni.position_count = len(
                        position.split(",")) if position is not None else 0
                    ni.description = description
                    ni.package_id = package_id
                    ni.need_play_type = need_play_type
                    ni.need_name = need_name
                    ni.anchor_level = anchor_level
                    ni.ads_interval = ads_interval
                    # ni.ads_need_group_id=ngp.ads_need_group_id
                    ni.enable = enable
                    self.db_ads.add(ni)
                    try:
                        self.db_ads.commit()
                    except Exception as e:
                        self.db_ads.rollback()
                        log.e(e)
                        self.write_json(500, "添加失败")
                        self.db_ads.close()
                        return

                    if ifrepait == '1':
                        # self.db_ads.refresh(pi)
                        pnm = PackageNeedMap()
                        pnm.ads_package_id = pi.ads_package_id
                        pnm.ads_need_id = ni.need_id
                        pnm.description = ni.description
                        pnm.create_time = datetime.datetime.now()
                        self.db_ads.add(pnm)
                        try:
                            self.db_ads.commit()
                        except Exception as e:
                            self.db_ads.rollback()
                            self.db_ads.close()
                            log.e(e)
                            self.write_json(500, "添加失败")
                            return

                    gnm = GroupNeedMap()
                    gnm.ads_group_id = ngp.ads_need_group_id
                    gnm.ads_need_id = ni.need_id
                    gnm.description = need_name
                    gnm.create_time = datetime.datetime.now()
                    self.db_ads.add(gnm)

                    try:
                        self.db_ads.commit()
                    except Exception as e:
                        self.db_ads.rollback()
                        log.e(e)
                        self.write_json(500, "添加失败")
                        return
                self.db_ads.commit()
                self.db_ads.close()
            except Exception as e:
                self.db_ads.rollback()
                self.db_ads.close()
                log.e(e)
                self.write_json(500, "添加失败")
            self.write_json(0)
        else:
            self.write_json(-1, "没有需要添加的schedule数据")


class IncomeAnchorsettleHander(SwxJsonHandler):
    @permision
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument("args")
        if args is not None:
            args = json.loads(args)
        package_id = args["package_id"]
        type = ''
        if "type" in args:
            type = args["type"]
        result = self.db_ads.query(NeedInfo).filter(
            NeedInfo.package_id == package_id).all()
        # 查询所有平台 和经纪公司
        anchor_income = 0
        union_inmome = 0
        plat_inmome = 0
        agent_inmome = 0
        rate = Decimal(0)

        if result:
            rate = self.findRate4Package(package_id)
            rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))

            lst = list()
            for ret in result:
                lst.append(str(ret.need_id))
            lst = ",".join(lst)
            sql = "select income ,income_type,plat_id,agent_id from T_log_income_anchor where 1=1 and need_id in ({})".format(
                lst)
            result_income = self.db_wealth.execute(sql).fetchall()

            for ret in result_income:
                if ret[1] == 1:
                    anchor_income += ret[0]
                    # 如何agent_id ！=0 说明是经纪公司 不结算到平台
                    if not ret[3]:
                        plat = app_map().getAdmPlat(ret[2])
                        if plat:
                            plat_inmome += ret[0] * Decimal(str(plat[2] / 100))
                        else:
                            plat_inmome += ret[0]

                elif ret[1] == 2:
                    union_inmome += ret[0]
                    plat = app_map().getAdmPlat(ret[2])
                    if plat:
                        plat_inmome += ret[0] * Decimal(str(plat[2] / 100))
                    else:
                        plat_inmome += ret[0]

                elif ret[1] == 3:
                    agent_inmome += ret[0]

        v_data = self.db_ads.query(ContractPackInfo).filter(
            ContractPackInfo.package_id == package_id).first()
        v_data.anchor_balance = anchor_income
        v_data.union_balance = (union_inmome * rate).quantize(Decimal('0.00'))
        v_data.plat_balance = (plat_inmome * rate).quantize(Decimal('0.00'))
        v_data.agent_balance = agent_inmome
        if type == "1":
            v_data.status = 2
            v_data.log_time = datetime.datetime.now()
        v_data.balance_last_time = datetime.datetime.now()
        try:
            self.write_json(0)
            self.db_ads.commit()
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "结算失败")
            return
        finally:
            self.db_ads.close()
            self.db_wealth.close()

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


class IncomeAnchorsettle4closeHander(SwxJsonHandler):
    # @permision
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument("args")
        if args is not None:
            args = json.loads(args)
        package_id = args["package_id"]
        account_type = args["account_type"]
        # type = ''
        # if "type" in args:
        #     type = args["type"]
        result = self.db_ads.query(NeedInfo).filter(
            NeedInfo.package_id == package_id).all()
        # 查询所有平台 和经纪公司
        anchor_income = 0
        union_inmome = 0
        plat_inmome = 0
        agent_inmome = 0
        rate = Decimal(0)

        if result:
            rate = self.findRate4Package(package_id)
            rate = Decimal.from_float(rate / 100).quantize(Decimal('0.00'))

            lst = list()
            for ret in result:
                lst.append(str(ret.need_id))
            lst = ",".join(lst)
            sql = "select income ,income_type,plat_id,agent_id from " \
                  "T_log_income_anchor where income_from {} and need_id in ({})"
            if str(account_type) == '1':  # 关账结算
                sql = sql.format('!=4', lst)
            if str(account_type) == '2':  # 关账之后其他结算
                sql = sql.format('=4', lst)
            result_income = self.db_wealth.execute(sql).fetchall()

            for ret in result_income:
                income, income_type, plat_id, _ = ret
                if not plat_id:
                    continue
                if income_type == 1:
                    anchor_income += income
                    if not ret[3]:
                        plat = app_map().getAdmPlat(plat_id)
                        if plat:
                            plat_inmome += income * Decimal(str(plat[2] / 100))
                        else:
                            plat_inmome += income

                elif income_type == 2:
                    union_inmome += income
                    plat = app_map().getAdmPlat(plat_id)
                    if plat:
                        plat_inmome += income * Decimal(str(plat[2] / 100))
                    else:
                        plat_inmome += income

                elif income_type == 3:
                    agent_inmome += income

        v_data = self.db_ads.query(ContractPackInfo).filter(
            ContractPackInfo.package_id == package_id).first()
        if str(account_type) == '1':
            v_data.anchor_balance_close = anchor_income
            v_data.union_balance_close = (
                union_inmome *
                rate).quantize(
                Decimal('0.00'))
            v_data.plat_balance_close = (
                plat_inmome *
                rate).quantize(
                Decimal('0.00'))
            v_data.agent_balance_close = agent_inmome
        elif str(account_type) == '2':
            v_data.anchor_balance_other = anchor_income
            v_data.union_balance_other = (
                union_inmome *
                rate).quantize(
                Decimal('0.00'))
            v_data.plat_balance_other = (
                plat_inmome *
                rate).quantize(
                Decimal('0.00'))
            v_data.agent_balance_other = agent_inmome

        try:
            self.write_json(0)
            self.db_ads.commit()
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "结算失败")
        finally:
            self.db_ads.close()
            self.db_wealth.close()

    def findRate4Package(self, package_id):
        sql = 'select rate from ads_contract_package_info where package_id={}'.format(
            package_id)
        result = self.db_ads.execute(sql).scalar()
        self.db_ads.close()
        return result


# ---------------log查询---------------------------------
class LogSelectInfoListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("/ads_manager/logselect_info/logselect_list.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]
        op_type = ''
        op_user_name = ''
        start_time = ''
        end_time = ''
        if "level" in filter.keys():
            op_type = filter["level"]
            op_user_name = filter["user_id"]
            start_time = filter["start_time"]
            end_time = filter["end_time"]
        try:
            query = self.db_adm.query(AdsOpLog)
            data_now = datetime.datetime.now().strftime('%Y-%m-%d')
            if op_type:
                query = query.filter(AdsOpLog.op_type == op_type)
            if op_user_name:
                op_user_name = '%' + op_user_name + '%'
                query = query.filter(AdsOpLog.op_user_name.like(op_user_name))
            if start_time and end_time is None:
                query = query.filter(
                    and_(
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') <= data_now,
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') >= start_time))
            if end_time and start_time is None:
                query = query.filter(
                    and_(
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') >= data_now))
            if start_time and end_time:
                query = query.filter(
                    and_(
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') <= end_time,
                        func.date_format(
                            AdsOpLog.createtime,
                            '%Y-%m-%d') >= start_time))

            total = query.count()
            query = query.order_by(AdsOpLog.op_id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))

            query_result = query.all()

            lst = list()
            for item in query_result:
                lst.append({
                    'op_id': item.op_id or 0,
                    'op_type': item.op_type or 0,
                    'op_user_id': item.op_user_id or 0,
                    'op_user_name': item.op_user_name or '',
                    'op_desc': item.op_desc or '',
                    'op_content': item.op_content,
                    'create_time': item.createtime.isoformat() or '',
                })

            ret = self.set_page_params(total, limit, lst)
            for info_data in ret['data']:
                if info_data['op_type'] == 1:
                    info_data['op_name'] = '撤回广告'
                if info_data['op_type'] == 2:
                    info_data['op_name'] = '补贴金额'
                if info_data['op_type'] == 3:
                    info_data['op_name'] = '提现修改'
                if info_data['op_type'] == 4:
                    info_data['op_name'] = '审核记录'
                if info_data['op_type'] == 5:
                    info_data['op_name'] = '广告投放'
                if info_data['op_type'] == 6:
                    info_data['op_name'] = '自动化审核'
                if info_data['op_type'] == 7:
                    info_data['op_name'] = '申诉'
                if info_data['op_type'] == 8:
                    info_data['op_name'] = '数据同步'
                if info_data['op_type'] == 9:
                    info_data['op_name'] = '修改ads_task_play_log'
                if info_data['op_type'] == 10:
                    info_data['op_name'] = '增加用户余额'

            # for item in app_map().TLogWithdrawAnchor():
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(500, "LogSelectInfoListHander查询失败")
        finally:
            self.db_adm.close()


class LogSelectInfoListHander_content(SwxJsonHandler):
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        datas = self.db_adm.query(
            AdsOpLog.op_content).filter(
            AdsOpLog.op_id == id).first()
        lst = {}
        list_s = []
        if datas:
            op_content = datas[0]
            # op_content = json.dumps(op_content)
            op_content = re.sub('\'', '\"', op_content)
            print(op_content)
            op_cc = json.loads(op_content)

            for item in op_cc.keys():
                list_s.append(item)
            if op_content:
                lst['id_id'] = op_cc[str(list_s[0])]
                lst['id_name'] = str(list_s[0])
                lst['apply_state'] = str(op_cc[str(list_s[1])])
                lst['apply_name'] = str(list_s[1])
            else:
                self.write_json(-1, '没有对应的描述')
                self.db_adm.close()
                return
        else:
            self.write_json(-1, '没有对应的套餐数据')
            self.db_adm.close()
            return
        self.write_json(0, '', lst)
        self.db_adm.close()


class Paltform4AllList(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        _, unionList = app_map().get_platform_map_list()
        self.write_raw_json(unionList)


class UnionList4AllList(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        unionlist = app_map().getUnionList()
        self.write_raw_json(unionlist)


class FulshDateHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        try:
            response1 = request.urlopen(
                r"http://120.92.116.187:12001/base_data/flush?access_token=bfb19b31c3a3f74c92c0cea48db05fda5ffd9088")
            if response1 is not None:
                ret = response1.read().decode('utf-8')
                data = json.loads(ret)
                if data["Code"] == 0:
                    response2 = request.urlopen(
                        r"http://120.92.116.187:12001/plan_info/flush?access_token=bfb19b31c3a3f74c92c0cea48db05fda5ffd9088")
                    if response2 is not None:
                        ret = response2.read().decode('utf-8')
                        data2 = json.loads(ret)
                        if data2["Code"] == 0:
                            self.write_json(0)
                        else:
                            self.write_json(-1, '刷新失败')
                else:
                    self.write_json(-1, "刷新失败")
            else:
                self.write_json(-1, "刷新失败")
        except Exception as e:
            log.e(e)
            self.write_json(-1, "刷新失败")


class CreditUpdateHandler(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        credit_time = self.get_argument("credit_time", None)
        auto_id = self.get_argument("auto_id", None)
        try:
            data = json.dumps({"playLogCreatedDate": credit_time}).encode(
                encoding='utf-8')
            req = request.Request(
                url="http://xhlgw.xiaohulu.com:50000/api/v1/credit/admin/fresh_play_ads_result",
                data=data)
            res = request.urlopen(req)
            if res is not None:
                ret = res.read().decode('utf-8')
                data = json.loads(ret)
                if data["code"] == 0:
                    self.db_adm.query(PlayLogAuto).filter(
                        PlayLogAuto.auto_id == auto_id).update({PlayLogAuto.score_status: 1})
                    self.db_adm.commit()
                    self.db_adm.close()
                    self.write_json(0)
                else:
                    self.write_json(-1, '请重试，或联系管理员')
        except Exception as e:
            log.e(e)
            self.write_json(-1, '请重试，或联系管理员')


class PlayRecordImportHanderAll(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        upload_path = os.path.join(
            os.path.dirname(__file__) + '/../../..',
            'UploadFiles')  # 文件的暂存路径

        file_metas = self.request.files['infile']  # 提取表单中‘name’为‘infile’的文件元数据
        playnum = self.get_argument("playnum", None)
        data_now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # 根据公会名，查询公会的id
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        for meta in file_metas:
            filename = data_now_str + '_' + meta['filename']
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        # 读取文件
        workbook = xlrd.open_workbook(filepath)
        # os.remove(os.path.join(upload_path, filename))
        # 拿到表名
        sheets = workbook.sheet_names()
        # 第一个表
        worksheet = workbook.sheet_by_name(sheets[0])
        # 行数
        nrows = worksheet.nrows
        if nrows <= 1:
            self.write_json(0, '上传表格错误(表格不能为空表且数据从第二行开始)')
            return

        lst = list()

        for i in range(1, worksheet.nrows):
            if worksheet.ncols != 25:
                lst.append("第" + str(i) + "行数据列数不对\n")
            if worksheet.cell(
                    i, 12).value != 'None' and worksheet.cell(
                    i, 12).value != '':
                if not self.isNum(worksheet.cell(i, 12).value):
                    lst.append("第" + str(i + 1) + "行 第M列 数据格式不对")
            if worksheet.cell(
                    i, 14).value != 'None' and worksheet.cell(
                    i, 14).value != '':
                if not self.isNum(worksheet.cell(i, 14).value):
                    lst.append("第" + str(i + 1) + "行 第O列 数据格式不对")
            if worksheet.cell(
                    i, 15).value != 'None' and worksheet.cell(
                    i, 15).value != '':
                if not self.isNum(worksheet.cell(i, 15).value):
                    lst.append("第" + str(i + 1) + "行 第P列 数据格式不对")
            if worksheet.cell(
                    i, 16).value != 'None' and worksheet.cell(
                    i, 16).value != '':
                if not self.isNum(worksheet.cell(i, 16).value):
                    lst.append("第" + str(i + 1) + "行 第Q列 数据格式不对")
            if worksheet.cell(
                    i, 22).value != 'None' and worksheet.cell(
                    i, 22).value != '':
                if not self.isNum(worksheet.cell(i, 22).value):
                    lst.append("第" + str(i + 1) + "行 第W列 数据格式不对")

        if lst:
            error = ','.join(lst)
            self.write_json(-1, error)
            return error

        try:
            yield self.importExcelData(nrows, playnum, worksheet, filename)
            self.write_json(0, '上传成功')
        except Exception as e:
            self.db_ads.rollback()
            log.e('ads_task_play_log excel import error:{}'.format(e))
            self.write_json(-1, 'excel数据格式错误,error:{}'.format(e))
            return
        finally:
            self.db_ads.close()

    def isNum(self, value):
        try:
            float(value)
        except Exception:
            return False
        else:
            return True

    @run_on_executor
    def importExcelData(self, nrows, playnum, worksheet, filename):
        user = self.get_current_user()
        for i in range(1, worksheet.nrows):
            # 更新当前进度
            app_playlog[int(playnum)] = {"now": i, "max": nrows}
            # time.sleep(3)
            temp = dict()
            temp['popularity'] = int(
                worksheet.cell(
                    i,
                    12).value) if worksheet.cell(
                i,
                12).value != 'None' and worksheet.cell(
                i,
                12).value != '' else 0
            temp['play_id'] = int(
                worksheet.cell(
                    i,
                    14).value) if worksheet.cell(
                i,
                14).value != 'None' and worksheet.cell(
                i,
                14).value != '' else 0
            temp['income'] = '{:g}'.format(
                float(
                    worksheet.cell(
                        i,
                        15).value)) if worksheet.cell(
                i,
                15).value != 'None' and worksheet.cell(
                    i,
                15).value != '' else 0
            temp['verify_result'] = int(
                worksheet.cell(
                    i,
                    16).value) if worksheet.cell(
                i,
                16).value != 'None' and worksheet.cell(
                i,
                16).value != '' else 0
            temp['is_count_money'] = int(
                worksheet.cell(
                    i,
                    22).value) if worksheet.cell(
                i,
                22).value != 'None' and worksheet.cell(
                i,
                22).value != '' else 0
            query = self.db_ads.query(TaskPlayLog).filter(
                and_(
                    TaskPlayLog.popularity == temp['popularity'],
                    TaskPlayLog.income == temp['income'],
                    TaskPlayLog.verify_result == temp['verify_result'],
                    TaskPlayLog.play_id == temp['play_id'],
                    TaskPlayLog.is_count_money == temp['is_count_money'])).all()
            if query:
                log.v('该次重复,play_id:' + str(temp['play_id']) + '\n')
            else:

                v_data = self.db_ads.query(TaskPlayLog).filter(
                    TaskPlayLog.play_id == temp['play_id']).first()
                if v_data:
                    v_data.popularity = temp['popularity']
                    v_data.income = temp['income']
                    v_data.verify_result = temp['verify_result']
                    v_data.verify_user = user["id"]
                    v_data.is_count_money = temp["is_count_money"]
                    if v_data.coin_exchange_rate and temp['income']:
                        v_data.coin_count=(v_data.coin_exchange_rate * Decimal(temp['income'])).quantize(Decimal('0.00'))


        oplog = AdsOpLog()
        oplog.op_type = 4
        oplog.op_user_id = user["id"]
        oplog.op_user_name = user["name"]
        oplog.op_desc = 'ads_task_play_log excel导入 文件:' + str(filename)
        co = {
            "user_id": user["id"],
            "datetime": datetime.datetime.now(),
            "filename": filename}
        oplog.op_content = str(co)
        oplog.createtime = datetime.datetime.now()
        self.db_adm.add(oplog)

        try:
            self.db_adm.commit()
            self.db_ads.commit()
        except Exception as e:
            self.db_adm.rollback()
            self.db_ads.rollback()
            log.e(e)
        finally:
            self.db_adm.close()
            self.db_ads.close()


class PlayRecordExportHander(SwxJsonHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        sql = "SELECT k.task_create_time,t.task_id,n.anchor_level,t.user_id,k.plat_id,k.room_id," \
              "t.begin_time,t.postion_id,t.ads_id,t.popularity,k.estmate_income,t.play_id,t.income,t.verify_result,t.verify_status," \
              "t.record_path,t.screen_shot_path,p.package_name,t.is_new_user,t.is_count_money,t.record_path_old,t.screen_shot_path_old FROM ads_task_play_log t LEFT JOIN ads_task k" \
              " ON t.task_id = k.task_id LEFT JOIN ads_need_info n ON n.need_id = t.need_id LEFT JOIN ads_contract_package_info p on" \
              " p.package_id=n.package_id  WHERE t.`status` !=0"

        room_id = self.get_argument("room_id", None)
        user_id = self.get_argument("user_id", None)
        task_id = self.get_argument("task_id", None)
        status = self.get_argument("status", None)
        verify_status = self.get_argument("verify_status", None)
        verify_result = self.get_argument("verify_result", None)
        begintime = self.get_argument("begin_time", None)
        playnum = self.get_argument("playnum", None)
        package_id = ''
        is_account = ''
        play_id = ''
        if "package_id" in self.request.arguments:
            package_id = self.get_argument("package_id", None)
        if "is_account" in self.request.arguments:
            is_account = self.get_argument("is_account", None)
        if "play_id" in self.request.arguments:
            play_id = self.get_argument("play_id", None)

        filename = '_播放记录'
        if play_id:
            sql = sql + " and t.play_id like '%" + play_id.strip() + "%'"
        if user_id:
            sql = sql + " and t.user_id like '%" + user_id.strip() + "%'"
        if room_id:
            sql = sql + " and k.room_id like '%" + room_id.strip() + "%'"
            filename += '_房间id:' + str(room_id)
        if verify_status:
            sql = sql + " and t.verify_status = '" + verify_status.strip() + "'"
            filename += '_审核状态' + verify_status

        if verify_result:
            filename += '_结果' + verify_result
            if (verify_result == '0' or verify_result == '-1'):
                sql = sql + " and t.verify_result = '" + verify_result.strip() + "'"
            else:
                sql = sql + " and t.verify_result != '0'"
                sql = sql + " and t.verify_result != '-1'"

        if begintime:
            sql = sql + " and t.create_time = '" + begintime.strip() + "'"
            filename += '_任务创建时间' + begintime

        if status:
            if status == '3':
                sql = sql + " and (t.status = 1 or t.status=2)"
            else:
                sql = sql + " and t.status = '" + status.strip() + "'"

        if package_id:
            sql = sql + " and n.package_id = '" + package_id + "'"
        if is_account:
            sql = sql + " and t.close_account = '" + is_account + "'"
        if task_id:
            sql = sql + " and t.task_id = '" + task_id + "'"

        offset = " ORDER BY t.play_id DESC"
        datas = self.db_ads.execute(sql + offset).fetchall()
        self.db_ads.close()
        els_url = yield self.export_playlog(datas, filename, playnum)
        self.write_json(0, data=els_url)
        return

    @run_on_executor
    def export_playlog(self, datas, filename, playnum):
        list_name = [
            '任务日期',
            '任务id',
            '任务级别',
            '主播级别',
            '用户id',
            'plat_id',
            'room_id',
            'source_link',
            '播放时间',
            '播放版位',
            '播放素材id',
            '30天平均最高人气',
            '实时人气',
            '任务预计收入',
            '播放id',
            '播放收入（运营审核修改项）',
            '识别结果0为成功其他为失败（运营审核修改项）',
            '是否已自动化审核(0:未审核,1:已审核)',
            '视频地址',
            '截图目录',
            '套餐名称',
            '是否为新人',
            '是否结算(0:不结算，1:结算)',
            '旧视频',
            '旧截图']
        return exportPlayRecord(datas, list_name, filename, playnum)


class PlayLogExportSelectHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        playnum = self.get_argument("playnum", None)
        if playnum is None:
            self.write_json(-1, 'playlog进度序列号不能为空')
            return
        if int(playnum) not in app_playlogExport:
            app_playlogExport[int(playnum)] = {"now": 0, "max": 0}
        self.write_json(0, '', app_playlogExport[int(playnum)])


class PlayLogExportCreateHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        date_now = int(time.time())
        app_playlogExport[date_now] = {"now": 0, "max": 0}
        self.write_json(0, '', date_now)


class PlayLogImportSelectHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        playnum = self.get_argument("playnum", None)
        if playnum is None:
            self.write_json(-1, 'playlog进度序列号不能为空')
            return
        if int(playnum) not in app_playlog:
            app_playlog[int(playnum)] = {"now": 0, "max": 0}
        self.write_json(0, '', app_playlog[int(playnum)])


class PlayLogImportCreateHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        date_now = int(time.time())
        app_playlog[date_now] = {"now": 0, "max": 0}
        self.write_json(0, '', date_now)


# ---------------任务查询---------------------------------
class TaskSelectListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):

        self.render("/ads_manager/task_select_info/task_select_list.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        #
        filter = args["filter"]
        level = ''
        schedule_id = ''
        task_result = ''
        package_id = ''

        date = ''
        user_id = ''
        plat_id = ''
        room_id = ''
        task_id = ''
        if "level" in filter.keys():
            level = filter["level"]
            schedule_id = filter["schedule_id"]
            task_result = filter["task_result"]
            package_id = filter["package_id"]
            # task_status = filter["task_status"]
            date = filter["date"]
            user_id = filter["user_id"]
            # plat_id = filter["platform_id"]
            room_id = filter["room_id"]
            task_id = filter["task_id"]
        try:
            query = self.db_entourage.query(
                AdsTask,
                func.count(
                    TaskPlayLog.play_id),
                func.sum(
                    case(
                        [
                            (TaskPlayLog.status == 2,
                             1)],
                        else_=0)),
                NeedGroupInfo.anchor_level,
                RoomInfo.source_link,
                RoomInfo.emcee).join(
                TaskPlayLog,
                AdsTask.task_id == TaskPlayLog.task_id).join(
                NeedGroupInfo,
                NeedGroupInfo.ads_need_group_id == AdsTask.group_id).join(
                RoomInfo,
                and_(
                    RoomInfo.platform_id == AdsTask.plat_id,
                    RoomInfo.room_id == AdsTask.room_id)).group_by(
                AdsTask,
                RoomInfo.source_link,
                RoomInfo.emcee)
            # data_now = datetime.datetime.now().strftime('%Y-%m-%d')

            if package_id:
                query = query.join(
                    GroupNeedMap, AdsTask.group_id == GroupNeedMap.ads_group_id).join(
                    NeedInfo, NeedInfo.need_id == GroupNeedMap.ads_need_id).filter(
                    NeedInfo.package_id == package_id)

            if schedule_id:
                query = query.filter(AdsTask.schedule_id == schedule_id)
            if task_id:
                query = query.filter(AdsTask.task_id == task_id)
            if task_result:
                if task_result == '0':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == -1,
                            AdsTask.task_status == 0))
                elif task_result == '1':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == -1,
                            AdsTask.task_status == 1))
                elif task_result == '2':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 0,
                            AdsTask.task_status == 5))
                elif task_result == '3':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 1,
                            AdsTask.task_status == 5))
                elif task_result == '4':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 3,
                            AdsTask.task_status == 5))
            if date:
                query = query.filter(AdsTask.create_time == date)

            # else:
            #     query = query.filter(AdsTask.create_time == data_now)
            if user_id:
                query = query.filter(AdsTask.user_id == user_id)
            if level:
                query = query.filter(NeedGroupInfo.anchor_level == level)
            if room_id:
                query = query.filter(AdsTask.room_id == room_id)
            # if plat_id == '' and room_id:
            #     query = query.filter(AdsTask.room_id == room_id)

            query = query.order_by(AdsTask.task_id.desc())
            total = query.count()
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            lst = list()
            for item in query_result:
                platfrom_name = self.db_guild.query(
                    BasePlatformsGuild.name).filter(
                    BasePlatformsGuild.id == item[0].plat_id).first()
                lst.append({
                    'task_id': item[0].task_id or 0,
                    'user_id': item[0].user_id or 0,
                    'plat_id': item[0].plat_id or 0,
                    'room_id': item[0].room_id or '',
                    'task_result': item[0].task_result or 0,
                    'task_status': item[0].task_status or 0,
                    'schedule_id': item[0].schedule_id or 0,
                    'estmate_income': str(item[0].estmate_income) or '',
                    'task_create_time': item[0].task_create_time.isoformat() or '',
                    'stream_start_time': str(item[0].stream_start_time or ''),
                    'create_time': str(item[0].create_time) or '',
                    'task_play_log': str(item[1]) or '',
                    'task_play_log_end': str(item[2]) or '',
                    'anchor_level': str(item[3]) or '',
                    'source_link': str(item[4]) or '',
                    'emcee': str(item[5]) or '',
                    'platfrom_name': str(platfrom_name[0]) or '',
                })
            ret = self.set_page_params(total, limit, lst)
            for info_data in ret['data']:
                if info_data['task_result'] == - \
                        1 and info_data['task_status'] == 0:
                    info_data['task_name'] = '未开始'
                elif info_data['task_result'] == -1 and info_data['task_status'] == 1:
                    info_data['task_name'] = '进行中'
                elif info_data['task_result'] == 0 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已完成'
                elif info_data['task_result'] == 1 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已放弃'
                elif info_data['task_result'] == 3 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已过期'

                info_data['play_log'] = str(
                    info_data['task_play_log_end']) + '/' + str(info_data['task_play_log'])

                # if info_data['task_status'] != 1 and info_data['task_status'] != 5:
                #     info_data['task_status_name'] = '未开始'
                #     info_data['task_name'] = '未知'
                # elif info_data['task_status'] == 1:
                #     info_data['task_status_name'] = '正在进行'
                # elif info_data['task_status'] == 5:
                #     info_data['task_status_name'] = '已结束'
            # for item in app_map().TLogWithdrawAnchor():
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(500, "TaskSelectListHander查询失败")
        finally:
            self.db_entourage.close()
            self.db_guild.close()


#
class TaskSelectUpdateHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # limit, args = self.get_pages_args()
        #
        # filter = args["filter"]
        # level = ''
        # schedule_id = ''
        # task_result = ''
        # package_id = ''
        #
        # date = ''
        # user_id = ''
        # plat_id = ''
        # room_id = ''

        level = self.get_argument("level", None)
        schedule_id = self.get_argument("schedule_id", None)
        task_result = self.get_argument("task_result", None)
        package_id = self.get_argument("package_id", None)
        date = self.get_argument("date", None)
        user_id = self.get_argument("user_id", None)
        room_id = self.get_argument("room_id", None)
        task_id = self.get_argument("task_id", None)

        try:
            query = self.db_entourage.query(
                AdsTask,
                func.count(
                    TaskPlayLog.play_id),
                func.sum(
                    case(
                        [
                            (TaskPlayLog.status == 2,
                             1)],
                        else_=0)),
                NeedGroupInfo.anchor_level,
                RoomInfo.source_link,
                RoomInfo.emcee,
                RoomInfo.max_user_pre_count).join(
                TaskPlayLog,
                AdsTask.task_id == TaskPlayLog.task_id).join(
                NeedGroupInfo,
                NeedGroupInfo.ads_need_group_id == AdsTask.group_id).join(
                RoomInfo,
                and_(
                    RoomInfo.platform_id == AdsTask.plat_id,
                    RoomInfo.room_id == AdsTask.room_id)).group_by(
                AdsTask,
                RoomInfo.source_link,
                RoomInfo.emcee,
                RoomInfo.max_user_pre_count)
            # data_now = datetime.datetime.now().strftime('%Y-%m-%d')

            if package_id and package_id != '':
                query = query.join(
                    GroupNeedMap, AdsTask.group_id == GroupNeedMap.ads_group_id).join(
                    NeedInfo, NeedInfo.need_id == GroupNeedMap.ads_need_id).filter(
                    NeedInfo.package_id == package_id)

            if schedule_id and schedule_id != '':
                query = query.filter(AdsTask.schedule_id == schedule_id)
            if task_id and task_id != '':
                query = query.filter(AdsTask.task_id == task_id)
            if task_result and task_result != '':
                if task_result == '0':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == -1,
                            AdsTask.task_status == 0))
                elif task_result == '1':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == -1,
                            AdsTask.task_status == 1))
                elif task_result == '2':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 0,
                            AdsTask.task_status == 5))
                elif task_result == '3':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 1,
                            AdsTask.task_status == 5))
                elif task_result == '4':
                    query = query.filter(
                        and_(
                            AdsTask.task_result == 3,
                            AdsTask.task_status == 5))
            if date and date != '':
                query = query.filter(AdsTask.create_time == date)

            # else:
            #     query = query.filter(AdsTask.create_time == data_now)
            if user_id and user_id != '':
                query = query.filter(AdsTask.user_id == user_id)
            if level and level != '':
                query = query.filter(NeedGroupInfo.anchor_level == level)
            if room_id and room_id != '':
                query = query.filter(AdsTask.room_id == room_id)
            # if plat_id == '' and room_id:
            #     query = query.filter(AdsTask.room_id == room_id)

            query = query.order_by(AdsTask.task_id.desc())

            query_result = query.all()
            lst = list()
            for item in query_result:
                platfrom_name = self.db_guild.query(
                    BasePlatformsGuild.name).filter(
                    BasePlatformsGuild.id == item[0].plat_id).first()
                lst.append({
                    'task_id': item[0].task_id or 0,
                    'user_id': item[0].user_id or 0,
                    'plat_id': item[0].plat_id or 0,
                    'room_id': item[0].room_id or '',
                    'task_result': item[0].task_result or 0,
                    'task_status': item[0].task_status or 0,
                    'schedule_id': item[0].schedule_id or 0,
                    'estmate_income': str(item[0].estmate_income) or '',
                    'task_create_time': item[0].task_create_time.isoformat() or '',
                    'stream_start_time': str(item[0].stream_start_time or ''),
                    'create_time': str(item[0].create_time) or '',
                    'task_play_log': str(item[1]) or '',
                    'task_play_log_end': str(item[2]) or '',
                    'anchor_level': str(item[3]) or '',
                    'source_link': str(item[4]) or '',
                    'emcee': str(item[5]) or '',
                    'max_user_pre_count': str(item[6]) or '',
                    'platfrom_name': str(platfrom_name[0]) or '',
                })
            ret = lst

            for info_data in ret:

                if info_data['task_result'] == - \
                        1 and info_data['task_status'] == 0:
                    info_data['task_name'] = '未开始'
                elif info_data['task_result'] == -1 and info_data['task_status'] == 1:
                    info_data['task_name'] = '进行中'
                elif info_data['task_result'] == 0 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已完成'
                elif info_data['task_result'] == 1 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已放弃'
                elif info_data['task_result'] == 3 and info_data['task_status'] == 5:
                    info_data['task_name'] = '已过期'
                else:
                    info_data['task_name'] = ''

                info_data['play_log'] = str(
                    info_data['task_play_log_end']) + '/' + str(info_data['task_play_log'])

            list_name = [
                '任务ID',
                '用户ID',
                '主播级别',
                'schedule_id',
                '平台ID',
                '平台名称',
                '昵称',
                '房间ID',
                '任务状态',
                '完成程度',
                '预计收入',
                '任务接受时间',
                '开始推流时间',
                '预计收入',
                '30天平均人气']
            els_url = export_task_list_update(ret, list_name, list_name)
            self.write_json(0, data=els_url)

        except Exception as e:
            log.e(e)
            self.write_json(500, "TaskSelectListHander导出失败")
        finally:
            self.db_entourage.close()
            self.db_guild.close()


class SeleteTaskplaylogList(SwxJsonHandler):
    def get(self, *args, **kwargs):
        task_id = self.get_argument("task_id", None)
        #
        try:
            lst = []
            query_schedule = ''
            query = ''
            verify_status_name = ''
            verify_result_name = ''
            status_name = ''
            if task_id:
                query = self.db_entourage.query(TaskPlayLog).filter(
                    TaskPlayLog.task_id == task_id).order_by(
                    TaskPlayLog.play_id.desc())

                query_schedule = query.all()
                # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
                if query_schedule:
                    for ptype in query_schedule:

                        if ptype.verify_status == 0:
                            verify_status_name = '未审核'
                        elif ptype.verify_status == 1:
                            verify_status_name = '已审核'

                        if ptype.verify_result == -1:
                            verify_result_name = '初始状态'
                        elif ptype.verify_result == 0:
                            verify_result_name = '成功'
                        elif ptype.verify_result == 1:
                            verify_result_name = '没有找到截图'
                        else:
                            verify_result_name = '失败'

                        if ptype.status == 0:
                            status_name = '未播放'
                        elif ptype.status == 1:
                            status_name = '开始播放'
                        elif ptype.status == 2:
                            status_name = '结束播放'

                        lst.append({
                            'play_id': ptype.play_id or '',
                            'user_id': ptype.user_id or 0,
                            'status': status_name,
                            'income': float(ptype.income),
                            'popularity': ptype.popularity or 0,
                            'screen_shot_path': str(ptype.screen_shot_path) or '',
                            'record_path': str(ptype.record_path) or '',
                            'verify_status': verify_status_name,
                            'verify_result': verify_result_name,
                            'log_create_time': ptype.log_create_time.isoformat() or '',
                        })
                    self.write_json(0, '', lst)
                    self.db_entourage.close()
                else:
                    self.write_json(-1, '没有对应的task_play_log', lst)
                    # self.write_json(0, data=ret)
                    self.db_entourage.close()
        except Exception as e:
            self.db_entourage.rollback()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            self.db_entourage.close()

        self.db_entourage.close()


class SeleteTaskPlatList(SwxJsonHandler):
    def get(self, *args, **kwargs):

        try:
            lst = []
            query = self.db_guild.query(
                BasePlatformsGuild.id,
                BasePlatformsGuild.name).order_by(
                BasePlatformsGuild.id)
            query_schedule = query.all()
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
            for ptype in query_schedule:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_guild.close()
        except Exception as e:
            self.db_guild.rollback()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            # self.db_entourage.close()
            self.db_guild.close()


class SeleteTaskPackageList(SwxJsonHandler):
    def get(self, *args, **kwargs):
        try:
            lst = []
            query = self.db_ads.query(
                ContractPackInfo.package_id,
                ContractPackInfo.package_name).order_by(
                ContractPackInfo.package_id.desc())
            query_package = query.all()
            # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
            for ptype in query_package:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            # self.db_entourage.close()
            self.db_ads.close()


# ---------------提现用户详情---------------------------------
class IdentityPersonalListHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render(
            "/ads_manager/identity_personal_info/identity_personal_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]

        id_user_name = ''
        hold_user_name = ''
        bank_name = ''
        verify_status = ''
        identity_status = ''
        id_user = ''
        date = ''
        if "date" in filter.keys():
            id_user_name = filter["id_user_name"]
            hold_user_name = filter["hold_user_name"]
            bank_name = filter["bank_name"]
            verify_status = filter["verify_status"]
            id_user = filter["id_user"]
            identity_status = filter["identity_status"]
            date = filter["date"]
        try:
            query = self.db_wealth.query(TIdentityPersonal)
            # data_now = datetime.datetime.now().strftime('%Y-%m-%d')
            if date:
                query = query.filter(
                    func.date_format(
                        TIdentityPersonal.logtime,
                        '%Y-%m-%d') == date)
            if id_user_name:
                id_user_name = '%' + id_user_name + '%'
                query = query.filter(
                    TIdentityPersonal.id_user_name.like(id_user_name))
            if id_user:
                query = query.filter(TIdentityPersonal.user_id == id_user)
            if hold_user_name:
                hold_user_name = '%' + hold_user_name + '%'
                query = query.filter(
                    TIdentityPersonal.hold_user_name.like(hold_user_name))
            if bank_name:
                bank_name = '%' + bank_name + '%'
                query = query.filter(
                    TIdentityPersonal.bank_name.like(bank_name))
            if verify_status:
                if verify_status == '1':
                    query = query.filter(TIdentityPersonal.verify_status == 1)
                elif verify_status == '2':
                    query = query.filter(TIdentityPersonal.verify_status != 1)

            if identity_status:
                if identity_status == '1':
                    query = query.filter(TIdentityPersonal.status == 1)
                elif identity_status == '0':
                    query = query.filter(TIdentityPersonal.status == 0)

            query = query.order_by(TIdentityPersonal.identity_id.desc())
            total = query.count()
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            lst = list()

            for item in query_result:
                lst.append({
                    'identity_id': item.identity_id or 0,
                    'user_id': item.user_id or 0,
                    'verify_status': item.verify_status or '',
                    'status': item.status or '',
                    'id_user_name': item.id_user_name or '',
                    'id_number': item.id_number or '',
                    'bank_name': item.bank_name or '',
                    'bank_card_number': item.bank_card_number or '',
                    'hold_user_name': item.hold_user_name or '',
                    'bank_sub_name': str(item.bank_sub_name) or '',
                    'id_img_front': item.id_img_front or '',
                    'qq_number': item.qq_number or '',
                    'id_img_back': item.id_img_back or '',
                    'logtime': item.logtime.isoformat() or '',
                })

            ret = self.set_page_params(total, limit, lst)
            for info_data in ret['data']:
                if info_data['verify_status'] == 1:
                    info_data['verify_status_name'] = '已审核'
                else:
                    info_data['verify_status_name'] = '未审核'

                if info_data['status'] == 1:
                    info_data['status_name'] = '正常'
                elif info_data['status'] == 2:
                    info_data['status_name'] = '删除'

            self.write_json(0, data=ret)
            self.db_wealth.close()
        except Exception as e:
            self.db_wealth.close()
            log.e(e)
            self.write_json(500, "IdentityPersonalListHander查询失败")
        finally:
            self.db_wealth.close()
            # self.db_wealth.close()


class IdentityPersonalEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @run_on_executor
    def post(self, *args, **kwargs):
        try:
            identity_id = self.get_argument('identity_id', '')
            id_user_name = self.get_argument('id_user_name', '')
            id_number = self.get_argument('id_number', '')
            bank_name = self.get_argument('bank_name', '')
            bank_card_number = self.get_argument('bank_card_number', '')
            hold_user_name = self.get_argument('hold_user_name', '')
            bank_sub_name = self.get_argument('bank_sub_name', '')
            qq_number = self.get_argument('qq_number', '')
            query = self.db_wealth.query(TIdentityPersonal)
            if query:
                query_list = query.filter(TIdentityPersonal.identity_id == identity_id).update({
                    TIdentityPersonal.id_user_name: id_user_name, TIdentityPersonal.id_number: id_number,
                    TIdentityPersonal.bank_card_number: bank_card_number,
                    TIdentityPersonal.hold_user_name: hold_user_name,
                    TIdentityPersonal.bank_sub_name: bank_sub_name, TIdentityPersonal.qq_number: qq_number,
                    TIdentityPersonal.bank_name: bank_name})
                self.db_wealth.commit()
                if query_list:
                    self.write_json(200, '修改成功')
                    self.db_wealth.close()
                    return
                else:
                    self.write_json(500, '修改失败')
                    self.db_wealth.close()
                    return
            else:
                self.write_json(500, '修改失败')
                self.db_wealth.close()
        except Exception as e:
            self.db_wealth.close()
            log.e('SysApi.AddAccount:' + str(e))
            self.write_json(500, '修改失败')
        finally:
            self.db_wealth.close()
            # self.db_wealth.close()


class PlayLogAutoListHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/autoreview/autoreview.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()

        filter = args["filter"]
        search = filter["search"]
        today = datetime.date.today()
        # threeday = datetime.timedelta(days=3)
        # towday = datetime.timedelta(days=2)
        oneday = datetime.timedelta(days=1)
        yestorday = today - oneday
        # yestorday = today - threeday

        num = self.db_adm.query(PlayLogAuto).filter(
            PlayLogAuto.auto_date == yestorday).count()
        if num <= 0:
            max = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday)).count()
            now = self.db_ads.query(TaskPlayLog).filter(
                and_(
                    TaskPlayLog.create_time == yestorday,
                    TaskPlayLog.verify_status == 1)).count()
            verify_num = self.db_ads.query(TaskPlayLog).filter(
                and_(
                    TaskPlayLog.create_time == yestorday,
                    TaskPlayLog.verify_status == 1,
                    TaskPlayLog.verify_result == 0)).count()
            account_num = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday,
                     TaskPlayLog.verify_status == 1,
                     TaskPlayLog.close_account == 1,
                     TaskPlayLog.verify_result == 0)).count()
            count_money_num = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == yestorday,
                     TaskPlayLog.verify_status == 1,
                     TaskPlayLog.close_account == 1,
                     TaskPlayLog.is_count_money == 1,
                     TaskPlayLog.verify_result == 0)).count()
            pa = PlayLogAuto()
            pa.auto_max = max
            pa.auto_now = now
            pa.auto_date = yestorday
            pa.verify_num = verify_num
            pa.account_num = account_num
            pa.count_money_num = count_money_num
            pa.update_time = datetime.datetime.now()
            pa.auto_status = 0

            self.db_adm.add(pa)
            try:
                self.db_adm.commit()
            except Exception as e:
                log.e(e)
            finally:
                self.db_adm.close()
                self.db_ads.close()

        query = self.db_adm.query(PlayLogAuto)
        if search is not None and search != '':
            query = query.filter(PlayLogAuto.auto_date == search)
        total = query.count()
        query = query.order_by(PlayLogAuto.auto_date.desc())
        query = query.limit(int(limit['per_page'])).offset(
            (int(limit['page_index'] * limit['per_page'])))
        query_result = query.all()
        self.db_adm.close()

        lst = list()
        for item in query_result:
            lst.append(json.loads(json.dumps(item, cls=AlchemyEncoder)))
        ret = self.set_page_params(total, limit, lst)
        self.write_json(0, data=ret)
        # self.db_adm.close()


class PlayLogAutoAuditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        date = self.get_argument("date")
        id = self.get_argument("id")
        playnum = self.get_argument("playnum")

        if not date:
            self.write_json(-1, "日期不能为空")
            return
        try:
            results = self.db_ads.query(TaskPlayLog).filter(
                and_(TaskPlayLog.create_time == date, TaskPlayLog.verify_status == 0)).all()
        except Exception as e:
            log.e(e)
        finally:
            self.db_ads.close()
        yield self.autoAudit(id, results, date, playnum)
        self.write_json(0)

    @run_on_executor
    def autoAudit(self, id, results, date, playnum):
        user = self.get_current_user()
        for ret in results:
            now = app_playlogAuto[int(playnum)]["now"] + 1
            max = app_playlogAuto[int(playnum)]["max"]
            app_playlogAuto[int(playnum)] = {"now": now, 'max': max}
            ad_results = self.db_detect.query(Adresult).filter(
                Adresult.ad_key == ret.play_id).all()
            verify_user = user["id"]
            if ad_results:
                # 更新自动化审核进度
                res_list = list()
                for ad in ad_results:
                    res_list.append(ad.is_ad)
                verify_status = 1
                verify_result = 0 if 1 in res_list else -3
            else:
                verify_status = 1
                verify_result = -2
                # temp_result = -2

            self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == ret.play_id).update({
                TaskPlayLog.verify_user: verify_user,
                TaskPlayLog.verify_status: verify_status,
                TaskPlayLog.verify_result: verify_result
            })
            try:
                self.db_ads.commit()
            except Exception as e:
                self.db_ads.rollback()
                log.e(e)
            finally:
                self.db_ads.close()
                self.db_detect.close()
        # 修改 is_count_money
        sql_count = 'SELECT task_id,sum(verify_result) as verify_result from ads_task_play_log ' \
                    'where create_time=\'{}\' GROUP BY task_id'.format(date)
        task_counts = self.db_ads.execute(sql_count).fetchall()

        sql_update_count = 'update ads_task_play_log set is_count_money={} where task_id={}'

        app_playlogAuto[int(playnum)] = {"now": 0, "max": len(task_counts)}
        for t in task_counts:
            now = app_playlogAuto[int(playnum)]["now"] + 1
            max = app_playlogAuto[int(playnum)]["max"]
            app_playlogAuto[int(playnum)] = {"now": now, 'max': max}

            task_id, verify_result = t
            verify_result = 1 if verify_result == 0 else 0
            temp_sql = sql_update_count.format(verify_result, task_id)
            self.db_ads.execute(temp_sql)

        # 添加自动化审核日志
        oplog = AdsOpLog()
        oplog.op_type = 6
        user = self.get_current_user()
        oplog.op_user_id = user["id"]
        oplog.op_user_name = user["name"]
        oplog.op_desc = '用户{} 自动化审核 日期:{}'.format(user["name"], str(date))
        oc = {"user_id": user["id"], 'datetime': datetime.datetime.now()}
        oplog.op_content = str(oc)
        oplog.createtime = datetime.datetime.now()
        self.db_adm.add(oplog)

        # 更新自动化审核数据信息
        query = self.db_ads.query(TaskPlayLog).filter(
            and_(TaskPlayLog.create_time == date,
                 TaskPlayLog.verify_status == 1))
        now = query.count()
        query = query.filter(
            TaskPlayLog.verify_result == 0)
        verify_num = query.count()
        query = query.filter(TaskPlayLog.is_count_money == 1)
        count_money_num = query.count()
        query = query.filter(TaskPlayLog.close_account == 1)
        account_num = query.count()

        self.db_adm.query(PlayLogAuto).filter(PlayLogAuto.auto_id == id).update({
            PlayLogAuto.auto_status: 1,
            PlayLogAuto.auto_now: now,
            PlayLogAuto.account_num: account_num,
            PlayLogAuto.count_money_num: count_money_num,
            PlayLogAuto.verify_num: verify_num,
            PlayLogAuto.update_time: datetime.datetime.now(),
            PlayLogAuto.auto_user: user["name"]
        })
        try:
            self.db_adm.commit()
            self.db_ads.commit()
        except Exception as e:
            self.write_json(-1, '自动化审核失败')
            self.db_adm.rollback()
            self.db_ads.rollback()
            log.e(e)
        finally:
            self.db_ads.close()
            self.db_adm.close()
            self.db_detect.close()


class PlayLogAutoFlushHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):

        args = self.get_argument('args', None)
        if args:
            args = json.loads(args)
            date = args['date']
            id = args['id']

        if not date or not id:
            self.write_json(-1, "系统参数错误")
            return
            # 更新自动化审核数据信息
        query = self.db_ads.query(TaskPlayLog).filter(
            and_(TaskPlayLog.create_time == date,
                 TaskPlayLog.verify_status == 1))
        now = query.count()
        query = query.filter(
            TaskPlayLog.verify_result == 0)
        verify_num = query.count()
        query = query.filter(TaskPlayLog.is_count_money == 1)
        count_money_num = query.count()
        query = query.filter(TaskPlayLog.close_account == 1)
        account_num = query.count()
        self.db_adm.query(PlayLogAuto).filter(PlayLogAuto.auto_id == id).update({
            PlayLogAuto.auto_now: now,
            PlayLogAuto.account_num: account_num,
            PlayLogAuto.count_money_num: count_money_num,
            PlayLogAuto.verify_num: verify_num,
            PlayLogAuto.update_time: datetime.datetime.now()
        })

        try:
            self.db_adm.commit()
            self.write_json(0)
        except Exception as e:
            self.db_adm.rollback()
            self.write_json(-1, '刷新失败')
            log.e(e)
        finally:
            self.db_adm.close()
            self.db_ads.close()


class PlayLogAutoSelectHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        playnum = self.get_argument("playnum", None)
        if playnum is None:
            self.write_json(-1, 'playlog进度序列号不能为空')
            return
        if int(playnum) not in app_playlogAuto:
            app_playlogAuto[int(playnum)] = {"now": 0, "max": 0}
        self.write_json(0, '', app_playlogAuto[int(playnum)])


class PlayLogAutoCreateHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        date_now = int(time.time())
        id = self.get_argument('id')
        ret = self.db_adm.query(PlayLogAuto).filter(
            PlayLogAuto.auto_id == id).first()
        self.db_adm.close()
        if ret:
            app_playlogAuto[date_now] = {
                "now": ret.auto_now, "max": ret.auto_max}
            self.write_json(0, '', date_now)
        else:
            self.write_json(-1, '没有找到对应的数据信息')


class TaskRecepetCountHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):

        self.render("/ads_manager/taskReceptCount/taskReceptCount.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        date = self.get_argument("date", None)
        type = self.get_argument("type", None)  # type=1 查询 2 刷新数据库

        if not date:
            self.write_json(-1, "请选择日期")
            return

        pack_dataMap = dict()
        try:
            pack_data = self.db_entourage.query(ContractPackInfo).all()
        finally:
            self.db_entourage.close()

        for p in pack_data:
            pack_dataMap[p.package_id] = p.package_name
        lst = list()

        # 先查询数据库
        if type == "1":
            sql = '''
                        SELECT package_id,
                    sum(CASE when LEVEL='S'  THEN task_total END) s,
                    sum(CASE when LEVEL='S'  THEN task_accept END) s0,
                    sum(CASE when LEVEL='S'  THEN task_finish END) s1,
                    sum(CASE when LEVEL='S'  THEN task_forgo END) s2,
                    sum(CASE when LEVEL='S'  THEN task_onway END) s3,
                    sum(CASE when LEVEL='S'  THEN task_wait END) s4,

                    sum(CASE when LEVEL='A'  THEN task_total END) a,
                    sum(CASE when LEVEL='A'  THEN task_accept END) a0,
                    sum(CASE when LEVEL='A'  THEN task_finish END) a1,
                    sum(CASE when LEVEL='A'  THEN task_forgo END) a2,
                    sum(CASE when LEVEL='A'  THEN task_onway END) a3,
                    sum(CASE when LEVEL='A'  THEN task_wait END) a4,

                    sum(CASE when LEVEL='B'  THEN task_total END) b,
                    sum(CASE when LEVEL='B'  THEN task_accept END) b0,
                    sum(CASE when LEVEL='B'  THEN task_finish END) b1,
                    sum(CASE when LEVEL='B'  THEN task_forgo END) b2,
                    sum(CASE when LEVEL='B'  THEN task_onway END) b3,
                    sum(CASE when LEVEL='B'  THEN task_wait END) b4,

                    sum(CASE when LEVEL='C'  THEN task_total END) c,
                    sum(CASE when LEVEL='C'  THEN task_accept END) c0,
                    sum(CASE when LEVEL='C'  THEN task_finish END) c1,
                    sum(CASE when LEVEL='C'  THEN task_forgo END) c2,
                    sum(CASE when LEVEL='C'  THEN task_onway END) c3,
                    sum(CASE when LEVEL='C'  THEN task_wait END) c4,

                    sum(CASE when LEVEL='D'  THEN task_total END) d,
                    sum(CASE when LEVEL='D'  THEN task_accept END) d0,
                    sum(CASE when LEVEL='D'  THEN task_finish END) d1,
                    sum(CASE when LEVEL='D'  THEN task_forgo END )d2,
                    sum(CASE when LEVEL='D'  THEN task_onway END )d3,
                    sum(CASE when LEVEL='D'  THEN task_wait END )d4
                 from adm_dashboard_task  where task_time=\'{}\' GROUP  BY package_id '''.format(date)
            try:
                ret = self.db_adm.execute(sql).fetchall()
            except BaseException:
                self.write_json(-1, '查询失败')
                self.db_adm.close()
                return
            for d in ret:
                package_name = ''
                if d[0] in pack_dataMap:
                    package_name = pack_dataMap[d[0]]
                lst.append({"package_id": str(d[0]), "s": str(d[1]), "s0": str(d[2]), "s1": str(d[3]), "s2": str(d[4]),
                            "s3": str(d[5]), "s4": str(d[6]), "a": str(d[7]), "a0": str(d[8]),
                            "a1": str(d[8]), "a2": str(d[10]), "a3": str(d[11]), "a4": str(d[12]), "b": str(d[13]),
                            "b0": str(d[14]), "b1": str(d[15]), "b2": str(d[16]), "b3": str(d[17]), "b4": str(d[18]),
                            "c": str(d[19]), "c0": str(d[20]), "c1": str(d[21]), "c2": str(d[22]),
                            "c3": str(d[23]), "c4": str(d[24]), "d": str(d[25]), "d0": str(d[26]), "d1": str(d[27]),
                            "d2": str(d[28]), "d3": str(d[29]), "d4": str(d[30]), "package_name": package_name})
            if lst:
                self.write_json(code=0, data=lst)
        if type == "2" or not lst:

            start = date + " 00:00:00"
            end = date + " 23:59:59"
            sql_plan = 'SELECT i.package_id,sum(CASE i.anchor_level WHEN "S" THEN 1 ELSE 0 END) s,' \
                       'sum(CASE i.anchor_level WHEN "A" THEN 1 ELSE 0 END) a,' \
                       'sum(CASE i.anchor_level WHEN "B" THEN 1 ELSE 0 END) b,' \
                       'sum(CASE i.anchor_level WHEN "C" THEN 1 ELSE 0 END) c,' \
                       'sum(CASE i.anchor_level WHEN "D" THEN 1 ELSE 0 END) d' \
                       ' FROM' \
                       ' ads_need_plan_info n' \
                       ' LEFT JOIN ads_group_need_map m ON n.group_id = m.ads_group_id' \
                       ' LEFT JOIN ads_need_info i ON m.ads_need_id = i.need_id where i.package_id is not null' \
                       ' and n.create_time>\'{}\' and n.create_time < \'{}\' GROUP BY i.package_id'.format(start, end)
            try:
                datap = self.db_entourage.execute(sql_plan).fetchall()
            except Exception as e:
                log.e(e)
                self.db_entourage.close()
                return
            sql_task = '''
                       SELECT
        i.package_id,
             sum(CASE i.anchor_level WHEN 'S' THEN 1 ELSE 0 END) S,
             sum(CASE when i.anchor_level='S' and n.task_result=0 and n.task_status = 5 THEN 1 ELSE 0 END) S1,
             sum(CASE when i.anchor_level='S' and n.task_result=1 and n.task_status = 5  THEN 1 ELSE 0 END) S2,
             sum(CASE when i.anchor_level='S' and n.task_status=1 THEN 1 ELSE 0 END) S3,
             sum(CASE when i.anchor_level='S' and n.task_status=0 THEN 1 ELSE 0 END) S4,

             sum(CASE when i.anchor_level='A' THEN 1 ELSE 0 END) A,
             sum(CASE when i.anchor_level='A' and n.task_result=0 and n.task_status = 5 THEN 1 ELSE 0 END) A1,
             sum(CASE when i.anchor_level='A' and n.task_result=1 and n.task_status = 5 THEN 1 ELSE 0 END) A2,
             sum(CASE when i.anchor_level='A' and n.task_status=1 THEN 1 ELSE 0 END) A3,
             sum(CASE when i.anchor_level='A' and n.task_status=0 THEN 1 ELSE 0 END) A4,

              sum(CASE when i.anchor_level='B'  THEN 1 ELSE 0 END) B,
             sum(CASE when i.anchor_level='B' and n.task_result=0 and n.task_status = 5 THEN 1 ELSE 0 END) B1,
             sum(CASE when i.anchor_level='B' and n.task_result=1 and n.task_status = 5 THEN 1 ELSE 0 END) B2,
             sum(CASE when i.anchor_level='B' and n.task_status=1 THEN 1 ELSE 0 END) B3,
             sum(CASE when i.anchor_level='B' and n.task_status=0 THEN 1 ELSE 0 END) B4,

             sum(CASE when i.anchor_level='C'  THEN 1 ELSE 0 END) C,
             sum(CASE when i.anchor_level='C' and n.task_result=0 and n.task_status = 5 THEN 1 ELSE 0 END) C1,
             sum(CASE when i.anchor_level='C' and n.task_result=1 and n.task_status = 5 THEN 1 ELSE 0 END) C2,
             sum(CASE when i.anchor_level='C' and n.task_status=1 THEN 1 ELSE 0 END) C3,
             sum(CASE when i.anchor_level='C' and n.task_status=0 THEN 1 ELSE 0 END) C4,

             sum(CASE when i.anchor_level='D'  THEN 1 ELSE 0 END) D,
             sum(CASE when i.anchor_level='D' and n.task_result=0 and n.task_status = 5 THEN 1 ELSE 0 END) D1,
             sum(CASE when i.anchor_level='D' and n.task_result=1 and n.task_status = 5 THEN 1 ELSE 0 END) D2,
             sum(CASE when i.anchor_level='D' and n.task_status=1 THEN 1 ELSE 0 END) D3,
             sum(CASE when i.anchor_level='D' and n.task_status=0 THEN 1 ELSE 0 END) D4
             FROM
                ads_task n
            LEFT JOIN ads_group_need_map m ON n.group_id = m.ads_group_id
            LEFT JOIN ads_need_info i ON m.ads_need_id = i.need_id where i.package_id is not null and n.create_time= \'{}\' GROUP BY i.package_id


                      '''.format(date)

            try:
                datat = self.db_entourage.execute(sql_task).fetchall()
            finally:
                self.db_entourage.close()

            # lst = list()
            # lsts = list()
            # lsta = list()
            # lstb = list()
            # lstc = list()
            # lstd = list()
            dicts = dict()
            for p in datap:
                package_id = p.package_id
                package_name = ''
                if package_id in pack_dataMap:
                    package_name = pack_dataMap[package_id]
                s = str(p.s)
                a = str(p.a)
                b = str(p.b)
                c = str(p.c)
                d = str(p.d)
                dicts[package_id] = {
                    "package_id": package_id,
                    "package_name": package_name,
                    "s": s,
                    "a": a,
                    "b": b,
                    "c": c,
                    "d": d,
                    "s0": 0,
                    "s1": 0,
                    "s2": 0,
                    "s3": 0,
                    's4': 0,
                    "a0": 0,
                    "a1": 0,
                    "a2": 0,
                    "a3": 0,
                    "a4": 0,
                    "b0": 0,
                    "b1": 0,
                    "b2": 0,
                    "b3": 0,
                    "b4": 0,
                    "c0": 0,
                    "c1": 0,
                    "c2": 0,
                    "c3": 0,
                    "c4": 0,
                    "d0": 0,
                    "d1": 0,
                    "d2": 0,
                    "d3": 0,
                    "d4": 0}

            for t in datat:
                if t.package_id in dicts:
                    s0 = str(t.S)
                    s1 = str(t.S1)
                    s2 = str(t.S2)
                    s3 = str(t.S3)
                    s4 = str(t.S4)

                    a0 = str(t.A)
                    a1 = str(t.A1)
                    a2 = str(t.A2)
                    a3 = str(t.A3)
                    a4 = str(t.A4)

                    b0 = str(t.B)
                    b1 = str(t.B1)
                    b2 = str(t.B2)
                    b3 = str(t.B3)
                    b4 = str(t.B4)

                    c0 = str(t.C)
                    c1 = str(t.C1)
                    c2 = str(t.C2)
                    c3 = str(t.C3)
                    c4 = str(t.C4)

                    d0 = str(t.D)
                    d1 = str(t.D1)
                    d2 = str(t.D2)
                    d3 = str(t.D3)
                    d4 = str(t.D4)

                    dicts[t.package_id].update({"s0": s0,
                                                "s1": s1,
                                                "s2": s2,
                                                "s3": s3,
                                                "s4": s4,
                                                "a0": a0,
                                                "a1": a1,
                                                "a2": a2,
                                                "a3": a3,
                                                "a4": a4,
                                                "b0": b0,
                                                "b1": b1,
                                                "b2": b2,
                                                "b3": b3,
                                                "b4": b4,
                                                "c0": c0,
                                                "c1": c1,
                                                "c2": c2,
                                                "c3": c3,
                                                "c4": c4,
                                                "d0": d0,
                                                "d1": d1,
                                                "d2": d2,
                                                "d3": d3,
                                                "d4": d4})

            # lst = list()
            for d in dicts.keys():
                lst.append(dicts[d])
            self.db_adm.query(DashboardTask).filter(
                DashboardTask.task_time == date).delete(
                synchronize_session=False)
            try:
                self.db_adm.commit()
            except Exception as e:
                self.db_adm.rollback()
                log(e)
                self.write_json(-1, '查询失败')
                return

            for l in lst:
                dbts = DashboardTask()
                dbts.package_id = l["package_id"]
                dbts.level = "S"
                dbts.task_total = l["s"]
                dbts.task_accept = l["s0"]
                dbts.task_finish = l["s1"]
                dbts.task_forgo = l["s2"]
                dbts.task_onway = l["s3"]
                dbts.task_wait = l["s4"]
                dbts.task_time = date
                dbts.create_time = datetime.datetime.now()

                dbta = DashboardTask()
                dbta.package_id = l["package_id"]
                dbta.level = "A"
                dbta.task_total = l["a"]
                dbta.task_accept = l["a0"]
                dbta.task_finish = l["a1"]
                dbta.task_forgo = l["a2"]
                dbta.task_onway = l["a3"]
                dbta.task_wait = l["a4"]
                dbta.task_time = date
                dbta.create_time = datetime.datetime.now()

                dbtb = DashboardTask()
                dbtb.package_id = l["package_id"]
                dbtb.level = "B"
                dbtb.task_total = l["b"]
                dbtb.task_accept = l["b0"]
                dbtb.task_finish = l["b1"]
                dbtb.task_forgo = l["b2"]
                dbtb.task_onway = l["b3"]
                dbtb.task_wait = l["b4"]
                dbtb.task_time = date
                dbtb.create_time = datetime.datetime.now()

                dbtc = DashboardTask()
                dbtc.package_id = l["package_id"]
                dbtc.level = "C"
                dbtc.task_total = l["c"]
                dbtc.task_accept = l["c0"]
                dbtc.task_finish = l["c1"]
                dbtc.task_forgo = l["c2"]
                dbtc.task_onway = l["c3"]
                dbtc.task_wait = l["c4"]
                dbtc.task_time = date
                dbtc.create_time = datetime.datetime.now()

                dbtd = DashboardTask()
                dbtd.package_id = l["package_id"]
                dbtd.level = "D"
                dbtd.task_total = l["d"]
                dbtd.task_accept = l["d0"]
                dbtd.task_finish = l["d1"]
                dbtd.task_forgo = l["d2"]
                dbtd.task_onway = l["d3"]
                dbtd.task_wait = l["d4"]
                dbtd.task_time = date
                dbtd.create_time = datetime.datetime.now()

                self.db_adm.add(dbts)
                self.db_adm.add(dbta)
                self.db_adm.add(dbtb)
                self.db_adm.add(dbtc)
                self.db_adm.add(dbtd)

                try:
                    self.db_adm.commit()
                except Exception as e:
                    log(e)
                    self.db_adm.rollback()
                finally:
                    self.db_adm.close()
            self.write_json(code=0, data=lst)


# ---------------用户账户余额查询---------------------------------
class AccountBalanceList(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render(
            "/ads_manager/account_balance_info/account_balance_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        user_type = ''
        user_name = ''
        user_id = ''
        union_name = ''
        room_id = ''
        union_id = ''
        id_agent_id = ''
        id_agent_name = ''
        name_list = []
        if "user_type" in filter.keys():
            user_type = filter["user_type"]
            user_name = filter["user_name"]
            user_id = filter["user_id"]
            union_name = filter["union_name"]
            room_id = filter["room_id"]
            union_id = filter["union_id"]
            id_agent_id = filter["id_agent_id"]
            id_agent_name = filter["id_agent_name"]
        try:
            query = self.db_wealth.query(TAccountAnchor)
            query_guild = self.db_guild.query(
                BaseUser.user_id,
                BaseUser.u_nickname,
                BaseRoom.room_id,
                BaseRoom.platform_id).join(
                BaseRoom,
                BaseUser.user_id == BaseRoom.user_id)

            query_guild_union = self.db_guild.query(BaseUnion)
            query_guild_user = self.db_guild.query(BaseUser)
            query_baser_room_user = self.db_guild.query(BaseRoom)
            query_agent_name = self.db_ads.query(AgentInfo)
            if user_type:
                query = query.filter(TAccountAnchor.user_type == user_type)
            if user_name:
                user_name = '%' + user_name + '%'
                query_guild_data = query_guild_user.filter(
                    BaseUser.u_nickname.like(user_name)).all()
                if query_guild_data:
                    for i in query_guild_data:
                        name_list.append(i.user_id)
                    query = query.filter(TAccountAnchor.user_id.in_(name_list))
                else:
                    query = query.filter(TAccountAnchor.user_id is None)
            if user_id:
                query = query.filter(TAccountAnchor.user_id == user_id)
            if union_name:
                union_name = '%' + union_name + '%'
                query_guild_union_data = query_guild_union.filter(
                    BaseUnion.union_name.like(union_name)).first()
                if query_guild_union_data:
                    # print(query_guild_union_data)
                    query = query.filter(
                        TAccountAnchor.union_id == query_guild_union_data.union_id)
                else:
                    query = query.filter(TAccountAnchor.union_id is None)

            if id_agent_name:
                id_agent_name = '%' + id_agent_name + '%'
                query_ads_agent_data = query_agent_name.filter(
                    AgentInfo.agent_name.like(id_agent_name)).first()
                if query_ads_agent_data:
                    query = query.filter(
                        TAccountAnchor.agent_id == query_ads_agent_data.agent_id)
                else:
                    query = query.filter(TAccountAnchor.agent_id is None)
            if union_id:
                query = query.filter(TAccountAnchor.union_id == union_id)
            if id_agent_id:
                query = query.filter(TAccountAnchor.agent_id == id_agent_id)
            if room_id:
                query_guild_room_id = query_guild.filter(
                    BaseRoom.room_id == room_id).first()
                if query_guild_room_id:
                    query = query.filter(
                        TAccountAnchor.user_id == query_guild_room_id.user_id)
                else:
                    query = query.filter(TAccountAnchor.user_id is None)

            query = query.order_by(TAccountAnchor.last_stat_date.desc())

            total = query.count()
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()
            lst = list()
            for item in query_result:
                lst.append({
                    'user_id': item.user_id or 0,
                    'user_type': item.user_type or 0,
                    'agent_id': item.agent_id or 0,
                    'union_id': item.union_id or 0,
                    'balance': str(item.balance) or '',
                    'last_stat_date': item.last_stat_date.isoformat() or '',
                    'logtime': item.logtime.isoformat() or '',
                    'create_time': item.create_time.isoformat() or '',
                })
            base_user_room_list = app_map().Baseuserroom()
            base_union_list = app_map().Baseunion()
            ads_agent_list = app_map().AgentInfo()
            ret = self.set_page_params(total, limit, lst)
            for info_data in ret['data']:
                # for info_p in withdraw_list:
                if info_data['user_type'] == 1:
                    if info_data['user_id'] in base_user_room_list:
                        info_data['room_id'] = base_user_room_list[info_data['user_id']]['room_id']
                        info_data['u_nickname'] = base_user_room_list[info_data['user_id']]['u_nickname']
                        info_data['platform_id'] = base_user_room_list[info_data['user_id']]['platform_id']
                    else:
                        anchor_list_user = query_guild.filter(
                            BaseUser.user_id == info_data['user_id']).first()
                        query_baser_room_user_user = query_baser_room_user.filter(
                            BaseRoom.user_id == info_data['user_id']).first()
                        if anchor_list_user:
                            info_data['u_nickname'] = anchor_list_user.u_nickname
                            if query_baser_room_user_user:
                                info_data['room_id'] = query_baser_room_user_user.room_id
                                info_data['platform_id'] = query_baser_room_user_user.platform_id

                if info_data['union_id'] != 0 and info_data['union_id']:
                    if info_data['union_id'] in base_union_list:
                        info_data['union_name'] = base_union_list[info_data['union_id']]['union_name']
                    else:
                        anchor_list_union = query_guild_union.filter(
                            BaseUnion.union_id == info_data['union_id']).first()
                        if anchor_list_union:
                            info_data['union_name'] = anchor_list_union.union_name
                else:
                    info_data['union_name'] = '-'

                if info_data['agent_id'] != 0 and info_data['agent_id']:
                    if info_data['agent_id'] in ads_agent_list:
                        info_data['agent_name'] = ads_agent_list[info_data['agent_id']]['agent_name']
                    else:
                        anchor_list_union = query_agent_name.filter(
                            AgentInfo.agent_id == info_data['agent_id']).first()
                        if anchor_list_union:
                            info_data['agent_name'] = anchor_list_union.agent_name
                else:
                    info_data['agent_name'] = '-'
                if 'union_name' not in info_data:
                    info_data['union_name'] = '-'
                if 'agent_name' not in info_data:
                    info_data['agent_name'] = '-'
                if 'room_id' not in info_data:
                    info_data['room_id'] = '-'
                    info_data['platform_id'] = '-'
                if 'u_nickname' not in info_data:
                    info_data['u_nickname'] = '-'

                if info_data['user_id'] == 0:
                    info_data['user_id'] = '-'
                if info_data['agent_id'] == 0:
                    info_data['agent_id'] = '-'
                if info_data['union_id'] == 0:
                    info_data['union_id'] = '-'
                if info_data['platform_id'] is None:
                    info_data['platform_id'] = '-'
                if info_data['room_id'] is None:
                    info_data['room_id'] = '-'
            for info_data in ret['data']:
                if info_data['user_type'] == 1:
                    info_data['user_type_name'] = '普通主播'
                elif info_data['user_type'] == 2:
                    info_data['user_type_name'] = '公会用户'
                elif info_data['user_type'] == 3:
                    info_data['user_type_name'] = '经纪公司'

            self.write_json(0, data=ret)
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()
        except Exception as e:
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "AccountBalanceList查询失败")
        finally:
            self.db_wealth.close()
            self.db_guild.close()
            self.db_ads.close()


class AccountBalanceAddIncome(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        query_union_group_id_data = ''

        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            income_num = args["income"]
            play_id = args["play_id"]
            update_type = args["update_type"]
        else:
            self.write_json(-1, '系统错误')
            return
        #
        # platform_id = 0
        # room_id = 0
        income_type = 1
        sql_playlog = 'SELECT ' \
                      ' p.user_id,g.room_id groom_id,g.platform_id gplatform_id,g.union_id gunion_id,' \
                      ' u.agent_id uagent_id,u.plat_id uplat_id,u.room_id uroom_id,' \
                      ' t.plat_id plat_id,t.room_id troom_id,p.need_id' \
                      ' FROM' \
                      ' ads_task_play_log p' \
                      ' LEFT JOIN ads_union_group g ON g.user_id = p.user_id and g.apply_status=10' \
                      ' LEFT JOIN ads_agent_user_map u ON u.user_id = p.user_id' \
                      ' LEFT JOIN ads_task t ON t.task_id=p.task_id' \
                      ' WHERE 1=1  and p.play_id = {}'.format(play_id)
        playlogResults = self.db_ads.execute(sql_playlog).first()
        user_id = playlogResults[0]
        union_id = playlogResults[3]
        agent_id = playlogResults[4]
        need_id = playlogResults[9] if playlogResults[9] else 0
        if agent_id:
            platform_id = playlogResults[5]
            room_id = playlogResults[6]
            income_type = 3
        elif union_id:
            platform_id = playlogResults[2]
            room_id = playlogResults[1]
            income_type = 2
        else:
            platform_id = playlogResults[7]
            room_id = playlogResults[8]

        date_now = datetime.datetime.now()
        oc = "播放记录申诉:play_id:{},user_id:{},plat_id:{},room_id:{},datetime:{},need_id:{}".format(
            play_id, user_id, platform_id, room_id, date_now, need_id)

        query_union_group_id = self.db_ads.query(
            AdsUnionGroup.ads_union_group_id).filter(
            and_(
                AdsUnionGroup.user_id == user_id,
                AdsUnionGroup.platform_id == platform_id,
                AdsUnionGroup.room_id == room_id,
                AdsUnionGroup.union_id == union_id)).first()
        task_id = self.db_ads.query(
            TaskPlayLog.task_id,
            TaskPlayLog.create_time,
            TaskPlayLog.close_account).filter(
            TaskPlayLog.play_id == play_id).first()

        user = self.get_current_user()
        #财务模块--update_type==》2修改 3 申诉
        # 修改只修改ads_task_play_log  申诉 需同时修改财富结算相关表
        if update_type == 2 or update_type == 3:
            # self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == play_id).update(
            #     {TaskPlayLog.income: income_num,
            #      TaskPlayLog.verify_result: 0,
            #      TaskPlayLog.verify_status: 1,
            #      TaskPlayLog.is_count_money: 1,
            #      })
            p_data=self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == play_id).first()
            if p_data:
                p_data.income=income_num
                p_data.verify_result=0
                p_data.verify_status=1
                p_data.is_count_money=1
                if p_data.coin_exchange_rate and income_num:
                    p_data.coin_count = (p_data.coin_exchange_rate *
                                         Decimal(income_num)).quantize(Decimal('0.00'))

            # 添加修改ads_task_play_log日志
            oplog = AdsOpLog()
            oplog.op_type = 9
            oplog.op_user_id = user["id"]
            oplog.op_user_name = user["name"]
            oplog.op_desc = '修改 ads_task_play_log 金额: play_id:{}  income:{}'.format(
                play_id, income_num)
            occ = {
                "play_id:{} income:{}".format(
                    play_id,
                    income_num)}
            oplog.op_content = str(occ)
            oplog.createtime = datetime.datetime.now()
            self.db_adm.add(oplog)

        if update_type == 3:
            # 校验当前是否关账
            if task_id.close_account != 1:
                self.db_ads.close()
                self.db_wealth.close()
                self.write_json(-1, '未结账不允许申诉')
                return

            old_income = 0
            if income_type == 1:
                old_income = self.db_wealth.query(TAccountAnchor.balance). \
                    filter(TAccountAnchor.user_id == user_id).first()
            elif income_type == 2:
                old_income = self.db_wealth.query(TAccountAnchor.balance). \
                    filter(TAccountAnchor.union_id == union_id).first()
            elif income_type == 3:
                old_income = self.db_wealth.query(TAccountAnchor.balance). \
                    filter(TAccountAnchor.agent_id == agent_id).first()
            if old_income:
                old_balance = old_income.balance
                if income_num:
                    new_income = old_income.balance + Decimal(income_num)
                else:
                    new_income = Decimal(old_income.balance) + Decimal('0')
            else:
                # 如果用户没有账号信息 添加一个
                old_balance = 0
                new_income = income_num
                account = TAccountAnchor()
                account.user_id = user_id
                account.user_type = income_type
                account.agent_id = agent_id if agent_id else 0
                account.union_id = union_id if union_id else 0
                account.balance = 0
                account.last_stat_date = datetime.date.today()
                account.create_time = datetime.datetime.now()
                account.lock_balance = 0
                self.db_wealth.add(account)

            if query_union_group_id:
                query_union_group_id_data = query_union_group_id.ads_union_group_id
            else:
                query_union_group_id_data = 0
            if task_id:
                task_id_data = task_id.task_id
                task_creatime_data = task_id.create_time.isoformat()
            else:
                task_id_data = 0
                task_creatime_data = date_now

            # 添加一条财富表日志
            tlogincomeanchor = TLogIncomeAnchor()
            tlogincomeanchor.income_type = income_type
            tlogincomeanchor.ads_union_group_id = query_union_group_id_data
            tlogincomeanchor.agent_id = int(
                agent_id) if agent_id is not None else 0
            tlogincomeanchor.union_id = int(
                union_id) if union_id is not None else 0
            tlogincomeanchor.user_id = user_id
            tlogincomeanchor.play_id = play_id
            tlogincomeanchor.need_id = need_id
            tlogincomeanchor.plat_id = platform_id
            tlogincomeanchor.room_id = room_id
            tlogincomeanchor.task_id = task_id_data
            tlogincomeanchor.income_from = 3
            tlogincomeanchor.income = income_num
            tlogincomeanchor.comment = str(oc)
            tlogincomeanchor.create_time = date_now
            tlogincomeanchor.logtime = date_now
            tlogincomeanchor.task_create_time = task_creatime_data
            self.db_wealth.add(tlogincomeanchor)

            # 修改账户余额
            if income_type == 1:
                self.db_wealth.query(TAccountAnchor).filter(
                    TAccountAnchor.user_id == user_id).update({TAccountAnchor.balance: new_income})
            elif income_type == 2:
                self.db_wealth.query(TAccountAnchor).filter(
                    TAccountAnchor.union_id == union_id).update({TAccountAnchor.balance: new_income})
            elif income_type == 3:
                self.db_wealth.query(TAccountAnchor).filter(
                    TAccountAnchor.agent_id == agent_id).update({TAccountAnchor.balance: new_income})

            oplog = AdsOpLog()
            oplog.op_type = 7
            user = self.get_current_user()
            oplog.op_user_id = user["id"]
            oplog.op_user_name = user["name"]
            oplog.op_desc = '更新 T_log_income_anchor balance:' + str(new_income)
            occ = {
                "old_balance:{} add_balance:{},new_balance:{} ,need_id:{}, plat_id:{},room_id:{}".format(
                    float(old_balance),
                    float(income_num),
                    float(new_income),
                    need_id,
                    platform_id,
                    room_id)}
            oplog.op_content = str(occ)
            oplog.createtime = datetime.datetime.now()
            self.db_adm.add(oplog)
        try:
            self.db_wealth.commit()
            self.db_adm.commit()
            self.db_ads.commit()
            self.write_json(0, "添加成功")
        except Exception as e:
            self.db_wealth.rollback()
            self.db_adm.rollback()
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "添加错误")
        finally:
            self.db_ads.close()
            self.db_adm.close()
            self.db_wealth.close()


class AccountAdd4ClosePackage(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            income_num = args["income_num"]
            play_id = args["play_id"]
            comment = args["comment"]
            # user_id = args["user_id"]
        else:
            self.write_json(-1, '系统错误')
            return
        if not play_id:
            self.write_json(-1, 'play_id不能为空')
            return

        sql_filter = 'SELECT t.task_id,t.create_time,t.close_account,t.is_count_money,p.status FROM ads_task_play_log t ' \
                     'LEFT JOIN ads_need_info n ON n.need_id = t.need_id LEFT JOIN ads_contract_package_info p ' \
                     'ON p.package_id = n.package_id WHERE play_id={}'.format(play_id)
        play_log_data = self.db_ads.execute(sql_filter).first()
        # 校验当前play_log 是否可以增加余额 2标示已经关账
        income_from = 3
        if play_log_data.status == 2:
            income_from = 4
        elif not play_log_data or play_log_data.close_account != 1 or play_log_data.is_count_money != 1:
            self.db_ads.close()
            self.db_wealth.close()
            self.write_json(-1,
                            '当前播放记录(play_id:{}),应该【申诉】或【修改】'.format(play_id))
            return

        # 检查当前 套餐是否关账 2标示已经关账
        # if play_log_data.status == 2:
        #     income_from = 4
        # else:
        #     income_from = 3

        income_type = 1
        sql_playlog = 'SELECT ' \
                      ' p.user_id,g.room_id groom_id,g.platform_id gplatform_id,g.union_id ' \
                      ' gunion_id, u.agent_id uagent_id,u.plat_id uplat_id,u.room_id uroom_id,' \
                      ' t.plat_id plat_id,t.room_id troom_id,p.need_id FROM ads_task_play_log p' \
                      ' LEFT JOIN ads_union_group g ON g.user_id = p.user_id and g.apply_status=10' \
                      ' LEFT JOIN ads_agent_user_map u ON u.user_id = p.user_id' \
                      ' LEFT JOIN ads_task t ON t.task_id=p.task_id' \
                      ' WHERE 1=1  and p.play_id = {}'.format(play_id)
        playlogResults = self.db_ads.execute(sql_playlog).first()
        if not playlogResults:
            self.write_json(-1, '无法获取play_id:的数据'.format(play_id))
            self.db_ads.close()
            return
        user_id = playlogResults[0]
        union_id = playlogResults[3]
        agent_id = playlogResults[4]
        need_id = playlogResults[9] if playlogResults[9] else 0
        if agent_id:
            platform_id = playlogResults[5]
            room_id = playlogResults[6]
            income_type = 3
        elif union_id:
            platform_id = playlogResults[2]
            room_id = playlogResults[1]
            income_type = 2
        else:
            platform_id = playlogResults[7]
            room_id = playlogResults[8]

        date_now = datetime.datetime.now()
        query_union_group_id = self.db_ads.query(
            AdsUnionGroup.ads_union_group_id).filter(
            and_(
                AdsUnionGroup.user_id == user_id,
                AdsUnionGroup.platform_id == platform_id,
                AdsUnionGroup.room_id == room_id,
                AdsUnionGroup.union_id == union_id)).first()
        # 获取之前账户的余额
        old_income = 0
        if income_type == 1:
            old_income = self.db_wealth.query(TAccountAnchor.balance). \
                filter(TAccountAnchor.user_id == user_id).first()
        elif income_type == 2:
            old_income = self.db_wealth.query(TAccountAnchor.balance). \
                filter(TAccountAnchor.union_id == union_id).first()
        elif income_type == 3:
            old_income = self.db_wealth.query(TAccountAnchor.balance). \
                filter(TAccountAnchor.agent_id == agent_id).first()

        if old_income:
            old_balance = old_income.balance
            if income_num:
                new_income = old_income.balance + Decimal(income_num)
            else:
                new_income = Decimal(old_income.balance) + Decimal('0')
        else:
            # 如果用户没有账号信息 添加一个
            old_balance = 0
            new_income = income_num
            account = TAccountAnchor()
            account.user_id = user_id if income_type == 1 else 0
            account.user_type = income_type
            account.agent_id = agent_id if agent_id else 0
            account.union_id = union_id if union_id else 0
            account.balance = 0
            account.last_stat_date = datetime.date.today()
            account.create_time = datetime.datetime.now()
            account.lock_balance = 0
            self.db_wealth.add(account)

        if query_union_group_id:
            query_union_group_id_data = query_union_group_id.ads_union_group_id
        else:
            query_union_group_id_data = 0
        if play_log_data:
            task_id_data = play_log_data.task_id
            task_creatime_data = play_log_data.create_time.isoformat()
        else:
            task_id_data = 0
            task_creatime_data = date_now

        # 添加一条财富表日志
        tlogincomeanchor = TLogIncomeAnchor()
        tlogincomeanchor.income_type = income_type
        tlogincomeanchor.ads_union_group_id = query_union_group_id_data
        tlogincomeanchor.agent_id = int(
            agent_id) if agent_id is not None else 0
        tlogincomeanchor.union_id = int(
            union_id) if union_id is not None else 0
        tlogincomeanchor.user_id = user_id
        tlogincomeanchor.play_id = play_id
        tlogincomeanchor.need_id = need_id
        tlogincomeanchor.plat_id = platform_id
        tlogincomeanchor.room_id = room_id
        tlogincomeanchor.task_id = task_id_data
        tlogincomeanchor.income_from = income_from
        tlogincomeanchor.income = income_num
        tlogincomeanchor.comment = comment
        tlogincomeanchor.create_time = date_now
        tlogincomeanchor.logtime = date_now
        tlogincomeanchor.task_create_time = task_creatime_data
        self.db_wealth.add(tlogincomeanchor)

        # 修改账户余额
        if income_type == 1:
            self.db_wealth.query(TAccountAnchor).filter(
                TAccountAnchor.user_id == user_id).update({TAccountAnchor.balance: new_income})
        elif income_type == 2:
            self.db_wealth.query(TAccountAnchor).filter(
                TAccountAnchor.union_id == union_id).update({TAccountAnchor.balance: new_income})
        elif income_type == 3:
            self.db_wealth.query(TAccountAnchor).filter(
                TAccountAnchor.agent_id == agent_id).update({TAccountAnchor.balance: new_income})
        # 修改播放记录金额
        # self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == play_id).update(
        #     {TaskPlayLog.income: income_num,
        #      TaskPlayLog.verify_result: 0,
        #      TaskPlayLog.verify_status: 1,
        #      TaskPlayLog.is_count_money: 1
        #      })
        p_data = self.db_ads.query(TaskPlayLog).filter(TaskPlayLog.play_id == play_id).first()
        if p_data:
            p_data.income = income_num
            p_data.verify_result = 0
            p_data.verify_status = 1
            p_data.is_count_money = 1
            if p_data.coin_exchange_rate and income_num:
                p_data.coin_count = (p_data.coin_exchange_rate *
                                     Decimal(income_num)).quantize(Decimal('0.00'))

        # 添加2条日志
        oplog = AdsOpLog()
        oplog.op_type = 10
        user = self.get_current_user()
        oplog.op_user_id = user["id"]
        oplog.op_user_name = user["name"]
        oplog.op_desc = '更新 T_log_income_anchor balance:' + str(new_income)
        occ = "old_balance:{} add_balance:{},new_balance:{},need_id:{}," \
              " plat_id:{},room_id:{},user_id:{},union_id:{},agent_id:{}".format(
                  old_balance, income_num, new_income, need_id, platform_id, room_id, user_id, union_id, agent_id)
        oplog.op_content = str(occ)
        oplog.createtime = datetime.datetime.now()
        oplog2 = AdsOpLog()
        oplog2.op_type = 9
        oplog2.op_user_id = user["id"]
        oplog2.op_user_name = user["name"]
        oplog2.op_desc = '修改 ads_task_play_log 金额: play_id:{}  income:{}'.format(
            play_id, income_num)
        occ2 = {
            "play_id:{} income:{}".format(
                play_id,
                income_num)}
        oplog2.op_content = str(occ2)
        oplog2.createtime = datetime.datetime.now()

        self.db_adm.add(oplog)
        self.db_adm.add(oplog2)
        try:
            self.db_wealth.commit()
            self.db_adm.commit()
            self.db_ads.commit()
            self.write_json(0, "添加成功")
        except Exception as e:
            self.db_wealth.rollback()
            self.db_adm.rollback()
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "添加错误")
        finally:
            self.db_ads.close()
            self.db_adm.close()
            self.db_wealth.close()


class AccountBalanceGetPackage(SwxJsonHandler):
    def get(self, *args, **kwargs):
        query_list = None
        try:
            lst = []
            query_list = self.db_ads.query(
                ContractPackInfo.package_id,
                ContractPackInfo.package_name).order_by(
                ContractPackInfo.package_id.desc()).all()
            for ptype in query_list:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
            self.db_ads.close()
        except Exception as e:
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "获取套餐list失败")
        finally:
            self.db_ads.close()

            # self.db_ads.close()


class AccountBalanceGetNeedId(SwxJsonHandler):
    def get(self, *args, **kwargs):
        query_list = None
        user_id = self.get_argument("user_id", None)
        # need_id = self.get_argument("need_id", None)
        try:
            lst = []
            query_list = self.db_ads.query(
                TaskPlayLog.need_id,
                NeedInfo.need_name).join(
                NeedInfo,
                NeedInfo.need_id == TaskPlayLog.need_id).group_by(
                TaskPlayLog.need_id).order_by(
                TaskPlayLog.need_id.desc())
            if user_id:
                query_list = query_list.filter(TaskPlayLog.user_id == user_id)
            query_list_data = query_list.all()
            for ptype in query_list_data:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
        except Exception as e:
            log.e(e)
            self.write_json(500, "获取need_id失败")
        finally:
            self.db_ads.close()


class AccountBalanceGetPlayId(SwxJsonHandler):
    def get(self, *args, **kwargs):
        query_list = None
        user_id = self.get_argument("user_id", None)
        need_id = self.get_argument("need_id", None)
        try:
            lst = []
            query_list = self.db_ads.query(TaskPlayLog.play_id).order_by(
                TaskPlayLog.play_id.desc())
            if user_id:
                query_list = query_list.filter(TaskPlayLog.user_id == user_id)
            if need_id:
                query_list = query_list.filter(TaskPlayLog.need_id == need_id)
            query_list_data = query_list.all()
            for ptype in query_list_data:
                lst.append(json.loads(json.dumps(ptype, cls=AlchemyEncoder)))
            self.write_raw_json(lst)
        except Exception as e:
            log.e(e)
            self.write_json(500, "获取play_id失败")
        finally:
            self.db_ads.close()


class AccountBalanceIncomeList(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        id = self.get_argument("id", None)
        user_type = self.get_argument("user_type", None)
        # unionList = app_map().getUnionList()
        income_all = 0
        user_name = ''
        query_list = None
        if id is None:
            self.write_json(-1, "系统错误")
            return
        _, lst = app_map().get_platform_map_list()

        if user_type == '1':
            user_name = '用户'
            query_list = self.db_wealth.query(TLogIncomeAnchor).filter(
                TLogIncomeAnchor.user_id == id).order_by(
                TLogIncomeAnchor.income_log_id.desc()).all()
        elif user_type == '2':
            user_name = '公会'
            query_list = self.db_wealth.query(TLogIncomeAnchor).filter(
                TLogIncomeAnchor.union_id == id).order_by(
                TLogIncomeAnchor.income_log_id.desc()).all()
        elif user_type == '3':
            user_name = '经纪人'
            query_list = self.db_wealth.query(TLogIncomeAnchor).filter(
                TLogIncomeAnchor.agent_id == id).order_by(
                TLogIncomeAnchor.income_log_id.desc()).all()

        self.db_wealth.close()
        if query_list:
            for ptype in query_list:
                income_all = round(income_all, 2) + round(ptype.income, 2)

        self.render(
            "/ads_manager/account_balance_info/account_balance_select_list.mako",
            id=id,
            income_all=income_all,
            user_type=user_type,
            user_name=user_name)

    @tornado.web.authenticated
    @permision
    def post(self):
        # print('2323')
        limit, args = self.get_pages_args()
        id = self.get_argument("id", None)
        user_type = self.get_argument("user_type", None)
        ret = dict()
        # print(id)
        if id is None or id == "":
            self.write_json(-1, "系统错误")
            return
        try:
            lst = []
            query = ''
            income_type_name = ''
            income_from_name = ''
            status_name = ''
            if id:
                id = str(id).split(':')[1]

                if user_type == '1':
                    query = self.db_wealth.query(TLogIncomeAnchor).filter(
                        TLogIncomeAnchor.user_id == id).order_by(
                        TLogIncomeAnchor.income_log_id.desc())
                elif user_type == '2':
                    query = self.db_wealth.query(TLogIncomeAnchor).filter(
                        TLogIncomeAnchor.union_id == id).order_by(
                        TLogIncomeAnchor.income_log_id.desc())
                elif user_type == '3':
                    query = self.db_wealth.query(TLogIncomeAnchor).filter(
                        TLogIncomeAnchor.agent_id == id).order_by(
                        TLogIncomeAnchor.income_log_id.desc())

                # query = self.db_wealth.query(TLogIncomeAnchor).filter(
                # TLogIncomeAnchor.user_id ==
                # id).order_by(TLogIncomeAnchor.income_log_id.desc())
                total = query.count()
                query = query.limit(int(limit['per_page'])).offset(
                    (int(limit['page_index'] * limit['per_page'])))
                query_schedule = query.all()
                # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
                if query_schedule:
                    for ptype in query_schedule:
                        if ptype.income_type == 1:
                            income_type_name = '直接对主播结算'
                        elif ptype.income_type == 2:
                            income_type_name = '对公会结算'
                        elif ptype.income_type == 3:
                            income_type_name = '对经纪公司结算'

                        if ptype.income_from == 1:
                            income_from_name = '从play_log结算'
                        elif ptype.income_from == 2:
                            income_from_name = '运营要求加上去的'
                        elif ptype.income_from == 3:
                            income_from_name = '申诉成功要求加上去的'

                        lst.append({
                            'income_log_id': ptype.income_log_id or '',
                            'union_id': ptype.union_id or 0,
                            'agent_id': ptype.agent_id,
                            'user_id': ptype.user_id,
                            'task_id': ptype.task_id,
                            'play_id': ptype.play_id,
                            'plat_id': ptype.plat_id,
                            'room_id': ptype.room_id,
                            'comment': ptype.comment,
                            'income': float(ptype.income),
                            'income_type_name': income_type_name,
                            'income_from_name': income_from_name,
                            'logtime': str(ptype.logtime.isoformat()).replace('T', ' ') or '',
                        })

                    ret['data'] = lst
                    ret['page_index'] = limit['page_index']
                    ret['total'] = total
                    self.write_json(0, data=ret)
                    self.db_wealth.close()
                else:
                    self.write_json(0, '没有对应的结算信息')
                    # self.write_json(0, data=ret)
                    self.db_wealth.close()
        except Exception as e:
            self.db_wealth.close()
            log.e(e)
            self.write_json(500, "获取错误")
        finally:
            # self.db_entourage.close()
            self.db_wealth.close()

            # self.db_entourage.close()


class AccountBalanceIncomeUpdate(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        # print('2323')
        id = self.get_argument("id", None)
        ret = dict()
        if id is None or id == "":
            self.write_json(-1, "系统错误")
            return
        try:
            lst = []
            # query = ''
            income_type_name = ''
            income_from_name = ''
            # status_name = ''
            if id:
                id = str(id).split(':')[1]
                query = self.db_wealth.query(TLogIncomeAnchor).filter(
                    TLogIncomeAnchor.user_id == id).order_by(
                    TLogIncomeAnchor.income_log_id.desc())
                total = query.count()
                query_schedule = query.all()
                # sql_session.update({AdsConfigAnchorWhitelist.eff_airtime: time_len})
                if query_schedule:
                    for ptype in query_schedule:
                        if ptype.income_type == 1:
                            income_type_name = '直接对主播结算'
                        elif ptype.income_type == 2:
                            income_type_name = '对公会结算'
                        elif ptype.income_type == 3:
                            income_type_name = '对经纪公司结算'

                        if ptype.income_from == 1:
                            income_from_name = '从play_log结算'
                        elif ptype.income_from == 2:
                            income_from_name = '运营要求加上去的'
                        elif ptype.income_from == 3:
                            income_from_name = '申诉成功要求加上去的'

                        lst.append({
                            'income_log_id': ptype.income_log_id or '',
                            'union_id': ptype.union_id or 0,
                            'agent_id': ptype.agent_id,
                            'user_id': ptype.user_id,
                            'task_id': ptype.task_id,
                            'play_id': ptype.play_id,
                            'plat_id': ptype.plat_id,
                            'room_id': ptype.room_id,
                            'comment': ptype.comment,
                            'income': float(ptype.income),
                            'income_type_name': income_type_name,
                            'income_from_name': income_from_name,
                            'logtime': str(ptype.logtime.isoformat()).replace('T', ' ') or '',
                        })

                    ret['data'] = lst
                    ret['total'] = total
                    self.db_entourage.close()
            list_name = ['结算log ID', '公会ID', '经纪人ID', '用户ID', '任务ID',
                         'playID',
                         '平台ID', '房间ID', '描述', '结算价格', '结算类型', '结算来源', '时间'
                         ]

            els_url = export_acoount_balance_select_list(
                lst, list_name, list_name)
            self.write_json(0, data=els_url)
            return
        except Exception as e:
            # session.rollback()
            log.e('AccountBalanceIncomeUpdate:' + str(e))
            self.write_json(500, 'user_id结算信息(跳转,导出)失败')
            return
        finally:
            self.db_wealth.close()


class CloudDiscernListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("/ads_manager/cloudDiscern/cloud.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = "SELECT id,r.play_id,expect_words,actual_words,match_ratio,`from`,r.log_time," \
                  "p.verify_status,p.verify_result from ads_log_oral_ads_result r LEFT JOIN " \
                  "ads_task_play_log p on r.play_id=p.play_id where 1=1"

            filter = args["filter"]
            verify_result = filter["verify_result"]
            name = filter["search"]
            cloud_from = filter["cloud_from"]
            createtime = filter["createtime"]
            if name:
                sql = sql + " and r.play_id like '%" + name.strip() + "%'"
            if verify_result:
                if verify_result == '1':
                    sql = sql + " and p.verify_result !=0 and  p.verify_result !=-1"
                else:
                    sql = sql + " and p.verify_result = '" + verify_result + "'"
            offset = " ORDER BY r.play_id DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            if cloud_from:
                sql = sql + " and r.from = '" + cloud_from + "'"

            if createtime:
                start = createtime + " 00:00:00"
                end = createtime + " 23:59:59"
                sql = sql + " and r.create_time >= '" + start + \
                    "' and r.create_time <= '" + end + "'"

            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'id',
                'play_id',
                'expect_words',
                'actual_words',
                'match_ratio',
                'from',
                'log_time',
                'verify_status',
                'verify_result']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['log_time'] = temp['log_time'].isoformat()
                lst.append(temp)

            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')

        finally:
            self.db_ads.close()


# ---------------角色管理---------------------------------
class RoleInfoSelectHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/sys_manager/role_info/role_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        role_name = ''
        try:
            if "search" in filter.keys():
                role_name = filter["search"]
            query = self.db_adm.query(AdmRole)
            if role_name:
                # name = '%' + name + '%'
                role_name = '%' + role_name + '%'
                query = query.filter(AdmRole.role_name.like(role_name))
            total = query.count()
            query = query.order_by(AdmRole.role_id.desc())
            query = query.limit(int(limit['per_page'])).offset(
                (int(limit['page_index'] * limit['per_page'])))
            query_result = query.all()

            lst = list()
            for item in query_result:
                if item.role_name != 'admin':
                    lst.append({
                        'role_id': item.role_id or '',
                        'role_name': item.role_name or '',
                        'create_time': item.create_time.isoformat() or '',
                        'log_time': item.log_time.isoformat() or '',
                    })
            ret = self.set_page_params(total, limit, lst)
            self.write_json(0, data=ret)
            self.db_adm.close()
        except Exception as e:
            # self.db_adm.close()
            log.e(e)
            self.write_json(500, "roleInfoSelectHander查询失败")
        finally:
            self.db_adm.close()


class RoleInfoAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):

        role_name = self.get_argument("role_name", None)
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
            # create_time = args["create_time"]
            role_name = args["role_name"]

        try:
            date_now = datetime.datetime.now()
            item = AdmRole(role_name=role_name,
                           log_time=date_now,
                           create_time=date_now
                           )
            self.db_adm.add(item)
            self.db_adm.commit()

            self.write_json(0)  # 将上传好的路径返回
        except Exception as e:
            self.db_adm.rollback()
            log.e(e)
            self.write_json(500, "新增失败")
        finally:
            self.db_adm.close()


class AdsPackageInfoScheduleListHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        date = self.get_argument('date')
        # type=self.get_argument('type')
        self.render('ads_manager/ads_caldar/ads_caldar_list.mako', date=date)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        filter = args["filter"]
        cal_date = filter['cal_date']
        # type = filter['type']
        # sql = "select order_id,order_sche_name,order_date,s.package_id,need_play_num,order_status," \
        #       "order_s,order_a,order_b,order_c,order_d,adsinfo_id,create_people,p.status" \
        #       " from ads_package_info_schedule s LEFT JOIN ads_contract_package_info " \
        #       "p on s.package_id=p.package_id where 1=1"
        sql = "select order_id,order_sche_name,order_date,s.package_id,need_play_num,order_status," \
              "order_s,order_a,order_b,order_c,order_d,adsinfo_id,create_people" \
              " from ads_package_info_schedule s where 1=1"

        if cal_date:
            sql = sql + ' and order_date=\'{}\''.format(cal_date)
        offset = " ORDER BY order_id DESC LIMIT {},{}".format(
            limit['page_index'] * limit['per_page'], limit['per_page'])
        datas = self.db_adm.execute(sql + offset).fetchall()
        lst = list()
        head = [
            'order_id',
            'order_sche_name',
            'order_date',
            'package_id',
            'need_play_num',
            'order_status',
            'order_s',
            'order_a',
            'order_b',
            'order_c',
            'order_d',
            'adsinfo_id',
            'create_people']
        for data in datas:
            temp = dict(zip(head, data))
            temp['order_date'] = temp['order_date'].isoformat()
            package_id = temp.get('package_id', None)
            if package_id:
                sql_pack = 'select status from ads_contract_package_info where package_id={}'.format(
                    package_id)
                pstatus = self.db_ads.execute(sql_pack).scalar()
                temp['status'] = pstatus
            lst.append(temp)
        count = self.db_adm.execute(
            "select count(*) from({}) as count_data".format(sql)).scalar()
        ret = self.set_page_params(count, limit, lst)
        self.db_adm.close()
        self.db_ads.close()
        self.write_json(0, data=ret)


class AdsPackageInfoScheduleSelectHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('ads_manager/ads_caldar/ads_caldar.mako')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        date = self.get_argument('date')
        start_date = datetime.datetime.strptime(date, "%Y-%m")
        year = start_date.year
        month = start_date.month
        _, last_day = calendar.monthrange(year, month)
        start = '{}-{}-01'.format(year, month)
        end = '{}-{}-{}'.format(year, month, last_day)
        # sql = "select order_id,order_sche_name,order_date,order_status,p.`status`,s.package_id " \
        #       " from ads_package_info_schedule s LEFT JOIN ads_contract_package_info p " \
        #       " on p.package_id=s.package_id where 1=1 and order_date<='{}' and order_date>='{}'". \
        #     format(end, start)
        sql = "select order_id,order_sche_name,order_date,order_status,s.package_id " \
              " from ads_package_info_schedule s  where 1=1 and order_date<='{}' and order_date>='{}'". \
            format(end, start)
        datas = self.db_adm.execute(sql).fetchall()

        head = ['id', 'title', 'start', 'order_status', 'package_id']

        lst = list()
        for data in datas:
            order_id, order_sche_name, order_date, order_status, package_id = data
            order_date = order_date.isoformat() if order_date else ''
            temp = dict(zip(head, (order_id, order_sche_name,
                                   order_date, order_status, package_id)))
            sql_pack = 'select status from ads_contract_package_info where package_id={}'.format(
                package_id)
            pstatus = self.db_ads.execute(sql_pack).scalar()
            temp['pstatus'] = pstatus
            lst.append(temp)
        self.db_adm.close()
        self.db_ads.close()
        self.write_raw_json(lst)


class AdsCal4PackageAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    # @permision
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        # package_id = args["package_id"]
        package_name = args["package_name"]
        adser = args["adser"]
        begin_time = args["begin_time"]
        end_time = args["end_time"]
        ads_play_num_desc = args["ads_play_num_desc"]
        serving_meth = args["serving_meth"]
        is_allow_repeat = args["is_allow_repeat"]
        # need_desc = args["need_desc"]
        ads_play_num = args["ads_play_num"]
        s = int(args["s"]) if args["s"] else 0
        a = int(args["a"]) if args["a"] else 0
        b = int(args["b"]) if args["b"] else 0
        c = int(args["c"]) if args["c"] else 0
        d = int(args["d"]) if args["d"] else 0
        serving_meth = int(serving_meth) if serving_meth else 1
        ads_play_num = int(ads_play_num) if ads_play_num else 1
        s_day = math.ceil(s / serving_meth) if s else 0
        a_day = math.ceil(a / serving_meth) if a else 0
        b_day = math.ceil(b / serving_meth) if b else 0
        c_day = math.ceil(c / serving_meth) if c else 0
        d_day = math.ceil(d / serving_meth) if d else 0

        # 第1步 校验主播够不够
        sql_anchor = 'SELECT order_date,sum(order_s),sum(order_a),sum(order_b),' \
                     'sum(order_c),sum(order_d) FROM ads_package_info_schedule ' \
                     'where order_date<="{}" and order_date>="{}" GROUP BY order_date' \
            .format(end_time[0:10], begin_time[0:10])
        sql_anchor_all = 'SELECT invetoy_s,invetoy_a,invetoy_b,invetoy_c,invetoy_d from ads_anchor_invetoy'
        try:
            anchor_result = self.db_adm.execute(sql_anchor).fetchall()
            anchor_result_all = self.db_adm.execute(sql_anchor_all).first()
        except Exception as e:
            self.write_json(-1)
            # self.db_ads.close()
            self.db_adm.close()
            return

        anchor_dict = {r[0].isoformat(): r for r in anchor_result}
        start_date = begin_time[0:10]
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        s_all, a_all, b_all, c_all, d_all = anchor_result_all

        err = []
        for i in range(serving_meth):
            temp_day = datetime.timedelta(days=i)
            now = start_date + temp_day
            now = now.strftime("%Y-%m-%d")
            anchor_num = anchor_dict.get(now, (0, 0, 0, 0, 0, 0))
            _, order_s, order_a, order_b, order_c, order_d = anchor_num
            if s_all - order_s < s_day:
                err.append(
                    '{}日, S级别主播下单需要:{},实际库存{}\n'.format(
                        now, s_day, s_all - order_s))
            if a_all - order_a < a_day:
                err.append(
                    '{}日, A级别主播下单需要:{},实际库存{}\n'.format(
                        now, a_day, a_all - order_a))
            if b_all - order_b < b_day:
                err.append(
                    '{}日, B级别主播下单需要:{},实际库存{}\n'.format(
                        now, b_day, b_all - order_b))
            if c_all - order_c < c_day:
                err.append(
                    '{}日, C级别主播下单需要:{},实际库存{}\n'.format(
                        now, c_day, c_all - order_c))
            if d_all - order_d < d_day:
                err.append(
                    '{}日, D级别主播下单需要:{},实际库存{}\n'.format(
                        now, d_day, d_all - order_d))
        if err:
            self.db_ads.close()
            self.write_json(-1, ''.join(err))
            return

        # 第2步 先添加套餐
        package = ContractPackInfo()
        package.package_name = package_name
        package.adser = adser
        package.begin_time = begin_time
        package.end_time = end_time
        package.ads_play_num_desc = ''.join(ads_play_num_desc)
        package.serving_meth = serving_meth
        package.is_allow_repeat = is_allow_repeat
        package.anchor_need = s + a + b + c + d
        package.status = 1
        package.enable = 1
        package.rate = 100
        package.anchor_play_count = (s + a + b + c + d) * ads_play_num

        # package.anchor_play_count = ads_play_num
        json_desc = {"S": s, "A": a, "B": b, "C": c, "D": d}
        package.need_desc = json.dumps(json_desc)
        self.db_ads.add(package)
        try:
            self.db_ads.commit()
        except Exception as e:
            self.db_ads.rollback()
            self.db_ads.close()
            log.e(e)
            self.write_json(500, "系统错误")
            return

        # 第3步 添加日历schedule
        user = self.current_user
        start_date = begin_time[0:10]
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        for i in range(serving_meth):
            temp_day = datetime.timedelta(days=i)

            adscal = AdsPackageInfoSchedule()
            adscal.order_sche_name = package_name
            adscal.order_date = start_date + temp_day
            adscal.package_id = package.package_id
            adscal.order_s = s_day
            adscal.order_a = a_day
            adscal.order_b = b_day
            adscal.order_c = c_day
            adscal.order_d = d_day
            adscal.order_status = 1
            adscal.create_people = user['name']
            adscal.need_play_num = int(ads_play_num)
            adscal.create_time = datetime.datetime.now()
            self.db_adm.add(adscal)
        try:
            self.db_adm.commit()
            # self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_adm.rollback()
            # self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            # self.db_ads.close()
            self.db_adm.close()


# 获取某个套餐详情
class GetPackageByIdHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        package_id = self.get_argument('package_id')
        data = self.db_ads.query(ContractPackInfo).filter(
            ContractPackInfo.package_id == package_id).first()
        self.db_ads.close()
        if data:
            self.write_raw_json(
                json.loads(
                    json.dumps(
                        data,
                        cls=AlchemyEncoder)))
        else:
            self.write_raw_json([])


# 获取主播库存
class GetAnchorInvetoy(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self):
        type = self.get_argument('type')
        date = self.get_argument('date')
        sql = 'SELECT invetoy_id,invetoy_s,invetoy_a,invetoy_b,' \
              'invetoy_c,invetoy_d,create_time,log_time from ads_anchor_invetoy'
        anch_results = self.db_adm.execute(sql).first()
        anch_dict = {'S': 0, "A": 0, "B": 0, "C": 0, "D": 0}
        if type is '1':
            sch_results = self.db_adm.query(AdsPackageInfoSchedule). \
                filter(AdsPackageInfoSchedule.order_date == date).all()
            for ret in sch_results:
                anch_dict['S'] = anch_dict['S'] + \
                    ret.order_s if ret.order_s else anch_dict['S']
                anch_dict['A'] = anch_dict['A'] + \
                    ret.order_a if ret.order_a else anch_dict['A']
                anch_dict['B'] = anch_dict['B'] + \
                    ret.order_b if ret.order_b else anch_dict['B']
                anch_dict['C'] = anch_dict['C'] + \
                    ret.order_c if ret.order_c else anch_dict['C']
                anch_dict['D'] = anch_dict['D'] + \
                    ret.order_d if ret.order_d else anch_dict['D']
        _, invetoy_s, invetoy_a, invetoy_b, invetoy_c, invetoy_d, _, _ = anch_results
        anch_dict['S_all'] = invetoy_s
        anch_dict['A_all'] = invetoy_a
        anch_dict['B_all'] = invetoy_b
        anch_dict['C_all'] = invetoy_c
        anch_dict['D_all'] = invetoy_d
        # self.db_ads.close()
        self.db_adm.close()
        self.write_json(0, '', anch_dict)


# 主播库存
class AnchorStock(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("/ads_manager/ads_caldar/anchorstock.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        date = self.get_argument('date')
        start = datetime.datetime.strptime(date, "%Y-%m")
        month_time = datetime.datetime(
            month=start.month + 1, year=start.year, day=1)
        end_date = month_time.strftime("%Y-%m-%d")
        start_date = date + '-01'

        sql = 'SELECT invetoy_id,invetoy_s,invetoy_a,invetoy_b,' \
              'invetoy_c,invetoy_d from ads_anchor_invetoy'
        anch_results = self.db_adm.execute(sql).first()
        _, invetoy_s, invetoy_a, invetoy_b, invetoy_c, invetoy_d = anch_results
        anchor_all = {'s': invetoy_s, 'a': invetoy_a,
                      'b': invetoy_b, 'c': invetoy_c, 'd': invetoy_d}

        sql = 'SELECT order_date,sum(order_s),sum(order_a),sum(order_b),sum(order_c),' \
              'sum(order_d) from  ads_package_info_schedule ' \
              'where order_date>="{}" and order_date<"{}" GROUP BY order_date  ORDER BY order_date'.format(start_date,
                                                                                                           end_date)

        results = self.db_adm.execute(sql).fetchall()

        # self.db_ads.close()
        self.db_adm.close()
        lst = list()
        head = [
            'order_date',
            'order_s',
            'order_a',
            'order_b',
            'order_c',
            'order_d']
        for ret in results:
            order_date, order_s, order_a, order_b, order_c, order_d = ret
            order_date = order_date.isoformat()
            lst.append(dict(zip(head, (order_date, str(order_s), str(
                order_a), str(order_b), str(order_c), str(order_d)))))

        data = {}
        data['all'] = anchor_all
        data['day'] = lst
        self.write_json(0, '', data)


class AnchorAgentMapHander(SwxJsonHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render("/ads_manager/anchor/anchor_agent_maped.mako")

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = 'SELECT  m.agent_user_map_id,m.user_id,g.agent_name,m.plat_id,m.room_id,m.comment,m.price,m.createtime,m.rate ' \
                  'FROM	ads_agent_user_map m LEFT JOIN ads_agent_info g ON m.agent_id = g.agent_id where 1=1'
            filter = args["filter"]
            agent_name = filter.get('agent_name', None)
            room_id = filter.get('room_id', None)
            anchor_name = filter.get('anchor_name', None)
            user_id = filter.get('user_id', None)
            if agent_name:
                sql = sql + " and g.agent_name like '%" + agent_name.strip() + "%' "
            if room_id:
                sql = sql + " and m.room_id like '%" + room_id.strip() + "%' "
            if anchor_name:
                sql = sql + " and m.comment like '%" + anchor_name.strip() + "%' "
            if user_id:
                sql = sql + " and m.user_id like '%" + user_id.strip() + "%' "

            offset = " ORDER BY m.agent_user_map_id DESC LIMIT {},{}" .format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'agent_user_map_id',
                'user_id',
                'agent_name',
                'plat_id',
                'room_id',
                'comment',
                'price',
                'createtime',
                'rate']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['createtime'] = temp['createtime'].isoformat(
                ) if temp['createtime'] else ''
                temp['price'] = str(
                    (temp['price']).quantize(
                        Decimal('0.00'))) if temp['price'] else 0
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


class AnchorAgentMapExportHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            sql = 'SELECT  m.agent_user_map_id,g.agent_name,m.plat_id,m.room_id,m.user_id,m.comment,m.price,m.createtime,m.rate ' \
                  'FROM	ads_agent_user_map m LEFT JOIN ads_agent_info g ON m.agent_id = g.agent_id where 1=1'
            filename = ''
            agent_name = self.get_argument('agent_name', None)
            room_id = self.get_argument('room_id', None)
            anchor_name = self.get_argument('anchor_name', None)
            user_id = self.get_argument('user_id', None)
            if agent_name:
                sql = sql + " and g.agent_name like '%" + agent_name.strip() + "%' "
            if room_id:
                sql = sql + " and m.room_id like '%" + room_id.strip() + "%' "
            if anchor_name:
                sql = sql + " and m.comment like '%" + anchor_name.strip() + "%' "
            if user_id:
                sql = sql + " and m.user_id like '%" + user_id.strip() + "%' "
            offset = " ORDER BY m.agent_user_map_id DESC "
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = ['agent_user_map_id', '经纪公司名称', '平台号', '房间号', '用户ID',
                    '主播昵称', '结算价格', '经纪公司收入比例']
            els_url = exportAnchor(datas, head, filename)
            self.write_json(0, data=els_url)
            return
        except Exception as e:
            log.e(e)
            self.write_json(-1, 'excel导出失败')
        finally:
            self.db_ads.close()


class AgnetMap4AllHander(SwxJsonHandler):
    def get(self, *args, **kwargs):
        ngi_list = self.db_ads.query(AgentInfo) \
            .order_by(AgentInfo.agent_id.desc()).all()
        lst = list()
        for ngi in ngi_list:
            lst.append(json.loads(json.dumps(ngi, cls=AlchemyEncoder)))
        self.write_raw_json(lst)
        self.db_ads.close()


class AdsAgentUserMapAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        agent_id = args["agent_id"]
        plat_id = args["plat_id"]
        room_id = args["room_id"]
        price = args["price"]
        comment = args["comment"]
        user_id = args["user_id"]
        rate = args["rate"]

        agentmap = AdsAgentUserMap()
        agentmap.agent_id = agent_id
        agentmap.plat_id = plat_id
        agentmap.room_id = room_id
        agentmap.price = price
        agentmap.comment = comment
        agentmap.user_id = user_id
        agentmap.rate = rate
        agentmap.createtime = datetime.datetime.now()
        self.db_ads.add(agentmap)
        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class AdsAgentUserMapEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        agent_user_map_id = args["agent_user_map_id"]
        price = args["price"]
        try:
            self.db_ads.query(AdsAgentUserMap). filter(
                AdsAgentUserMap.agent_user_map_id == agent_user_map_id) .update(
                {
                    AdsAgentUserMap.price: Decimal(price)})
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class AdsAgentUserIncomeRateEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        agent_user_map_id = args["agent_user_map_id"]
        rate = args["rate"]
        try:
            self.db_ads.query(AdsAgentUserMap). filter(
                AdsAgentUserMap.agent_user_map_id == agent_user_map_id) .update(
                {
                    AdsAgentUserMap.rate: Decimal(rate)})
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "更新失败")
        finally:
            self.db_ads.close()


class AdsAgentUserMapDeleteHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument('args')
        if args:
            args = json.loads(args)
            ids = args.get('ids')
        self.db_ads.query(AdsAgentUserMap).filter(
            AdsAgentUserMap.agent_user_map_id.in_(ids)).delete(
            synchronize_session=False)
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(-1)
        finally:
            self.db_ads.close()


class AdsAgentUserAddHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        args = self.get_argument('args', None)
        if args is not None:
            args = json.loads(args)
        agent_name = args["agent_name"]
        agent = AgentInfo()
        agent.agent_name = agent_name
        self.db_ads.add(agent)
        try:
            self.db_ads.commit()
            self.write_json(0, "success")
        except Exception as e:
            self.db_ads.rollback()
            log.e(e)
            self.write_json(500, "系统错误")
        finally:
            self.db_ads.close()


class PlaylogScreenEditHander(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render("/ads_manager/playlog_screen/playlog_screen.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        if "screen_type" in self.request.arguments:
            screen_type = self.get_argument('screen_type', None)
        if "screen_path" in self.request.arguments:
            screen_path = self.get_argument('screen_path', None)
        if "record_path" in self.request.arguments:
            record_path = self.get_argument('record_path', None)

        play_ids = self.get_argument('play_ids', None)
        edit_type = self.get_argument('edit_type', None)
        # 批量修改
        if edit_type == "1":
            play_ids = play_ids.split(",")
            for play_id in play_ids:
                play_log = self.db_ads.query(TaskPlayLog).filter(
                    TaskPlayLog.play_id == play_id.strip()).first()
                if play_log:
                    record_path, record_path_old = play_log.record_path, play_log.record_path_old
                    screen_shot_path, screen_shot_path_old = play_log.screen_shot_path, play_log.screen_shot_path_old
                    if screen_type == "1":
                        play_log.record_path_old, play_log.record_path = \
                            record_path, record_path_old
                    elif screen_type == "2":
                        play_log.screen_shot_path_old, play_log.screen_shot_path = \
                            screen_shot_path, screen_shot_path_old
                    elif screen_type == "3":
                        play_log.record_path_old, play_log.record_path = \
                            record_path, record_path_old
                        play_log.screen_shot_path_old, play_log.screen_shot_path = \
                            screen_shot_path, screen_shot_path_old
        elif edit_type == '2':
            play_log = self.db_ads.query(TaskPlayLog).filter(
                TaskPlayLog.play_id == play_ids.strip()).first()
            if play_log:
                play_log.record_path = record_path
                play_log.screen_shot_path = screen_path
        try:
            self.db_ads.commit()
            self.write_json(0)
        except Exception as e:
            log.e(e)
            self.db_ads.rollback()
            self.write_json(-1)
        finally:
            self.db_ads.close()


class PlaylogFindByIdHander(SwxJsonHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        play_id = self.get_argument('play_id', None)
        data = self.db_ads.query(TaskPlayLog.screen_shot_path,
                                 TaskPlayLog.record_path).filter(
            TaskPlayLog.play_id == play_id).first()
        self.db_ads.close()
        screen_shot_path = ''
        record_path = ''
        if data:
            screen_shot_path, record_path = data
        self.write_json(
            0, "", {
                "screen_shot_path": screen_shot_path, "record_path": record_path})

# 主播信用分管理


class CreditScoreListHandler(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        self.render(
            "/ads_manager/user_credit_score/user_credit_score_list.mako")

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = "SELECT user_id,credit_score from ads_user_credit_score where 1=1"
            filter = args["filter"]
            user_id = ""
            if "search" in filter.keys():
                user_id = filter["search"]
            if user_id:
                sql = sql + " and user_id like '%" + user_id.strip() + "%'"
            nick_name=filter["nick_name"]
            if nick_name:
                sql_nick_name=("SELECT user_id from base_room where room_nickname like '%{}%' "
                               "UNION  SELECT user_id from weak_auth_room where room_nickname "
                               "like '%{}%'").format(nick_name,nick_name)
                user_ids=self.db_guild.execute(sql_nick_name).fetchall()
                user_ids=[str(u[0]) for u in user_ids]
                if user_ids:
                    sql = sql + " and user_id in ({}) ".format(",".join(user_ids))
            offset = " ORDER BY log_time DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = ['user_id', 'credit_score']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                user_id = data[0]
                user_info = app_map().get_user_info(user_id)
                if user_info:
                    temp['name'] = user_info[1]
                    temp['room_url'] = user_info[2]
                    temp['platform_id'] = user_info[3]
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()


class CreditScoreEditHandler(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        args = self.get_argument("args", None)
        user_ids = None
        summand = None
        action = None
        err_user_ids = []
        if args:
            args = json.loads(args)
            user_ids = args.get("user_ids", None)
            summand = args.get("summand", None)
            action = args.get("action", None)
        if not user_ids:
            self.write_json(-1, 'miss param user_ids')
            return
        user_ids = user_ids.split(",")
        for user_id in user_ids:
            try:
                user_id = int(user_id) if user_id else None
                summand = int(summand) if summand else None
                data = json.dumps(
                    {
                        "UserId": user_id,
                        'Summand': summand,
                        'Action': action,
                        'TriggerTime': int(
                            time.time() *
                            1000)}).encode(
                    encoding='utf-8')
                ssl._create_default_https_context = ssl._create_unverified_context
                req = request.Request(
                    url="https://xhlgw.xiaohulu.com:40000/api/v1/credit/record/add_custom_made",
                    data=data)
                res = request.urlopen(req)
                if res is not None:
                    ret = res.read().decode('utf-8')
                    data = json.loads(ret)
                    if data["code"] != 0:
                        err_user_ids.append(user_id)
            except Exception as e:
                log.e(e)
                err_user_ids.append(user_id)
        if err_user_ids:
            self.write_json(-1, '', ",".join(err_user_ids))
        else:
            self.write_json(0)


class CreditScoreDetailHandler(SwxJsonHandler):
    @tornado.web.authenticated
    @permision
    def get(self, *args, **kwargs):
        user_id_select = ''
        if 'user_id' in self.request.arguments:
            user_id_select = self.get_argument('user_id')
        self.render(
            "/ads_manager/user_credit_score_detail/user_credit_score_detail.mako",
            user_id_select=user_id_select)

    @tornado.web.authenticated
    @permision
    def post(self, *args, **kwargs):
        limit, args = self.get_pages_args()
        try:
            sql = "SELECT id,user_id,`type`,result,cur_score,trigger_time,create_time,`action` from ads_user_credit_score_detail_log where 1=1"

            filter = args["filter"]
            user_id = filter.get('search', None)
            trigger_begintime = filter.get('trigger_begintime', None)
            trigger_endtime = filter.get('trigger_endtime', None)
            create_begintime = filter.get('create_begintime', None)
            create_endtime = filter.get('create_endtime', None)
            user_id_select = filter.get('user_id_select', None)
            user_id = user_id if user_id else user_id_select
            if user_id:
                sql = sql + " and user_id=" + user_id.strip() + ""
            if trigger_begintime:
                sql = sql + " and trigger_time>='{}'".format(trigger_begintime)
            if trigger_endtime:
                sql = sql + \
                    " and trigger_time<='{} 23:59:59'".format(trigger_endtime)
            if create_begintime:
                sql = sql + " and create_time>='{}'".format(create_begintime)
            if create_endtime:
                sql = sql + \
                    " and create_time<='{} 23:59:59'".format(create_endtime)

            offset = " ORDER BY trigger_time DESC LIMIT {},{}".format(
                limit['page_index'] * limit['per_page'], limit['per_page'])
            datas = self.db_ads.execute(sql + offset).fetchall()
            head = [
                'id',
                'user_id',
                'type',
                'result',
                'cur_score',
                'trigger_time',
                'create_time',
                'action']
            lst = list()
            for data in datas:
                temp = dict(zip(head, data))
                temp['trigger_time'] = temp['trigger_time'].isoformat() or ''
                temp['create_time'] = temp['create_time'].isoformat() or ''
                lst.append(temp)
            count = self.db_ads.execute(
                "select count(*) from({}) as count_data".format(sql)).scalar()
            ret = self.set_page_params(count, limit, lst)
            self.write_json(0, data=ret)
        except Exception as e:
            log.e(e)
            self.write_json(-1, '查询失败')
        finally:
            self.db_ads.close()