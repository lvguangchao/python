<%
    _sidebar = [

	{
		'require_type': 100,
		'id': 'ads',
		'link': '/ads',
		'name': '基础信息',
		'icon': 'fa-cog',
		'sub':[
             {
            'require_type': 100,
            'id': 'adsinfo',
            'link': '/adsinfo/list',
            'name': '素材管理',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'contractinfo',
            'link': '/contractinfo/list',
            'name': '合同管理',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'contractpackageinfo',
            'link': '/contract_package_info_all/list',
            'name': '套餐管理',
            'icon': 'fa-database'
            }
        ]
	},{
		'require_type': 100,
		'id': 'market',
		'link': '/market',
		'name': '广告投放',
		'icon': 'fa-video-camera',
		'sub':[
            {
            'require_type': 100,
            'id': 'needinfo',
            'link': '/needinfo/list',
            'name': 'need 管理',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'needgroupinfo',
            'link': '/needgroupinfo/list',
            'name': 'group管理',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'needschedule',
            'link': '/needschedule/list',
            'name': 'schedule管理',
            'icon': 'fa-database'

            },
            {
            'require_type': 100,
            'id': 'whitelistinfo',
            'link': '/whitelist/list',
            'name': '白名单',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'blacklistinfo',
            'link': '/blacklist/list',
            'name': '黑名单',
            'icon': 'fa-database'
            }
        ]
	},{
		'require_type': 100,
		'id': 'financial',
		'link': '/financial',
		'name': '财务',
		'icon': 'fa-credit-card',
		'sub':[
            {
            'require_type': 100,
            'id': 'withdrawanchorlistinfo',
            'link': '/withdrawanchorlist/list',
            'name': '提现',
            'icon': 'fa-database'
            },{
            'require_type': 100,
            'id': 'income',
            'link': '/income/list',
            'name': '结算(总)',
            'icon': 'fa-database'
            },
             {
            'require_type': 100,
            'id': 'incomeclose',
            'link': '/income/close/list?account_type=1',
            'name': '结算(关账前)',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'incomeother',
            'link': '/income/close/list?account_type=2',
            'name': '结算(关账后)',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'playrecord4income',
            'link': '/playrecord/income/list',
            'name': '播放记录结算',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'identitypersonal',
            'link': '/identitypersonal/list',
            'name': '实名认证用户',
            'icon': 'fa-database'
            },
            {
            'require_type': 100,
            'id': 'useraccountbalance',
            'link': '/accountbalance/list',
            'name': '用户账户余额',
            'icon': 'fa-database'
            },{
            'require_type': 100,
            'id': 'check',
            'link': '/income/check/list',
            'name': '对账查询',
            'icon': 'fa-database'
            }
        ]
	},
	{
		'require_type': 100,
		'id': 'plan',
		'link': '/plan',
		'name': '查询',
		'icon': 'fa-bar-chart-o',
		'sub':[
            {
            'require_type': 100,
            'id': 'advertisingplaninfo',
            'link': '/advertisingplanlist/list',
            'name': '广告计划查询',
            'icon': 'fa-database'
            }, {
            'require_type': 100,
            'id': 'playrecordread',
            'link': '/playrecord/read/list',
            'name': '播放记录查询',
            'icon': 'fa-database'
            }, {
            'require_type': 100,
            'id': 'taskselectlistinfo',
            'link': '/taskselectlist/list',
            'name': '任务查询',
            'icon': 'fa-database'
            }, {
            'require_type': 100,
            'id': 'cloud',
            'link': '/cloud/list',
            'name': '云识别查询',
            'icon': 'fa-database'
            },{
            'require_type': 100,
            'id': 'taskcount',
            'link': '/task/count',
            'name': '任务接受情况统计',
            'icon': 'fa-database'
            }
        ]
	},

	{
		'require_type': 100,
		'id': 'audit',
		'link': '/',
		'name': '审核',
		'icon': 'fa-desktop',
		'sub':[
            {
            'require_type': 100,
            'id': 'playrecord',
            'link': '/playrecord/list',
            'name': '播放记录审核',
            'icon': 'fa-database'
            },
             {
            'require_type': 100,
            'id': 'autoreview',
            'link': '/autoreview/list',
            'name': '自动化审核',
            'icon': 'fa-database'
            },
             {
            'require_type': 100,
            'id': 'source-edit',
            'link': '/playlog/screen/edit',
            'name': '监播素材替换',
            'icon': 'fa-database'
            }
            ,{
            'require_type': 100,
            'id': 'logselectinfo',
            'link': '/logselectinfo/list',
            'name': '日志审计',
            'icon': 'fa-database'
            }
        ]
	},
	{
		'require_type': 100,
		'id': 'ads_plan',
		'link': '/',
		'name': '广告计划',
		'icon': 'fa-calendar-o',
		'sub':[
            {
            'require_type': 100,
            'id': 'ads_cal',
            'link': '/ads/cal/select',
            'name': '广告计划日历',
            'icon': 'fa-database'
            },
             {
            'require_type': 100,
            'id': 'anchor_stock',
            'link': '/anchorstock/list',
            'name': '主播库存',
            'icon': 'fa-database'
            }

        ]
	},{
		'require_type': 100,
		'id': 'anchor',
		'link': '/',
		'name': '主播',
		'icon': 'fa-female',
		'sub':[
            {
            'require_type': 100,
            'id': 'anchor_agent',
            'link': '/anchor/agent/maped',
            'name': '经纪公司主播',
            'icon': 'fa-female'
            },{
            'require_type': 100,
            'id': 'user_credit_score_list',
            'link': '/user/creditscore/list',
            'name': '主播信用分',
            'icon': 'fa-female'
            },{
            'require_type': 100,
            'id': 'user_credit_score_detail',
            'link': '/user/creditscore/detail',
            'name': '信用分变动记录',
            'icon': 'fa-female'
            }
        ]
	},
     {
		'require_type': 100,
		'id': 'system',
		'link': '/',
		'name': '系统',
		'icon': 'fa-wrench',
		'sub':[
            {
            'require_type': 100,
            'id': 'user',
            'link': '/user/list',
            'name': '用户管理',
            'icon': 'fa-database'
            },
             {
            'require_type': 100,
            'id': 'role',
            'link': '/role/list',
            'name': '角色管理',
            'icon': 'fa-database'
            }

        ]
	},

	{
		'require_type': 100,
		'id': 'signout',
		'link': '/signout',
		'name': '退出',
		'icon': 'fa-power-off',
	}
]
%>


<!-- begin sidebar scrollbar -->
<div class="slimScrollDiv">

    <!-- begin sidebar user -->
    <div class="nav">
        <ul class="nav nav-profile">
            <li>
                <div class="image">
                    <img src="/static/img/avatar/001.png" width="36"/>
                    ##                     <i class="fa fa-male"></i>
                                    </div>

                <div class="dropdown">
                    <a class="title" href="#" id="user-profile" data-target="#" data-toggle="dropdown" role="button"
                       aria-haspopup="true" aria-expanded="false">
                        <span class="name" id="login_name"></span>
                        <span class="name">${ current_user["name"] }</span>
                        <span class="role">
    用户
                            <i class="fa fa-caret-right"></i></span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-right">
                        <li><a href="/pwd/update" id="btn-logout">修改密码</a></li>
                        <li><a href="/signout" id="btn-logout">安全退出</a></li>
                    </ul>
                </div>


            </li>
        </ul>
    </div>
    <!-- end sidebar user -->

    <!-- begin sidebar nav -->
    <div class="nav">
        <ul class="nav nav-menu">

            %for menu in _sidebar:

                %if 'separator' in menu:
                    <hr style="border:none;border-bottom:1px solid #636363;margin-bottom:0;margin-top:5px;"/>
                %endif
                <%
                    flag=False
                    if current_user['role_id']==0:
                        flag=True
                    else:
                      for r in current_user['role_menu']:
                         if "'"+menu['id']+"'"=="'"+r+"'":
                            flag=True
                            break
                %>
                %if 'sub' in menu and len(menu['sub']) > 0 and flag:
                    <li id="sidebar_menu_${menu['id']}"><a href="javascript:;"
                                                           onclick="ywl._sidebar_toggle_submenu('${menu['id']}');">
                        <i class="fa ${menu['icon']} fa-fw icon"></i><span>${menu['name']}</span>
                        <i class="menu-caret"></i></a>
                        <ul class="sub-menu" id="sidebar_submenu_${menu['id']}" style="display:none;">
                            %for sub in menu['sub']:
                            <%
                                flag=False
                                if current_user['role_id']==0:
                                    flag=True
                                else:
                                  for r in current_user['role_menu']:
                                    if "'"+sub['id']+"'"=="'"+r+"'":
                                      flag=True
                                      break
                            %>
                                %if flag:
                                <li id="sidebar_menu_${menu['id']}_${sub['id']}">
                                    %if "blank" in sub.keys():
                                        <a href="${sub['link']}" target=_blank><span>${sub['name']}</span></a>
                                    %else:
                                        <a href="${sub['link']}"><span>${sub['name']}</span></a>
                                    %endif
                                </li>
                                %endif
                            %endfor
                        </ul>
                    </li>
                %else:
                <%
                    flag=False
                    if current_user['role_id']==0:
                        flag=True
                    else:
                      flag=False
                      for r in current_user['role_menu']:
                         if "'"+menu['id']+"'"=="'"+r+"'":
                            flag=True
                            break
                %>
                %if flag or 'signout'==menu['id']:
                        <li id="sidebar_menu_${menu['id']}"><a href="${menu['link']}"
                            %if 'target' in menu:
                                                               target="${menu['target']}"
                            %endif
                        ><i class="fa ${menu['icon']} fa-fw icon"></i><span>${menu['name']}</span></a></li>
                        %endif
                %endif
            %endfor
        </ul>
    </div>
    <!-- end sidebar nav -->

</div>
<!-- end sidebar scrollbar -->
