var v_dlg = null
var treeObj=null

ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#role-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='role-list']",
        data_source: {
            type: 'ajax-post',
            url: '/role/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: '<input type="checkbox" id="host-select-all" value="">',
                key: 'select_all',
                sort: false,
                width: 20,
                render: 'make_check_box',
                fields: {id: 'role_id'}
            },
            {
                title: "role_id", key: "role_id", width: 30
            },
            {title: "角色名称", key: "role_name", width: 50},
            {
                title: "创建时间", key: "create_time", width: 180, render: 'format_time',
                fields: {logtime: 'create_time'}
            },
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

    var host_table = ywl.create_table(host_table_options);

    $(dom_id + " [ywl-filter='reload']").click(host_table.reload);

    v_dlg = ywl.create_role_info_dlg(host_table);

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    });

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");

    role_tree.init() //初始化菜单数

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_role_info_dlg = function (tbl) {
    var role_info_dlg = {};
    role_info_dlg.dom_id = "#dialog-role-info";
    role_info_dlg.update = 1;
    role_info_dlg.tbl = tbl;

    role_info_dlg.role_name = '';
    role_info_dlg.role_id = '';
    role_info_dlg.menu = '';
    role_info_dlg.update_show = function (role_name,role_id) {
        role_info_dlg.update = 1;
        role_info_dlg.init(role_name,role_id);
        $('#dlg-notice').hide();
        $(role_info_dlg.dom_id).modal();
    };

    role_info_dlg.create_show = function () {
        role_info_dlg.update = 0;
        role_info_dlg.init('', '');
        $('#dlg-notice').show();
        $(role_info_dlg.dom_id).modal();
    };

    role_info_dlg.hide = function () {
        $(role_info_dlg.dom_id).modal('hide');
    };

    role_info_dlg.init = function (role_name,role_id) {
        role_info_dlg.role_name = role_name;
        role_info_dlg.role_id = role_id;
        role_info_dlg.init_dlg();
    };
    role_info_dlg.init_dlg = function () {
        $(role_info_dlg.dom_id + ' #role_name').val(role_info_dlg.role_name);
        if (role_info_dlg.update == 1) {
            $(role_info_dlg.dom_id + ' #role_name').attr('disabled','disabled')
            $(role_info_dlg.dom_id +" #role-div").show()

        } else {
            $(role_info_dlg.dom_id + ' #role_name').removeAttr('disabled')
            $(role_info_dlg.dom_id +" #role-div").hide()
        }

        // 角色对应的权限赋值
        $.get('/role/getById?role_id='+role_info_dlg.role_id,function (ret) {
            treeObj.checkAllNodes(false);
            for(var i=0 in ret){
                var temp_id=ret[i]['menu_id'];
                var node = treeObj.getNodeByParam("id", temp_id, null);
                node.checked = true;
                treeObj.updateNode(node);
            }
        })


    };

    role_info_dlg.check_args = function () {
        var role_name = $(role_info_dlg.dom_id + ' #role_name').val();
        if (!role_name || role_name == "") {
            alert("角色名称不能为空")
            return
        }
        var nodes = treeObj.getCheckedNodes(true);
        var nodeArr=[]
        for (var i=0 in nodes){
            nodeArr.push(nodes[i].id)
        }
        role_info_dlg.role_name = role_name
        role_info_dlg.menus = nodeArr

        return true;
    };
    role_info_dlg.post = function () {
        if (role_info_dlg.update === 1) {

            $.ajax({
                type: "post",
                url: "/role/edit",
                data: {role_id:role_info_dlg.role_id,menus:role_info_dlg.menus},
                dataType: "json",
                traditional: true,
                success: function (ret) {
                    if (ret.code === TPE_OK) {
                        role_info_dlg.tbl.reload();
                        ywl.notify_success('角色菜单修改成功！');
                        role_info_dlg.hide();
                    } else {
                        ywl.notify_error('角色菜单修改失败：' + ret.message);
                    }
                }
            });

        } else {
            ywl.ajax_post_json('/role/add', {
                    // create_time: myDate.toLocaleTimeString(),
                    role_name: role_info_dlg.role_name
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        role_info_dlg.tbl.reload();
                        ywl.notify_success('添加类型成功！');
                        role_info_dlg.hide();
                    } else {
                        ywl.notify_error('添加类型失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，添加类型失败！');
                }
            );

        }
        return true;
    };
    $(role_info_dlg.dom_id + " #btn-save").click(function () {
        if (!role_info_dlg.check_args()) {
            return;
        }
        role_info_dlg.post();
    });
    return role_info_dlg
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

        } else if (col_key === "action") {
            var row_data = tbl.get_row(row_id);
                $(cell_obj).find('[ywl-btn-edit]').click(function () {
                    v_dlg.update_show(row_data.role_name,row_data.role_id);
            });
        }
    };

    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

        render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };
         render.make_action_btn = function (row_id, fields) {
            var ret = [];
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" role_id=' + fields.role_id + ' ywl-btn-edit="' + fields.ID + '">修改</a>&nbsp');
            return ret.join('');
        }

        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };


    };
};


var role_tree = (function () {
    var obj = {}
    obj.setting = {
        check: {
            enable: true
        },
        data: {
            simpleData: {
                enable: true
            }
        }
    };

    obj.setCheck = function () {
        var zTree = $.fn.zTree.getZTreeObj("treeDemo"),
            type = {"Y": "ps", "N": "s"};
        zTree.setting.check.chkboxType = type;
    }



    obj.init = function () {
        $.get('/menu/tree/select', function (ret) {
            $.fn.zTree.destroy("treeDemo");
            treeObj = $.fn.zTree.init($("#treeDemo"), role_tree.setting, ret);
            role_tree.setCheck();
            treeObj.expandAll(true);
        })
    }

    return obj
})()

