# -*- coding: utf-8 -*-
from . import toc
from . import ads
from . import balance

# from . import error
# from . import support

__all__ = ['controllers']

controllers = [
    (r'/', toc.LoginHandler),
    (r'/signout', toc.SignOutHander),
    (r'/login', toc.LoginHandler),
    (r'/pwd/update', toc.PwdUpdateHander),
    (r'/get/task/gen', toc.getTask4UploadHander),
    (r'/get/task/process', toc.getTaskProcessHander),
    (r'/not_permiss', toc.notPermissHander),

    (r'/get/RandomCode', toc.RandomCode),
    (r'/user/list', toc.UserHander),
    (r'/user/edit', toc.UserEditHander),
    (r'/user/add', toc.UserAddHander),
    (r'/user/delete', toc.UserDeleteHander),

    (r'/role/select4all', toc.AdmRole4AllHander),
    (r'/role/edit', toc.RoleEditHander),
    (r'/role/getById', toc.getRoleMenuByRoleIdHander),
    (r'/menu/tree/select', toc.AdmMenu4TreeHander),
    (r'/index', toc.IndexHandler),

    (r'/adsinfo/list', ads.AdsInfoHander),
    (r'/adsinfo/add', ads.AdsinfoAddHander),
    (r'/adsinfo/add/sale', ads.AdsinfoAdd4SaleHander),
    (r'/adsinfo/edit', ads.AdsinfoEditHander),
    (r'/adsinfo/vadd', ads.AdsInfoVedioAddHander),
    (r'/adsinfo/delete', ads.AdsInfoDeleteHander),
    (r'/adsinfo/select', ads.AdsInfoSelect4AllHander),
    (r'/groupinfo/select', ads.GroupInfoSelect4AllHander),
    (r'/needinfo/getadsinfo(.*)', ads.AdsInfoFindByIdHander),
    (r'/packinfo/select', ads.ContPackInfoSelect4AllHander),

    (r'/role/list', ads.RoleInfoSelectHander),  # 角色管理 list
    (r'/role/add', ads.RoleInfoAddHander),  # 角色管理(add)

    (r'/contractinfo/list', ads.ContractInfoHander),
    (r'/contractinfo/add', ads.ContractAddInfoHander),
    (r'/contractinfo/delete', ads.ContractDelInfoHander),
    (r'/contractinfo/edit', ads.ContractEdInfoHander),

    (r'/needinfo/get(.*)', ads.NeedInfoFindByIdIdHander),
    (r'/needinfo/list', ads.NeedInfoHander),

    (r'/needinfo/add', ads.NeedInfoAddHander),
    (r'/needinfo/edit', ads.NeedInfoEditHander),
    (r'/needinfo/delete', ads.NeedInfoDeleteHander),
    (r'/needinfo/all', ads.NeedInfo4AllHander),
    (r'/needinfo/toadd', ads.NeedinfoBatchAddHander),

    (r'/needgroupinfo/list', ads.NeedGroupInfoHander),
    (r'/needgroupinfo/add', ads.NeedGroupInfoAddHander),
    (r'/needgroupinfo/edit', ads.NeedGroupInfoEditHander),
    (r'/needgroupinfo/delete', ads.NeedGroupInfoDeleteHander),
    (r'/groupneedmap/update', ads.GroupNeedMapUpdateHander),
    (r'/groupneedinfo/all', ads.NeedGroupInfoAllHander),

    (r'/needgroupinfo/list_groupid', ads.NeedScheduleHander_group),  ##(点击获取group_id 详情)

    (r'/needinfo/selectBygruopId(.*)', ads.GroupNeedMapSelectByIdHander),
    (r'/needinfo/selectById(.*)', ads.NeedInfoSelectById),

    (r'/needschedule/list', ads.NeedScheduleHander),
    (r'/needschedule/list_shchedule', ads.NeedScheduleHander_shchedule),  ##(用于白名单页面,点击获取shchedule_id 详情)

    (r'/needschedule/add', ads.NeedScheduleAddHander),
    (r'/needschedule/edit', ads.NeedScheduleUpdateHander),
    (r'/needschedule/delete', ads.NeedScheduleDeleteHander),

    (r'/needschedule/retract', ads.NeedScheduleRetractHander),

    (r'/needschedule/import', ads.NeedScheduleIMInfoHanderAll),  ##(适用于schedule管理页面导入白名单)
    (r'/needschedule/white', ads.NeedScheduleSEWhiteAll),  ##(适用于schedule管理页面查看对应的白名单)


    (r'/contract_package_info/list', ads.ContractPackageInfoHander),  # (用于合同页面查看对应套餐)

    (r'/contract_package_info_all/list', ads.ContractPackageInfoHanderAll),
    (r'/contract_package_info/add', ads.ContractAddPackageInfoHanderAll),
    (r'/contract_package_info/delete', ads.ContractDelPackageInfoHanderAll),
    (r'/contract_package_info/edit', ads.ContractEdPackageInfoHanderAll),
    (r'/contract_package_info/edit_affairs', ads.ContractEdAffairsInfoHanderAll),  # (修改财务编号)

    (r'/whitelist/list', ads.WhitelistInfoHanderAll),  # 白名单
    (r'/whitelist/add', ads.WhitelistAddInfoHanderAll),
    (r'/whitelist/delete', ads.WhitelistDelInfoHanderAll),
    (r'/whitelist/edit', ads.WhitelistEdInfoHanderAll),
    (r'/whitelist/import', ads.WhitelistIMInfoHanderAll),

    (r'/seleteshchedule/select', ads.Seleteshchedule),  ##(获取shchedule,适用于黑白名单:白名单:0,黑名单:1)
    (r'/seleteshchedule/select_group', ads.Seleteshchedulegroup),  ##(获取shchedule所用的group_ID)

    (r'/blacklist/list', ads.BlacklistInfoHanderAll),  # 黑名单
    (r'/blacklist/add', ads.BlacklistAddInfoHanderAll),
    (r'/blacklist/delete', ads.BlacklistDelInfoHanderAll),
    (r'/blacklist/edit', ads.BlicklistEdInfoHanderAll),
    (r'/blacklist/import', ads.BlacklistIMInfoHanderAll),

    (r'/withdrawanchorlist/list', ads.WithdrawanchorInfoHanderAll),  # 用户提现
    (r'/withdrawanchorlist/update', ads.WithdrawanchorUpInfoHanderAll),  # 用户提现
    (r'/withdrawanchorlist/edit', ads.WithdrawanchorEdInfoHanderAll),
    (r'/withdrawanchorlist/edit_commit', ads.WithdrawanchorEdCommitHanderAll),  # 提现修改备注信息
    (r'/withdrawanchorlist/edit_identity', ads.WithdrawanchorEdIdentityHanderAll),  # 提现修改提现用户信息
    (r'/withdrawanchorlist/import', ads.WithdrawanchorIMInfoHanderAll),  # 用户提现导入修改提现状态
    (r'/withdrawanchorlist/remind', ads.WithdrawanchorREInfoHanderAll),  # 用户提现导入修改提现状态(弹框提醒目前的总数以及总价值)

    (r'/income/list', ads.IncomePackListHander),
    (r'/incomeanchor/list', ads.IncomeAnchorListHander),
    (r'/incomeanchor/getroominfo', ads.GetRoomInfoHander),
    (r'/incomeanchor/export', ads.IncomeAnchorExportHander),
    (r'/incomeanchor/settle', ads.IncomeAnchorsettleHander),

    (r'/playrecord/list', ads.PlayRecordHander),
    (r'/playrecord/read/list', ads.PlayRecordReadHander),
    (r'/playrecord/audit', ads.PlayRecordAuditHander),
    (r'/playrecord/edit', ads.PlayRecordEditHander),
    (r'/playrecord/export', ads.PlayRecordExportHander),
    (r'/playrecord/export/select', ads.PlayLogExportSelectHander),
    (r'/playrecord/export/create', ads.PlayLogExportCreateHander),

    (r'/playrecord/import', ads.PlayRecordImportHanderAll),
    (r'/playrecord/import/select', ads.PlayLogImportSelectHander),
    (r'/playrecord/create', ads.PlayLogImportCreateHander),

    (r'/advertisingplanlist/list', ads.AdvertisingPlanListHander),  # 广告计划查询
    (r'/advertisingplanlist/scheduleid', ads.Seleteshcheduleadvertisting),  # 广告计划查询(根据level获取对应的schedule_id)
    (r'/logselectinfo/list', ads.LogSelectInfoListHander),  # log查询
    (r'/logselectinfo/op_content', ads.LogSelectInfoListHander_content),  ##(log对应的content解析json的数据)
    (r'/platform4all/list', ads.Paltform4AllList),  # log查询
    (r'/unionList4all/list', ads.UnionList4AllList),  # log查询
    (r'/schedule/flush', ads.FulshDateHander),

    # 任务查询
    (r'/taskselectlist/list', ads.TaskSelectListHander),  # 任务查询
    (r'/taskselectlist/play_log', ads.SeleteTaskplaylogList),  # 任务查询(task_id对应的play_log) # 任务查询
    (r'/taskselectlist/plat_list', ads.SeleteTaskPlatList),  # 任务查询(task_id对应的platform) # 任务查询
    (r'/taskselectlist/package_list', ads.SeleteTaskPackageList),  # 任务查询(全部的套餐) # 任务查询
    (r'/taskselectlist/update', ads.TaskSelectUpdateHander),  # 任务导出
    # 提现用户详情
    (r'/identitypersonal/list', ads.IdentityPersonalListHander),  # 提现用户详情
    (r'/identitypersonal/edit', ads.IdentityPersonalEditHander),  # 提现用户详情(修改用户信息)
    # (r'/identitypersonal/play_log', ads.SeleteTaskplaylogList),  #任务查询(task_id对应的play_log)

    (r'/autoreview/list', ads.PlayLogAutoListHander),  # 自动审核
    (r'/autoreview/audit', ads.PlayLogAutoAuditHander),  # 自动审核
    (r'/autoreview/flush', ads.PlayLogAutoFlushHander),  # 自动审核 结算比例

    (r'/autoreview/select', ads.PlayLogAutoSelectHander),  # 自动审核
    (r'/autoreview/create', ads.PlayLogAutoCreateHander),  # 自动审核
    # 用户账户余额查询
    (r'/accountbalance/list', ads.AccountBalanceList),
    (r'/accountbalance/income_list', ads.AccountBalanceIncomeList),  # user_id结算信息(跳转)
    (r'/accountbalance/update', ads.AccountBalanceIncomeUpdate),  # user_id结算信息(跳转,导出)
    # (r'/accountbalance/income_list', ads.AccountBalanceIncomeList),  # user_id结算信息
    (r'/accountbalance/income/add', ads.AccountBalanceAddIncome),  # 申诉成功增加结算
    (r'/accountbalance/get_package', ads.AccountBalanceGetPackage),  # 获取套餐list
    (r'/accountbalance/get_need_id', ads.AccountBalanceGetNeedId),  # user_id 所对应的need_id
    (r'/accountbalance/get_play_id', ads.AccountBalanceGetPlayId),  # user_id 所对应的play_id
    (r'/task/count', ads.TaskRecepetCountHander),  #

    (r'/plat/data/synch', balance.PlatBalanceDataSynHander),  # 平台结算数据同步
    (r'/plat/data/select', balance.PlatDataSynSelectHander),  # 平台结算进度信息
    (r'/plat/data/create', balance.PlatDataSynCreateHander),  # 平台结算进度信息创建


    (r'/cloud/list', ads.CloudDiscernListHander),  # 云识别查询

    (r'/income/check/list', balance.CheckAccountListHander),  # 对账
    (r'/income/check/all', balance.CheckAccountHander),# 全局对账
    (r'/income/check/incre', balance.CheckIncreHander),# 增量对账
    (r'/income/check/detail', balance.CheckAccountDetailHander),
    (r'/income/check/select', balance.CheckAccountSelectHander),
    (r'/income/check/create', balance.CheckAccountCreateHander),


    (r'/ads/cal/list', ads.AdsPackageInfoScheduleListHander),  #
    (r'/ads/cal/select', ads.AdsPackageInfoScheduleSelectHander),  #
    (r'/ads/cal/add', ads.AdsCal4PackageAddHander),  #
    (r'/contract/package/getbyId', ads.GetPackageByIdHander),
    (r'/anchor/invetor/getbyId', ads.GetAnchorInvetoy),  # 获取主播当日库存

    (r'/anchorstock/list', ads.AnchorStock),  # 获取主播当月库存


    (r'/income/close/list', ads.IncomePackList4ClosedHander),  # 结账之前的套餐
    (r'/incomeanchor/close/settle', ads.IncomeAnchorsettle4closeHander),  # 结账之前的结算
    (r'/incomeanchor/close/list', ads.IncomeAnchor4closeListHander),  # 结账之前的结算详情
    (r'/incomeanchor/close/export', ads.IncomeAnchorExport4closeHander),
    (r'/playrecord/income/list', ads.PlayRecordIncomeHander),
    (r'/account/income/close/add', ads.AccountAdd4ClosePackage),  # 套餐完成之后,增加结算


    (r'/anchor/agent/maped', ads.AnchorAgentMapHander),  # 主播列表，
    (r'/anchor/agent/maped/export', ads.AnchorAgentMapExportHander),  # 主播导出，
    (r'/anchor/select4all', ads.AgnetMap4AllHander),  # 主播，
    (r'/anchor/agnet/add', ads.AdsAgentUserMapAddHander),
    (r'/anchor/agnet/edit', ads.AdsAgentUserMapEditHander),
    (r'/anchor/agnet/delete', ads.AdsAgentUserMapDeleteHander),
    (r'/anchor/agnet/name/add', ads.AdsAgentUserAddHander),

    (r'/anchor/agent/incomerate/edit', ads.AdsAgentUserIncomeRateEditHander),#修改经纪公司收入比例
    (r'/balance/rollback', balance.AccountRollBackHander),#修改经纪公司收入比例


    (r'/playlog/screen/edit', ads.PlaylogScreenEditHander),#播放记录素材修改
    (r'/playlog/find_by_id', ads.PlaylogFindByIdHander),#播放记录素材修改


    (r'/credit/update', ads.CreditUpdateHandler),#信用分更新


    (r'/user/creditscore/list', ads.CreditScoreListHandler),#信用列表
    (r'/user/creditscore/edit', ads.CreditScoreEditHandler),#信用列表
    (r'/user/creditscore/detail', ads.CreditScoreDetailHandler),#信用列表


]
