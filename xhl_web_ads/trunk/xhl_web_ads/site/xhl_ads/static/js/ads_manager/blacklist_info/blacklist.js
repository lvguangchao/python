var v_dlg = null

var shchedule_id_new = null
var shchedule_id_old = null

var plat_id_old = null
var room_id_old = null



function excelImportAds() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var b = xhr.responseText;
            var result = JSON.parse(b);
            if (result.code == 1) {
                alert("导入成功！");
            } else {
                alert("导入失败！");
            }
        }
    };
    var files = document.getElementById('files_ads').files;
    if (!files.length) {
        alert('请选择文件!');
        return;
    }
    var form = new FormData();
    var file = files[0];
    // var union_name=$('#hid_union_id').val()

    form.append("infile", file);
    // form.append("union_name",union_name);
    xhr.open("post", "/blacklist/import", false);
    xhr.send(form);

}

function show_adsInfo(id) {
    $.get("/needschedule/list_shchedule?id=" + id, function (ret) {
        if (ret.code === 0) {
            document.getElementById('schedule_id').innerHTML = ret.data.schedule_id;
            document.getElementById('group_name').innerHTML = ret.data.group_name;
            document.getElementById('count').innerHTML = ret.data.count;
            document.getElementById('anchor_if_exp').innerHTML = ret.data.anchor_if_exp;
            document.getElementById('lv_priority').innerHTML = ret.data.lv_priority;
            document.getElementById('logtime').innerHTML = ret.data.logtime;

            $("#dialog-scheduleinfo-info").modal();

        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }

    })
}


ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#blacklist-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='blacklist-list']",
        data_source: {
            type: 'ajax-post',
            url: '/blacklist/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: '<input type="checkbox" id="host-select-all" value="">',
                key: 'select_all',
                sort: false,
                width: 20,
                render: 'make_check_box',
                fields: {id: 'id'}
            },
            {title: "平台ID", key: "plat_id", width: 50},
            {title: "房间号", key: "room_id", width: 10},
            {
                title: "schedule_id", key: "ads_schedule_id", width: 10, render: 'format_ads',
                fields: {ads_schedule_id_list: 'ads_schedule_id'}
            },
            {
                title: "创建时间", key: "create_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'create_time'}
            }, {
                title: "log时间", key: "logtime", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'logtime'}
            },

            {title: "描述", key: "comment", width: 10},
            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'room_id', protocol: 'room_id'}
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
    $(dom_id + " [ywl-filter='update_demo']").click(function () {
        var isFirefox = /firefox/i.test(navigator.userAgent);
        var url = '/static/download/黑名单_套餐名称_主播名称.xls';
        {
            if (!url) return;
            if (isFirefox) {
                location.href = url
            } else {
                a = document.createElement('a')
                a.download = url.replace(/.+\/([^/]+\.\w+)(?:\?.*)?$/, '$1')
                a.href = url
                a.click()
            }
        }

    });

    $("#btn-delete-host").click(function () {
        var ids = [];
        var _objs = $(host_table.selector + " tbody tr td [data-check-box]");
        $.each(_objs, function (i, _obj) {
            if ($(_obj).is(':checked')) {
                var _row_data = host_table.get_row(_obj);
                ids.push(_row_data.id);
                ids.push(_row_data.plat_id);
                ids.push(_row_data.room_id);
                ids.push(_row_data.ads_schedule_id_list);
            }
        });

        if (ids.length === 0) {
            ywl.notify_error('请选择要批量删除的黑名单！');
            return;
        }

        var _fn_sure = function (cb_stack, cb_args) {
            ywl.ajax_post_json_time_out('/blacklist/delete', {ids: ids}, 1000 * 30,
                function (ret) {
                    if (ret.code === TPE_OK) {
                        host_table.reload();
                        ywl.notify_success('删除黑名单成功！');
                    } else {
                        ywl.notify_error('删除黑名单失败！' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，删除黑名单失败！');
                }
            );
        };
        var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>您确定要删除选定的黑名单吗？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
    });

    v_dlg = ywl.create_blacklist_infodlg(host_table);

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    })

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_blacklist_infodlg = function (tbl) {
    var blacklist_infodlg = {};
    blacklist_infodlg.dom_id = "#dialog-blacklist-info";
    blacklist_infodlg.update = 1;
    blacklist_infodlg.tbl = tbl;


    // blacklist_infodlg.id = 0;
    blacklist_infodlg.room_id = '';
    blacklist_infodlg.plat_id = 0;
    blacklist_infodlg.ads_schedule_id = '';
    blacklist_infodlg.comment = '';

    blacklist_infodlg.update_show = function (id, room_id, plat_id, ads_schedule_id, comment) {
        blacklist_infodlg.update = 1;
        blacklist_infodlg.init(id, room_id, plat_id, ads_schedule_id, comment);
        $('#dlg-notice').hide();
        $(blacklist_infodlg.dom_id).modal();
    };

    blacklist_infodlg.create_show = function () {
        blacklist_infodlg.update = 0;
        blacklist_infodlg.init('', '', 0, 0);
        $('#dlg-notice').show();
        $(blacklist_infodlg.dom_id).modal();
    };

    blacklist_infodlg.hide = function () {
        $(blacklist_infodlg.dom_id).modal('hide');
    };

    blacklist_infodlg.init = function (id, room_id, plat_id, ads_schedule_id, comment) {
        blacklist_infodlg.id = id;
        blacklist_infodlg.room_id = room_id;
        blacklist_infodlg.plat_id = plat_id;
        blacklist_infodlg.ads_schedule_id = ads_schedule_id;
        blacklist_infodlg.comment = comment;

        blacklist_infodlg.init_dlg();
    };
    blacklist_infodlg.init_dlg = function () {
        $(blacklist_infodlg.dom_id + ' #room_id').val(blacklist_infodlg.room_id);
        $(blacklist_infodlg.dom_id + ' #plat_id').val(blacklist_infodlg.plat_id);
        $(blacklist_infodlg.dom_id + ' #ads_schedule_id').val(blacklist_infodlg.ads_schedule_id);

        $(blacklist_infodlg.dom_id + ' #comment').val(blacklist_infodlg.comment);
        console.log(blacklist_infodlg.ads_schedule_id);

        $(blacklist_infodlg.dom_id + ' #id').val(blacklist_infodlg.id);

    };

    blacklist_infodlg.check_args = function () {
        var room_id = $(blacklist_infodlg.dom_id + ' #room_id').val();
        var plat_id = $(blacklist_infodlg.dom_id + ' #plat_id').val();
        var ads_schedule_id = $(blacklist_infodlg.dom_id + ' #ads_schedule_id').val();
        var comment = $(blacklist_infodlg.dom_id + ' #comment').val();

        if (!room_id || room_id == "") {
            alert("room_id不能为空")
            return
        }
        if (!plat_id || plat_id == "") {
            alert("plat_id不能为空")
            return
        }

        blacklist_infodlg.room_id = room_id
        blacklist_infodlg.plat_id = plat_id
        blacklist_infodlg.ads_schedule_id = ads_schedule_id
        blacklist_infodlg.comment = comment


        return true;
    };
    blacklist_infodlg.post = function () {
        if (blacklist_infodlg.update === 1) {
            ywl.ajax_post_json('/blacklist/edit', {
                    id: blacklist_infodlg.id,
                    room_id: blacklist_infodlg.room_id,
                    plat_id: blacklist_infodlg.plat_id,
                    ads_schedule_id: blacklist_infodlg.ads_schedule_id,
                    comment: blacklist_infodlg.comment
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        blacklist_infodlg.tbl.reload();
                        ywl.notify_success('更新类型成功！');
                        blacklist_infodlg.hide();
                    } else {
                        ywl.notify_error('更新类型失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，更新类型失败！');
                }
            );
        } else {
            ywl.ajax_post_json('/blacklist/add', {

                    room_id: blacklist_infodlg.room_id,
                    plat_id: blacklist_infodlg.plat_id,
                    ads_schedule_id: blacklist_infodlg.ads_schedule_id,
                    comment: blacklist_infodlg.comment
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        blacklist_infodlg.tbl.reload();
                        ywl.notify_success('添加类型成功！');
                        blacklist_infodlg.hide();
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
    $(blacklist_infodlg.dom_id + " #btn-save").click(function () {
        if (!blacklist_infodlg.check_args()) {
            return;
        }
        blacklist_infodlg.post();
    });
    return blacklist_infodlg
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

                v_dlg.update_show(row_data.id, row_data.room_id, row_data.plat_id, row_data.ads_schedule_id, row_data.comment)
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

            // if (fields.ret_code === 9999 && fields.cost_time > 0) {
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-edit="' + fields.ID + '">修改</a>&nbsp');
            // ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-delete="' + fields.ID + '">删除</a>&nbsp');
            // }

            return ret.join('');
        };


        render.format_ads = function (row_id, fields) {
            var temp = []
            if (fields.ads_schedule_id_list) {
                var arr = fields.ads_schedule_id_list;
                temp.push('<a href="javascript:void(0)" onclick="show_adsInfo(' + arr + ')">【' + arr + '】</a>')

            }
            return temp.join("  ");
        };


        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };


    };
};



