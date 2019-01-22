var u_dlg = null;
var host_table

function enable_user(user_id) {
    var _fn_sure = function (cb_stack, cb_args) {
        ywl.ajax_post_json_time_out('/user/delete', {user_id: user_id}, 1000 * 30,
            function (ret) {
                if (ret.code === TPE_OK) {
                    host_table.reload();
                    ywl.notify_success('禁用成功！');
                } else {
                    ywl.notify_error('禁用失败！' + ret.message);
                }
            },
            function () {
                ywl.notify_error('网络故障，禁用失败！');
            }
        );
    };
    var cb_stack = CALLBACK_STACK.create();

    ywl.dlg_confirm(cb_stack, {
        msg: '<p>您确定禁用当前用户吗？此操作不可恢复！！</p>',
        fn_yes: _fn_sure
    });
}

ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#user-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='user-list']",
        data_source: {
            type: 'ajax-post',
            url: '/user/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: '<input type="checkbox" id="host-select-all" value="">',
                key: 'select_all',
                sort: false,
                width: 20,
                render: 'make_check_box',
                fields: {id: 'user_id'}
            },
            {title: "ID", key: "user_id",width: 30},
            {title: "用户名", key: "user_name",width: 50},
            {title: "角色名", key: "role_name",width: 10},
            {title: "状态", key: "enable",width: 10,render: 'format_enable',
                fields: {enable: 'enable'}},
            {title: "时间", key: "logtime",width: 180,render: 'format_time',
                fields: {logtime: 'logtime'}},
            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {role_id: 'role_id'}
            }

        ],
        paging: {selector: dom_id, per_page: paging_normal},

        // 可用的属性设置
        have_header: true,

        // 可用的回调函数
        on_created: ywl.on_host_table_created,
        on_header_created: ywl.on_host_table_header_created
    };

    host_table = ywl.create_table(host_table_options);
    $(dom_id + " [ywl-filter='reload']").click(host_table.reload);

    ywl.create_table_filter_user_list(host_table, dom_id + "_filter_name");

    ywl.create_table_filter_search_box(host_table, dom_id + "_filter_search");
    $("#btn-add-host").click(function () {
        u_dlg.create_show();
    });
    u_dlg = ywl.create_user_info_dlg(host_table);

    // 初始化角色下拉框
    $.get("/role/select4all", {}, function (ret) {
        var auxArr = [];
        $.each(ret, function (k, v) {
            auxArr.push("<option value='" + v["role_id"] + "'>" + v["role_name"] + "</option>");
        });
        $('#role_id').append(auxArr.join(''));
    });



    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};

ywl.create_user_info_dlg = function (tbl) {
    var user_info_dlg = {};
    user_info_dlg.dom_id = "#dialog-user-info";
    user_info_dlg.update = 1;
    user_info_dlg.tbl = tbl;
    user_info_dlg.user_name = '';
    user_info_dlg.user_id = 0;
    user_info_dlg.row_id = 0;
    user_info_dlg.role_id = '';
    user_info_dlg.user_desc = '';

    user_info_dlg.update_show = function (user_id,user_name,role_id) {
        user_info_dlg.update = 1;
        user_info_dlg.init(user_id,user_name,role_id);
        $('#dlg-notice').hide();
        $(user_info_dlg.dom_id).modal();
    };

    user_info_dlg.create_show = function () {
        user_info_dlg.update = 0;
        user_info_dlg.init('', '', 0, 0);
        $('#dlg-notice').show();
        $(user_info_dlg.dom_id).modal();
    };

    user_info_dlg.hide = function () {
        $(user_info_dlg.dom_id).modal('hide');
    };

    user_info_dlg.init = function (user_id,user_name,role_id) {
        user_info_dlg.user_name = user_name;
        user_info_dlg.user_id = user_id;
        user_info_dlg.role_id = role_id;
        user_info_dlg.init_dlg();
    };
    user_info_dlg.init_dlg = function () {
        $(user_info_dlg.dom_id + ' #user_name').val(user_info_dlg.user_name);
        $(user_info_dlg.dom_id + ' #role_id').val(user_info_dlg.role_id);
        if (user_info_dlg.update === 1) {
            $(user_info_dlg.dom_id + ' #user_name').attr("disabled", "true");
            $(user_info_dlg.dom_id + ' #user-pwd-div').hide();
        } else {
            $(user_info_dlg.dom_id + ' #user_name').removeAttr("disabled");
            $(user_info_dlg.dom_id + ' #user-pwd-div').show();

        }

    };

    user_info_dlg.check_args = function () {
        // user_info_dlg.user_name = $(user_info_dlg.dom_id + ' #user_name').val();
         if(user_info_dlg.update==0){
            var user_name=$(user_info_dlg.dom_id + ' #user_name').val();
            if(!user_name){
                alert('请设置用户名称');
                return;
            }
            user_info_dlg.user_name=user_name;
            var pwd=$(user_info_dlg.dom_id + ' #user_pwd').val();
            if(!pwd){
                alert('请设置用户密码');
                return;
            }
            user_info_dlg.pwd=pwd
        }
        var role_id=$(user_info_dlg.dom_id + ' #role_id').val();
        if(!role_id){
            alert('请选择用户角色');
            return;
        }

        user_info_dlg.role_id = role_id
        return true;
    };
    user_info_dlg.post = function () {
        if (user_info_dlg.update === 1) {
            ywl.ajax_post_json('/user/edit', {
                    user_id: user_info_dlg.user_id,
                    role_id: user_info_dlg.role_id
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        user_info_dlg.tbl.reload();
                        ywl.notify_success('用户修改成功！');
                        user_info_dlg.hide();
                    } else {
                        ywl.notify_error('用户修改失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，用户修改失败！');
                }
            );
        }
        else if (user_info_dlg.update === 0) {
            ywl.ajax_post_json('/user/add', {
                    user_name: user_info_dlg.user_name,
                    user_pwd: user_info_dlg.pwd,
                    role_id: user_info_dlg.role_id
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        user_info_dlg.tbl.reload();
                        ywl.notify_success('用户添加成功！');
                        user_info_dlg.hide();
                    } else {
                        ywl.notify_error('用户添加失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，用户添加失败！');
                }
            );
        }
    };
    $(user_info_dlg.dom_id + " #btn-save").click(function () {
        if (!user_info_dlg.check_args()) {
            return;
        }
        user_info_dlg.post();
    });
    return user_info_dlg
};

ywl.on_host_table_header_created = function (tbl) {
    $('#host-select-all').click(function () {
        var _is_selected = $(this).is(':checked');
        $(tbl.selector + ' tbody').find('[data-check-box]').prop('checked', _is_selected);
    });
};
// 扩展/重载表格的功能
ywl.on_host_table_created = function (tbl) {

    tbl.on_cell_created = function (row_id, col_key, cell_obj) {
        if (col_key === 'select_all') {
            // 选择
            $('#host-select-' + row_id).click(function () {
                var _all_checked = true;
                var _objs = $(tbl.selector + ' tbody').find('[data-check-box]');
                $.each(_objs, function (i, _obj) {
                    if (!$(_obj).is(':checked')) {
                        _all_checked = false;
                        return false;
                    }
                });

                var select_all_dom = $('#host-select-all');
                if (_all_checked) {
                    select_all_dom.prop('checked', true);
                } else {
                    select_all_dom.prop('checked', false);
                }
            });

        }
        else if (col_key === "action") {
            var row_data = tbl.get_row(row_id);
            $(cell_obj).find('[ywl-btn-edit]').click(function () {
                var role_id=$(this).attr('role_id')
                u_dlg.update_show(row_data.user_id, row_data.user_name,role_id)
            });
            $(cell_obj).find('[ywl-btn-enable]').click(function () {
               enable_user(row_data.user_id)
            });
        }
    };

    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

         render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };

        render.begin_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + format_datetime(utc_to_local(fields.begin_time)) + ' </span>';
        };

        render.make_action_btn = function (row_id, fields) {
            var ret = [];
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" role_id=' + fields.role_id + ' ywl-btn-edit="' + fields.ID + '">修改</a>&nbsp');
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" role_id=' + fields.role_id + ' ywl-btn-enable="' + fields.ID + '">禁用</a>&nbsp');
            return ret.join('');
        }
        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };

         render.format_enable = function (row_id, fields) {
             var temp='未知'
            if(fields.enable==0){
                temp='<span class="badge badge-inverse mono">禁用</span>'
            }else if(fields.enable==1){
                temp='<span class="badge badge-info mono">启用</span>'
            }
            return '<label style="color: red">'+temp+'</label>'
         };
    };
};

ywl.create_table_filter_user_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'user_name';
    _tblf_st.filter_default = '全部';
    _tblf_st.filter_value = '';

    _tblf_st.get_filter = function () {
        var _ret = {};
        _ret[_tblf_st.filter_name] = _tblf_st.filter_value;
        return _ret;
    };

    _tblf_st.reset = function (cb_stack, cb_args) {
        if (_tblf_st.filter_value === _tblf_st.filter_default) {
            cb_stack.exec();
            return;
        }

        cb_stack
            .add(function (cb_stack) {
                _tblf_st.filter_value = _tblf_st.filter_default;
                $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
                cb_stack.exec();
            });
    };

    _tblf_st.init = function (cb_stack) {
        var node = '';
        var user_list = ywl.page_options.user_list;
        node += '<li><a href="javascript:;" ywl-user-id="0">全部</a></li>';
        node += '<li role="separator" class="divider"></li>';
        $.each(user_list, function (i, g) {
            node += '<li><a href="javascript:;" ywl-user-id="' + g.user_id + '">' + g.user_name + '</a></li>';
        });

        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-user-id]').click(_tblf_st._on_select);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var user_name = $(this).html();

        var cb_stack = CALLBACK_STACK.create();
        cb_stack
            .add(_tblf_st._table_ctrl.load_data)
            .add(function (cb_stack) {
                _tblf_st.filter_value = user_name;
                $(_tblf_st.selector + ' button span:first').html(user_name);
                cb_stack.exec();
            });
        cb_stack.exec();
    };

    return _tblf_st;
};

