from sqlalchemy import Column, String, Integer, VARCHAR, ForeignKey, Float, \
    DateTime, Text, Time, Numeric, Enum, text, Date, TIMESTAMP, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from .db import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'adm_sys_user'
    user_id = Column(Integer, primary_key=True)
    role_id = Column(Integer)
    user_name = Column(VARCHAR(20))
    user_pwd = Column(VARCHAR(40))
    createtime = Column(DateTime())
    enable = Column(Integer)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsInfo(Base):
    __tablename__ = 'ads_info'
    ads_id = Column(Integer, primary_key=True)
    ads_name = Column(VARCHAR(255))
    ads_time = Column(Integer)
    ads_materialurl = Column(VARCHAR(255))
    ads_materialurl_md5 = Column(VARCHAR(32))
    ads_thumbnailurl = Column(VARCHAR(255))
    ads_thumbnailurl_md5 = Column(VARCHAR(32))
    description = Column(VARCHAR(255))
    create_time = Column(VARCHAR(255))
    ads_contents = Column(VARCHAR(255))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class NeedInfo(Base):
    __tablename__ = 'ads_need_info'
    need_id = Column(Integer, primary_key=True)
    package_id = Column(Integer)
    need_play_type = Column(Integer)
    anchor_level = Column(VARCHAR(11))
    position = Column(VARCHAR(255))
    position_count = Column(Integer)
    ads_id = Column(VARCHAR(11))
    enable = Column(Integer)
    description = Column(VARCHAR(255))
    need_name = Column(VARCHAR(32))
    ads_interval = Column(VARCHAR(255))
    # ads_need_group_id = Column(Integer)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AgentInfo(Base):
    __tablename__ = 'ads_agent_info'
    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(VARCHAR(128))
    createtime = Column(TIMESTAMP)
    logtime = Column(TIMESTAMP)


class ContractPackInfo(Base):
    __tablename__ = 'ads_contract_package_info'
    package_id = Column(Integer, primary_key=True)
    affairs_num = Column(VARCHAR(255))
    package_name = Column(VARCHAR(11))
    contract_id = Column(Integer)
    package_price = Column(Numeric())
    begin_time = Column(DateTime())
    end_time = Column(DateTime())
    anchor_need = Column(Integer)
    anchor_play_count = Column(Integer)
    # 业务结算
    anchor_balance = Column(Numeric)
    union_balance = Column(Numeric)
    plat_balance = Column(Numeric)
    agent_balance = Column(Numeric)
    # 关账之前的结算
    anchor_balance_close = Column(Numeric)
    union_balance_close = Column(Numeric)
    plat_balance_close = Column(Numeric)
    agent_balance_close = Column(Numeric)
    # 关账之后的计算
    anchor_balance_other = Column(Numeric)
    union_balance_other = Column(Numeric)
    plat_balance_other = Column(Numeric)
    agent_balance_other = Column(Numeric)

    balance_last_time = Column(DateTime())
    status = Column(Integer)
    enable = Column(Integer)
    need_desc = Column(Text)
    ads_play_num_desc = Column(VARCHAR(255))
    serving_meth = Column(Integer)
    is_allow_repeat = Column(Integer)
    adser = Column(Integer)
    create_time = Column(DateTime())
    log_time = Column(DateTime())
    rate = Column(Integer)


class AdsContractInfo(Base):
    __tablename__ = 'ads_contract_info'
    contract_id = Column(Integer, primary_key=True)
    contract_name = Column(VARCHAR(255))
    contract_price = Column(Integer)
    adsver_id = Column(Numeric)
    contract_desc = Column(VARCHAR(255))
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)


class NeedGroupInfo(Base):
    __tablename__ = 'ads_group_info'
    ads_need_group_id = Column(Integer, primary_key=True)
    group_name = Column(VARCHAR(32))
    comment = Column(VARCHAR(32))
    anchor_level = Column(VARCHAR(11))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsConfigAnchorWhitelist(Base):
    __tablename__ = 'ads_config_anchor_listwhite'
    id = Column(Integer, primary_key=True)
    plat_id = Column(Integer)
    room_id = Column(VARCHAR(36))
    ads_schedule_id = Column(VARCHAR(32))
    comment = Column(VARCHAR(32))
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsConfigAnchorBlacklist(Base):
    __tablename__ = 'ads_config_anchor_listblack'
    id = Column(Integer, primary_key=True)
    plat_id = Column(Integer)
    room_id = Column(VARCHAR(36))
    ads_schedule_id = Column(VARCHAR(32))
    comment = Column(VARCHAR(32))
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class TLogWithdrawAnchor(Base):
    __tablename__ = 'T_log_withdraw_anchor'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    money = Column(Numeric)
    sevice_money = Column(Numeric)
    money_balance = Column(Numeric)
    sevice_money_balance = Column(Numeric)
    money_rp = Column(Numeric)
    sevice_money_rp = Column(Numeric)
    apply_state = Column(Integer)
    create_time = Column(DateTime)
    remark = Column(VARCHAR(512))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    finish_time = Column(DateTime())


class TUserAccountIdentity(Base):
    __tablename__ = 'T_user_account_identity'
    identity_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    verify_status = Column(Integer)
    status = Column(Integer)
    id_user_name = Column(VARCHAR(128))
    id_number = Column(VARCHAR(128))
    bank_name = Column(VARCHAR(128))
    bank_card_number = Column(VARCHAR(128))
    hold_user_name = Column(VARCHAR(128))
    bank_sub_name = Column(VARCHAR(128))
    id_img_front = Column(VARCHAR(256))
    qq_number = Column(VARCHAR(255))
    id_img_back = Column(VARCHAR(256))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class TIdentityPersonal(Base):
    __tablename__ = 'T_identity_personal'
    identity_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    verify_status = Column(Integer)
    status = Column(Integer)
    id_user_name = Column(VARCHAR(128))
    id_number = Column(VARCHAR(128))
    bank_name = Column(VARCHAR(128))
    bank_card_number = Column(VARCHAR(128))
    hold_user_name = Column(VARCHAR(128))
    bank_sub_name = Column(VARCHAR(128))
    id_img_front = Column(VARCHAR(256))
    qq_number = Column(VARCHAR(255))
    id_img_back = Column(VARCHAR(256))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class NeedSchedule(Base):
    __tablename__ = 'ads_need_schedule'
    schedule_id = Column(Integer, primary_key=True)
    schedule_create_time = Column(DateTime())
    schedule_destroy_time = Column(DateTime())
    start_alloc_time = Column(DateTime())
    end_alloc_time = Column(DateTime())
    start_play_time = Column(DateTime())
    end_play_time = Column(DateTime())
    count = Column(Integer)
    assign_flag = Column(Integer)
    flag = Column(Integer)
    enable = Column(Integer)
    schedule_enable = Column(Integer)
    schedule_state = Column(Integer)
    description = Column(VARCHAR(255))
    anchor_if_exp = Column(VARCHAR(255))
    lv_priority = Column(Integer)
    schedule_name = Column(VARCHAR(256))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    group_id = Column(Integer)


class GroupNeedMap(Base):
    __tablename__ = 'ads_group_need_map'
    id = Column(Integer, primary_key=True)
    ads_group_id = Column(Integer)
    ads_need_id = Column(Integer)
    description = Column(VARCHAR(255))
    create_time = Column(DateTime())
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class BaseUser(Base):
    __tablename__ = 'base_user'
    user_id = Column(Integer, primary_key=True)
    u_passport_id = Column(String(32), nullable=False, unique=True)
    anchorid_type = Column(
        Enum(
            '1',
            '2'),
        nullable=False,
        server_default=text("'2'"))
    is_signed = Column(Integer, server_default=text("'0'"))
    user_type = Column(
        Enum(
            '0',
            '4',
            '3',
            '2',
            '1'),
        server_default=text("'0'"))
    user_state = Column(Enum('1', '0'), server_default=text("'1'"))
    u_nickname = Column(String(128), index=True)
    u_mobile_number = Column(String(11))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    email = Column(String(64))
    avatar_img = Column(String(32), nullable=False, server_default=text("''"))


class BaseRoom(Base):
    __tablename__ = 'base_room'
    id = Column(Integer, primary_key=True)
    room_id = Column(String(40), nullable=False, unique=True)
    name = Column(String(60), nullable=False, unique=True)
    room_url = Column(String(128), nullable=False, unique=True)
    platform_id_roomid = Column(String(32), nullable=False, unique=True)
    room_nickname = Column(String(128))
    user_id = Column(Integer, server_default=text("'0'"))
    is_hanged = Column(Integer)
    platform_id = Column(Integer, server_default=text("'0'"))
    auth_state = Column(Enum('1', '2', '3'), server_default=text("'0'"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    attach = Column(String(20))


class BaseUnion(Base):
    __tablename__ = 'base_union'
    union_id = Column(Integer, primary_key=True, autoincrement=True)
    union_name = Column(String(60), nullable=False)
    create_user_id = Column(Integer)
    sign_anchor_num = Column(Integer)
    union_state = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    main_category = Column(String(50))
    describe = Column(String(200))
    contact_information = Column(String(50))
    recruitment_information = Column(String(4000))
    plat_ids = Column(String(128))
    logo = Column(String(256))
    is_auth = Column(Integer)
    upload_max_count = Column(Integer, default=500)

#
# class Paltform(Base):
#     __tablename__ = 'T_guild_platform'
#     plat_id = Column(Integer, primary_key=True)
#     plat_name = Column(VARCHAR(255))
#     description = Column(VARCHAR(255))
#     logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class RoomInfo(Base):
    __tablename__ = 'ads_room_info'
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer)
    room_id = Column(VARCHAR(255))
    year = Column(VARCHAR(255))
    week = Column(VARCHAR(255))
    source_link = Column(VARCHAR(255))
    emcee = Column(VARCHAR(255))
    sourcegname = Column(VARCHAR(255))
    x_rate = Column(Float)
    max_user_pre_count = Column(Float)
    ad_value = Column(Float)
    new_level = Column(VARCHAR(11))
    ad_level = Column(VARCHAR(11))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsNeedPlanInfo(Base):
    __tablename__ = 'ads_need_plan_info'
    need_plan_id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    plan_status = Column(Integer)
    schedule_id = Column(Integer)
    group_id = Column(Integer)
    flag = Column(VARCHAR(11))
    anchor_level = Column(VARCHAR(11))
    create_time = Column(DateTime)
    play_time = Column(DateTime)
    # schedule_id = Column(Integer)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsOpLog(Base):
    __tablename__ = 'ads_op_log'
    op_id = Column(Integer, primary_key=True)
    op_type = Column(Integer)
    op_user_id = Column(Integer)
    op_user_name = Column(VARCHAR(256))
    op_desc = Column(Text)
    op_content = Column(Text)
    createtime = Column(DateTime)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class TaskPlayLog(Base):
    __tablename__ = 'ads_task_play_log'
    play_id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    need_plan_id = Column(Integer)
    need_id = Column(Integer)
    postion_id = Column(VARCHAR(11))
    ads_id = Column(Integer)
    user_id = Column(Integer)
    status = Column(Integer)
    popularity_from = Column(Integer)
    popularity = Column(Integer)
    income = Column(Numeric)
    record_path = Column(VARCHAR(255))
    record_path_old = Column(VARCHAR(255))
    screen_shot_path = Column(Text)
    screen_shot_path_old = Column(Text)
    record_code = Column(Integer)
    verify_status = Column(Integer)
    verify_result = Column(Integer)
    verify_user = Column(Integer)
    begin_time = Column(DateTime())
    end_time = Column(DateTime())
    close_account = Column(Integer)
    is_count_money = Column(Integer)
    create_time = Column(Date)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    log_create_time = Column(DateTime())
    coin_count= Column(Numeric)
    coin_exchange_rate= Column(Numeric)
    coin_id= Column(Numeric)


class AdsTask(Base):
    __tablename__ = 'ads_task'
    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ads_union_group_id = Column(Integer)
    need_plan_id = Column(Integer)
    plat_id = Column(Integer)
    room_id = Column(VARCHAR(255))
    task_result = Column(Integer)
    task_status = Column(Integer)
    create_time = Column(Date)
    logtime = Column(DateTime())
    stream_start_time = Column(DateTime())
    task_create_time = Column(DateTime())
    is_audit = Column(Integer)
    close_account = Column(Integer)
    schedule_id = Column(Integer)
    group_id = Column(Integer)
    estmate_income = Column(Float)


class BasePlatformsGuild(Base):
    __tablename__ = 'base_platforms_guild'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(40))
    website = Column(VARCHAR(128))
    live_data = Column(Integer)
    created_at = Column(DateTime())
    updated_at = Column(DateTime())


# class OpLog(Base):
#     __tablename__ = 'ads_op_log'
#     op_id = Column(Integer, primary_key=True)
#     op_type = Column(Integer)
#     op_user_id = Column(Integer)
#     op_user_name = Column(VARCHAR(255))
#     op_desc = Column(VARCHAR(255))
#     op_content = Column(VARCHAR(255))
#     createtime=Column(DateTime())
#     logtime=Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# class NeedPlanInfo(Base):
#     __tablename__ = 'ads_need_plan_info'
#     need_plan_id= Column(Integer, primary_key=True)
#     task_id = Column(Integer)
#     plan_status = Column(Integer)
#     group_id = Column(Integer)
#     anchor_level = Column(VARCHAR(11))
#     play_time=Column(Date())
#     create_time=Column(DateTime())
#     logtime=Column(DateTime())
#     schedule_id=Column(Integer)
#     flag=Column(VARCHAR(11))
#     need_id_list=Column(VARCHAR(255))

class PlayLogAuto(Base):
    __tablename__ = 'ads_task_play_log_auto'
    auto_id = Column(Integer, primary_key=True)
    auto_max = Column(Integer)
    auto_now = Column(Integer)
    auto_date = Column(Date())
    auto_status = Column(Integer)
    auto_user = Column(VARCHAR(255))
    verify_num = Column(Integer)
    account_num = Column(Integer)
    count_money_num = Column(Integer)
    update_time = Column(DateTime())
    syn_datetime = Column(DateTime())
    syn_user = Column(VARCHAR(255))
    score_status = Column(Integer)
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Adresult(Base):
    __tablename__ = 'ad_result'
    id = Column(Integer, primary_key=True)
    ad_key = Column(VARCHAR(30))
    image_url = Column(VARCHAR(500))
    is_ad = Column(Integer)
    updateTime = Column(DateTime)


class AdsUnionGroup(Base):
    __tablename__ = 'ads_union_group'
    ads_union_group_id = Column(Integer, primary_key=True)
    union_id = Column(Integer)
    platform_id = Column(Integer)
    room_id = Column(String(36))
    user_id = Column(Integer)
    rate = Column(Integer, default=100)
    source_link = Column(String(255))
    apply_status = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)


class PackageInfo(Base):
    __tablename__ = 'ads_package_info'
    ads_package_id = Column(Integer, primary_key=True)
    package_name = Column(VARCHAR(255))
    anchor_alloc_type = Column(Integer)
    comment = Column(VARCHAR(255))
    create_time = Column(DateTime())
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class PackageNeedMap(Base):
    __tablename__ = 'ads_package_need_map'
    ads_package_id = Column(Integer, primary_key=True)
    ads_need_id = Column(Integer)
    description = Column(VARCHAR(255))
    create_time = Column(DateTime())
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class DashboardTask(Base):
    __tablename__ = 'adm_dashboard_task'
    dashboard_id = Column(Integer, primary_key=True)
    package_id = Column(Integer)
    level = Column(VARCHAR(255))
    # type=Column(VARCHAR(255))
    task_total = Column(Integer)
    task_accept = Column(Integer)
    task_finish = Column(Integer)
    task_forgo = Column(Integer)
    task_onway = Column(Integer)
    task_wait = Column(Integer)
    dashboard_status = Column(Integer)
    task_time = Column(Date)
    create_time = Column(DateTime())
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class TAccountAnchor(Base):
    __tablename__ = 'T_account_anchor'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'union_id', 'user_type', 'agent_id'),
    )
    user_id = Column(Integer)
    user_type = Column(Integer)
    agent_id = Column(Integer)
    union_id = Column(Integer)
    balance = Column(Numeric)
    lock_balance = Column(Numeric)
    last_stat_date = Column(Date)
    create_time = Column(DateTime())
    logtime = Column(DateTime())


class TLogIncomeAnchor(Base):
    __tablename__ = 'T_log_income_anchor'
    income_log_id = Column(Integer, primary_key=True)
    income_type = Column(Integer)
    ads_union_group_id = Column(Integer)
    union_id = Column(Integer)
    agent_id = Column(Integer)
    user_id = Column(Integer)
    task_id = Column(Integer)
    play_id = Column(Integer)
    income_from = Column(Integer)
    need_id = Column(Integer)
    room_id = Column(VARCHAR(32))
    comment = Column(VARCHAR(256))
    plat_id = Column(Integer)
    income = Column(Numeric)
    task_create_time = Column(DateTime())
    logtime = Column(DateTime())
    create_time = Column(DateTime())


# 对账记录表
class AdmIncomeCheck(Base):
    __tablename__ = 'adm_income_check'
    check_id = Column(Integer, primary_key=True)
    check_date = Column(Date)
    account_num = Column(Integer)
    withdraw_num = Column(Integer)
    income_log_num = Column(Integer)
    backup_file = Column(VARCHAR(255))
    # backup_file_sec = Column(VARCHAR(255))
    check_user = Column(VARCHAR(255))
    incre_check_result = Column(Integer)
    incre_check_time = Column(DateTime())
    global_check_result = Column(Integer)
    global_check_time = Column(DateTime())
    create_time = Column(DateTime())
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# 对账记录详情表
class AdmIncomeCheckDetail(Base):
    __tablename__ = 'adm_income_check_detail'
    detail_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    check_id = Column(Integer)
    user_type = Column(Integer)
    check_type = Column(Integer)
    agent_id = Column(Integer)
    union_id = Column(Integer)
    balance = Column(Numeric(11, 2), nullable=False)
    income = Column(Numeric(11, 2), nullable=False)
    withdraw = Column(Numeric(11, 2), nullable=False)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# 角色表
class AdmRole(Base):
    __tablename__ = 'adm_role'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(Integer)
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# 角色表
class AdmMenu(Base):
    __tablename__ = 'adm_menu'
    menu_id = Column(Integer, primary_key=True)
    meun_name = Column(VARCHAR(255))
    source_id = Column(Integer)
    parent_id = Column(Integer)
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# 角色-->菜单 表
class AdmRoleMenu(Base):
    __tablename__ = 'adm_role_menu'
    role_menu_id = Column(Integer, primary_key=True)
    role_id = Column(Integer)
    menu_id = Column(Integer)
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsPackageInfoSchedule(Base):
    __tablename__ = 'ads_package_info_schedule'
    order_id = Column(Integer, primary_key=True)
    order_sche_name = Column(VARCHAR(255))
    order_date = Column(DateTime())
    package_id = Column(Integer)
    need_play_num = Column(Integer)
    order_status = Column(Integer)
    order_s = Column(Integer)
    order_a = Column(Integer)
    order_b = Column(Integer)
    order_c = Column(Integer)
    order_d = Column(Integer)
    adsinfo_id = Column(Integer)
    create_people = Column(VARCHAR(255))
    create_time = Column(
        DateTime(),
        default=datetime.now,
        onupdate=datetime.now)
    log_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class AdsAgentUserMap(Base):
    __tablename__ = 'ads_agent_user_map'
    agent_user_map_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer)
    user_id = Column(Integer)
    plat_id = Column(Integer)
    room_id = Column(Integer)
    rate = Column(Integer)
    price = Column(Numeric)
    comment = Column(VARCHAR(255))
    createtime = Column(DateTime())
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Tlogwithdrawanchoridentityinfo(Base):
    __tablename__ = 'T_log_withdraw_anchor_identityinfo'
    id = Column(Integer, primary_key=True)
    u_mobile_number = Column(String(11))
    withdraw_cash_id = Column(Integer)
    identity_id = Column(Integer)
    balance = Column(Numeric)
    user_id = Column(Integer)
    id_user_name = Column(VARCHAR(128))
    id_number = Column(VARCHAR(128))
    id_img_front = Column(VARCHAR(256))
    id_img_back = Column(VARCHAR(256))
    bank_name = Column(VARCHAR(128))
    bank_card_number = Column(VARCHAR(128))
    hold_user_name = Column(VARCHAR(128))
    bank_sub_name = Column(VARCHAR(128))
    qq_number = Column(VARCHAR(255))
    logtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
