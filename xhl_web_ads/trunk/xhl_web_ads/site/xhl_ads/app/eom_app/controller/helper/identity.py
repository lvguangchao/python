from eom_app.orm.tables import TLogWithdrawAnchor, TUserAccountIdentity, \
    BaseUser, RoomInfo, TIdentityPersonal, TaskPlayLog, BaseRoom, BaseUnion, AgentInfo, User, AdsUnionGroup

from eom_app.orm.db import app_db
from  eom_app.orm.JSONEncoder import AlchemyEncoder
import json
import datetime


# 本类主要用户构建 缓存字典


class LabelClass(object):
    def __init__(self):
        self._withdraw = None
        self._baseuser = None
        self._baseuserroom = None
        self._adsuniongroup = None
        self._baseunion = None
        self._agentinfo = None
        self._groupId2unionIdMap = None  # xhl_ads数据库  ads_union_group_id  对应  union_id 的map
        self._unionid2nameMap = None  # xhl_guild 数据库  union_id  对应  union_name 的map
        self._name2unionidMap = None  # xhl_guild 数据库  union_id  对应  union_name 的map
        self._roomInfoMap = None
        self._unionList = None
        self._playLogMap = None
        self._AdmPlatMap = None
        self._AdmAgentMap = None
        self._LoginUserMap = None
        self._PackageMap = None
        self._plat_map = None
        self._plat_list = None
        self._sessionfactory = None
        self._sessionfactory_ads = None
        self._sessionfactory_wealth = None
        self._sessionfactory_guild = None
        self._sessionfactory_ads_adm = None
        self._user_info = None


    @property
    def db(self):
        if not self._sessionfactory:
            self._sessionfactory = app_db().create_DBSession()
        return self._sessionfactory

    @property
    def db_ads(self):
        if not self._sessionfactory_ads:
            self._sessionfactory_ads= app_db().create_Ads_DBSession()
        return self._sessionfactory_ads

    @property
    def db_wealth(self):
        if not self._sessionfactory_wealth:
            self._sessionfactory_wealth = app_db().create_Wealth_DBSession()
        return self._sessionfactory_wealth

    @property
    def db_guild(self):
        if not self._sessionfactory_guild:
            self._sessionfactory_guild = app_db().create_guild_DBSession()
        return self._sessionfactory_guild

    @property
    def db_adm(self):
        if not self._sessionfactory_ads_adm:
            self._sessionfactory_ads_adm = app_db().create_adm_DBSession()
        return self._sessionfactory_ads_adm

    def TLogWithdrawAnchor(self):
        if self._withdraw is None:
            session = None
            try:
                # print(datetime.datetime.now())
                result = self.db_wealth.query(TIdentityPersonal).all()
                # print(datetime.datetime.now())
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        temp['identity_id'] = info.identity_id
                        # temp['user_id'] = info.user_id
                        temp['verify_status'] = info.verify_status
                        temp['status'] = info.status
                        temp['id_user_name'] = info.id_user_name
                        temp['id_number'] = info.id_number
                        temp['bank_name'] = info.bank_name
                        temp['bank_card_number'] = info.bank_card_number
                        temp['hold_user_name'] = info.hold_user_name
                        temp['bank_sub_name'] = info.bank_sub_name
                        temp['id_img_front'] = info.id_img_front
                        temp['qq_number'] = info.qq_number
                        temp['id_img_back'] = info.id_img_back
                        ret[info.user_id] = temp
                    # print(datetime.datetime.now())
                    self._withdraw = ret
                    return ret
                return None
            except Exception as e:

                return None
            finally:
                if session is not None:
                    session.close()
        else:
            return self._withdraw

    def Baseuser(self):
        if self._baseuser is None:
            session = None
            try:
                result = self.db_guild.query(BaseUser.u_mobile_number, BaseUser.user_id).all()
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        # temp['user_id'] = info.user_id
                        temp['u_mobile_number'] = info.u_mobile_number
                        ret[info.user_id] = temp
                    self._baseuser = ret
                    return ret
                return None
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_guild.close()
        else:
            return self._baseuser

    def Baseuserroom(self):
        if self._baseuserroom is None:
            session = None
            try:
                result = self.db_guild.query(BaseUser.user_id, BaseUser.u_nickname, BaseRoom.room_id,
                                             BaseRoom.platform_id,BaseRoom.room_url).outerjoin(BaseRoom,
                                                                             BaseUser.user_id == BaseRoom.user_id).all()
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        temp['room_id'] = info.room_id
                        temp['u_nickname'] = info.u_nickname
                        temp['platform_id'] = info.platform_id
                        temp['room_url'] = info.room_url
                        ret[info.user_id] = temp
                    self._baseuserroom = ret
                    return ret
                return None
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_guild.close()
        else:
            return self._baseuserroom

    def Adsuniongroup(self):
        if self._adsuniongroup is None:
            session = None
            try:
                result = self.db_ads.query(AdsUnionGroup.user_id,
                                           AdsUnionGroup.source_link, AdsUnionGroup.union_id
                                           ).filter(AdsUnionGroup.apply_status != 50).all()
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        temp['source_link'] = info.source_link
                        temp['union_id'] = info.union_id
                        ret[str(info.user_id)] = temp
                    self._adsuniongroup = ret
                    return ret
                return None
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_ads.close()
        else:
            return self._adsuniongroup

    def Baseunion(self):
        if self._baseunion is None:
            session = None
            try:
                result = self.db_guild.query(BaseUnion.union_id, BaseUnion.union_name).all()
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        temp['union_name'] = info.union_name
                        ret[info.union_id] = temp
                    self._baseunion = ret
                    return ret
                return None
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_guild.close()
        else:
            return self._baseunion

    def AgentInfo(self):
        if self._agentinfo is None:
            session = None
            try:
                result = self.db_ads.query(AgentInfo.agent_id, AgentInfo.agent_name).all()
                ret = dict()
                if result:
                    for info in result:
                        temp = dict()
                        temp['agent_name'] = info.agent_name
                        ret[info.agent_id] = temp
                    self._agentinfo = ret
                    return ret
                return None
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_ads.close()
        else:
            return self._agentinfo

    # xhl_guild 数据库  union_id   对应  union_name 的map
    # xhl_guild 数据库  union_name 对应 union_id  的map
    def unionid2nameMap(self):
        if self._unionid2nameMap is None or self._name2unionidMap is None:
            try:
                sql = 'select union_id,union_name from base_union'
                results = self.db_guild.execute(sql).fetchall()
                unionid2nameMap = dict()
                name2unionidMap = dict()
                for r in results:
                    if r[0] is not None and r[0] != "":
                        unionid2nameMap[r[0]] = r[1]
                    if r[1] is not None and r[1] != "":
                        name2unionidMap[r[1]] = r[0]
                self._unionid2nameMap = unionid2nameMap
                self._name2unionidMap = name2unionidMap
                return unionid2nameMap, name2unionidMap
            except Exception as e:
                print(e)
                return None
            finally:
                self.db_guild.close()
        else:
            return self._unionid2nameMap, self._name2unionidMap

    def getUnionName(self, union_id):
        if not union_id:
            return ''
        unionid2nameMap, _ = self.unionid2nameMap()
        if union_id in unionid2nameMap:
            return unionid2nameMap[union_id]
        else:
            sql = 'select union_id,union_name from base_union where union_id={}'.format(union_id)
            result = self.db_guild.execute(sql).first()
            self.db_guild.close()
            if result:
                self._unionid2nameMap[result[0]] = result[1]
                return result[1]
            else:
                return ''

    def getRoomInfo(self):
        if self._roomInfoMap is None:
            roomInfoMap = dict()
            try:
                result = self.db_ads.query(RoomInfo).all()
                if result:
                    # roomInfoMap={'{}_{}'.format(info.room_id,info.platform_id):  json.loads(json.dumps(info, cls=AlchemyEncoder)) for info in result}
                    for info in result:
                        temp = json.loads(json.dumps(info, cls=AlchemyEncoder))
                        key='{}_{}'.format(info.room_id,info.platform_id)
                        roomInfoMap[key] = temp
                    self._roomInfoMap = roomInfoMap
                    return roomInfoMap
                return None
            except Exception as e:
                return None
            finally:
                self.db_ads.close()
        else:
            return self._roomInfoMap

    def getRoomInfoById(self, roomId,plat_id):
        key = '{}_{}'.format(roomId, plat_id)
        if not roomId or not plat_id:
            return ""
        roomInfoMap = self.getRoomInfo()
        if key in roomInfoMap:
            return roomInfoMap[key]
        else:
            try:
                result = self.db_ads.query(RoomInfo).filter(RoomInfo.room_id == roomId,RoomInfo.platform_id==plat_id).first()
                if result:
                    temp = json.loads(json.dumps(result, cls=AlchemyEncoder))

                    self._roomInfoMap[key] = temp
                    return self._roomInfoMap[key]
                else:
                    return ''
            finally:
                self.db_ads.close()

    def getUnionList(self):
        if self._unionList is None:
            sql = 'select union_id,union_name from  base_union '
            try:
                result = self.db_guild.execute(sql).fetchall();
                lst = list()
                for ret in result:
                    lst.append({"union_id": ret[0], "union_name": ret[1]})
            finally:
                self.db_guild.close()
                self._unionList = lst
            return lst
        else:
            return self._unionList

    def getPlayLogMap(self):
        if self._playLogMap is None:
            result = []
            try:
                sql = 'SELECT p.play_id,p.record_path,p.screen_shot_path,p.popularity ' \
                      ' from ads_task_play_log p'
                result = self.db_ads.execute(sql).fetchall();
            finally:
                self.db_ads.close()
            playLogMap = {ret['play_id']: ret for ret in result}
            self._playLogMap = playLogMap
            return playLogMap
        else:
            return self._playLogMap

    def getPlayLog(self, play_id):
        playLogMap = self.getPlayLogMap()
        if play_id in playLogMap:
            return playLogMap[play_id]
        else:
            try:
                sql = ' SELECT p.play_id,p.record_path,p.screen_shot_path,' \
                      'p.popularity from ads_task_play_log p  where play_id={}'.format(int(play_id))
                result = self.db_ads.execute(sql).fetchone()
                if result:
                    self._playLogMap[result['play_id']] = result
                    return self._playLogMap[play_id]
                else:
                    return ''
            finally:
                self.db_ads.close()

    def getAdmPlatMap(self):
        if self._AdmPlatMap is None:
            sql = 'select plat_id,plat_name,plat_rate from adm_platform'
            try:
                plat_result = self.db_adm.execute(sql)
            finally:
                self.db_adm.close()
            platMap = {p['plat_id']: p for p in plat_result}
            self._AdmPlatMap = platMap
            return platMap
        else:
            return self._AdmPlatMap

    def getAdmPlat(self, plat_id):
        AdmPlatMap = self.getAdmPlatMap()
        if plat_id in AdmPlatMap:
            return AdmPlatMap[plat_id]
        else:
            try:
                sql = 'select plat_id,plat_name,plat_rate from adm_platform where plat_id={}'.format(plat_id)
                result = self.db_adm.execute(sql).fetchone()
                if result:
                    self._AdmPlatMap[result['plat_id']] = result
                    return self._AdmPlatMap[plat_id]
                else:
                    return ''
            finally:
                self.db_adm.close()

    def getAdmAgentMap(self):
        if self._AdmAgentMap is None:
            sql = 'SELECT agent_id,agent_name from ads_agent_info'
            try:
                agent_result = self.db_ads.execute(sql)
            finally:
                self.db_ads.close()
            agentMap = {p['agent_id']: p for p in agent_result}
            self._AdmAgentMap = agentMap
            return agentMap
        else:
            return self._AdmAgentMap

    def getAdmAgent(self, agent_id):
        AdmAgentMap = self.getAdmAgentMap()
        if agent_id in AdmAgentMap:
            return AdmAgentMap[agent_id]
        else:
            try:
                sql = 'SELECT agent_id,agent_name from ads_agent_info where agent_id={}'.format(agent_id)
                result = self.db_ads.execute(sql).fetchone()
                if result:
                    self._AdmAgentMap[result['agent_id']] = result
                    return self._AdmPlatMap[agent_id]
                else:
                    return ''
            finally:
                self.db_ads.close()

    ##后台系统 =》 登陆用户
    def getLoginUserMap(self):
        if not self._LoginUserMap:
            rets = self.db_adm.query(User).all()
            loginUserMap = {user.user_id: user for user in rets}
            self._LoginUserMap = loginUserMap
            self.db_adm.close()
            return loginUserMap
        else:
            return self._LoginUserMap

    def getLoginUser(self, userId):
        if not userId:
            return ''
        self.getLoginUserMap()
        if userId in self._LoginUserMap:
            return self._LoginUserMap[userId]
        else:
            user = self.db_adm.query(User).filter(User.user_id == userId).first()
            self._LoginUserMap[user.user_id] = user
            self.db_adm.close()
            return user

    def getPackageMap(self):
        if self._PackageMap is None:
            sql = 'select package_id,package_name from ads_contract_package_info'
            try:
                plat_result = self.db_ads.execute(sql)
            finally:
                self.db_ads.close()
            PackageMap = {p['package_id']: p for p in plat_result}
            self._PackageMap = PackageMap
            return PackageMap
        else:
            return self._PackageMap

    def getPack(self, plat_id):
        if not plat_id:
            return ''
        PlatMap = self.getPackageMap()
        if plat_id in PlatMap:
            return PlatMap[plat_id]
        else:
            try:
                sql = 'select package_id,package_name from ads_contract_package_info ' \
                      ' WHERE  package_id={}'.format(plat_id)
                result = self.db_ads.execute(sql).fetchone()
                if result:
                    self._PackageMap[result['package_id']] = result
                    return self._PackageMap[plat_id]
                else:
                    return ''
            finally:
                self.db_ads.close()

    def get_role_menu(self, role_id):
        sql = 'SELECT m.source_id from adm_role r LEFT ' \
              ' JOIN adm_role_menu rm ON r.role_id=rm.role_id' \
              ' LEFT JOIN adm_menu m ON rm.menu_id=m.menu_id WHERE ' \
              ' r.role_id={}'.format(role_id)
        try:
            results = self.db_adm.execute(sql).fetchall()
        except Exception as e:
            results = []
        finally:
            self.db_adm.close()
        if results:
            sources = [r[0] for r in results if r[0]]
        else:
            sources = []
        return sources

    def get_menu_scource(self, role_id):

        sql = 'SELECT s.source_url from adm_sys_user u LEFT JOIN ' \
              ' adm_role_menu m on u.role_id=m.role_id ' \
              ' LEFT JOIN adm_menu_source s on s.menu_id=m.menu_id ' \
              ' where u.role_id={}'.format(role_id)

        try:
            results = self.db_adm.execute(sql).fetchall()
        except Exception as e:
            results = []
        finally:
            self.db_adm.close()
        if results:
            sources = [r[0] for r in results if r[0]]
        else:
            sources = []
        return sources

    # 获取平台信息,进行缓存到内存
    def get_platform_map_list(self):
        if not self._plat_map or not self._plat_list:
            sql='select id plat_id,name plat_name from base_platforms_guild'
            try:
                results=self.db_guild.execute(sql).fetchall()
                plat_map={r[0]:r[1] for r in results}
                plat_list=[{'plat_id':r[0],'plat_name':r[1]} for r in results]
                self._plat_map=plat_map
                self._plat_list=plat_list
            finally:
                self.db_guild.close()
        return self._plat_map, self._plat_list

    def get_platform_name(self,plat_id):
        if not plat_id:
            return ''
        elif plat_id in self._plat_map:
            return self._plat_map.get(plat_id)
        else:
            sql='select id plat_id,name plat_name from base_platforms_guild where id={}'.format(plat_id)
            data=self.db_guild.execute(sql).first()
            if data:
                plat_id,plat_name=data
                self._plat_map[plat_id]=plat_name
                self._plat_list.append({plat_id:plat_name})
                return plat_name
            else:
                return ''

    # 用户基本信息map，叠加base_room,weak_auth_room
    def init_user_info_map(self):
        if not self._user_info:
            base_room=None
            user_info=dict()
            try:
                sql_base='SELECT user_id,room_nickname as name,room_url,platform_id from base_room'
                sql_weak='SELECT  user_id,room_nickname as name,room_url,platform_id from weak_auth_room where user_id not in (SELECT user_id from base_room)'
                base_room=self.db_guild.execute(sql_base).fetchall()
                weak_room=self.db_guild.execute(sql_weak).fetchall()
                base_room.extend(weak_room)
            finally:
                self.db_guild.close()
            for r in base_room:
                user_id=r[0]
                user_info[user_id]=r
            self._user_info=user_info


    def get_user_info(self,user_id):
        if not user_id:
            return None
        elif user_id in self._user_info:
            return self._user_info[user_id]
        else:
            try:
                sql = 'SELECT user_id,room_nickname as name,room_url,platform_id from base_room where user_id={}'.format(user_id)
                data = self.db_guild.execute(sql).first()
                if data:
                    user_id=data[0]
                    self._user_info[user_id]=data
                else:
                    sql_weak='SELECT  user_id,room_nickname as name,room_url,platform_id from weak_auth_room where user_id={}'.format(user_id)
                    data = self.db_guild.execute(sql_weak).first()
                    if data:
                        user_id = data[0]
                        self._user_info[user_id] = data

                if user_id in self._user_info:
                    return self._user_info[user_id]
                else:
                    return None
            except Exception as e:
                self.db_guild.rollback()
                return None
            finally:
                self.db_guild.close()


_withdraw = LabelClass()

del LabelClass


def app_map():
    global _withdraw
    return _withdraw
