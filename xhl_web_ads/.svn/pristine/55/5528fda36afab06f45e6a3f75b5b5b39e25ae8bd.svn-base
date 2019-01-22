var v_dlg = null


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
                title: "合同ID", key: "role_id", width: 30
            },
            {title: "合同名称", key: "role_name", width: 50},
            {
                title: "创建时间", key: "create_time", width: 180, render: 'format_time', sort: true,
                fields: {logtime: 'create_time'}
            },{
                title: "修改时间", key: "log_time", width: 180, render: 'log_time', sort: true,
                fields: {logtime: 'log_time'}
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

    v_dlg = ywl.create_contractioninfo_infodlg(host_table);

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    });

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_contractioninfo_infodlg = function (tbl) {
    var contractioninfo_infodlg = {};
    contractioninfo_infodlg.dom_id = "#dialog-role-info";
    contractioninfo_infodlg.update = 1;
    contractioninfo_infodlg.tbl = tbl;

    contractioninfo_infodlg.role_name = '';
    contractioninfo_infodlg.update_show = function (role_name) {
        contractioninfo_infodlg.update = 1;
        contractioninfo_infodlg.init(role_name);
        $('#dlg-notice').hide();
        $(contractioninfo_infodlg.dom_id).modal();
    };

    contractioninfo_infodlg.create_show = function () {
        contractioninfo_infodlg.update = 0;
        contractioninfo_infodlg.init('', '', 0, 0);
        $('#dlg-notice').show();
        $(contractioninfo_infodlg.dom_id).modal();
    };

    contractioninfo_infodlg.hide = function () {
        $(contractioninfo_infodlg.dom_id).modal('hide');
    };

    contractioninfo_infodlg.init = function (role_name) {
        contractioninfo_infodlg.role_name = role_name;
        contractioninfo_infodlg.init_dlg();
    };
    contractioninfo_infodlg.init_dlg = function () {
        $(contractioninfo_infodlg.dom_id + ' #role_name').val(contractioninfo_infodlg.role_name);
    };

    contractioninfo_infodlg.check_args = function () {
        var role_name = $(contractioninfo_infodlg.dom_id + ' #role_name').val();
        if (!role_name || role_name == "") {
            alert("角色名称不能为空")
            return
        }

        contractioninfo_infodlg.role_name = role_name

        return true;
    };
    contractioninfo_infodlg.post = function () {
        if (contractioninfo_infodlg.update === 1) {

        } else {
            ywl.ajax_post_json('/role/add', {
                    // create_time: myDate.toLocaleTimeString(),
                    role_name: contractioninfo_infodlg.role_name
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        contractioninfo_infodlg.tbl.reload();
                        ywl.notify_success('添加类型成功！');
                        contractioninfo_infodlg.hide();
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
    $(contractioninfo_infodlg.dom_id + " #btn-save").click(function () {
        if (!contractioninfo_infodlg.check_args()) {
            return;
        }
        contractioninfo_infodlg.post();
    });
    return contractioninfo_infodlg
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
        }
    };

    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

        render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };

        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };


    };
};



