var ws = new WebSocket("ws://localhost:8000/chat");
ws.onmessage = function (e) {
    $("#msg_view").append("<br>" + e.data)
}


function sendMsg() {

}



var v_dlg=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#plugin-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='plugin-list']",
        data_source: {
            type: 'ajax-post',
            url: '/plugin/list'
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
            {title: "ID", key: "id",width: 30},
            {title: "update_url", key: "update_url",width: 50},
            {title: "core_url", key: "core_url",width: 10},
            {title: "tools_url", key: "tools_url",width: 10},
            {title: "module_url", key: "module_url",width: 10},
            {title: "update_person", key: "update_person",width: 10},
            {title: "state", key: "state",width: 10},
             {
                title: "日志时间", key: "logtime", width: 180, render: 'format_time',
                fields: {logtime: 'logtime'}
            },

            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'id', update_url: 'update_url',core_url:"core_url",tools_url:"tools_url",module_url:"module_url"}
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

    $("#to_pack").click(function () {
        $("#dialog-plugin-info").modal();
        ywl.ajax_post_json_time_out('/plugin/add', {}, 1000 * 300,
            function (ret) {
                if (ret.code === TPE_OK) {
                    ywl.notify_success('系统准备完毕，开始打包');

                    $("#msg").empty()
                    var msg = ret.data;
                    ws.send(msg);

                } else {
                    ywl.notify_error('系统准备失败！');
                }
            },
            function () {
                ywl.notify_error('网络故障，系统准备失败！');
            }
        );
    })

    ywl.create_vtype_info_dlg = function (tbl) {
        $("#dialog-plugin-info" + " #btn-save").click(function () {
            tbl.reload()
            $("#dialog-plugin-info").modal('hide');
        })
    }



    v_dlg = ywl.create_vtype_info_dlg(host_table);

    $("#btn-add-host").click(function () {
         v_dlg.create_show();
    })

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_vtype_info_dlg = function (tbl) {
    var vtype_info_dlg = {};
    vtype_info_dlg.dom_id = "#dialog-vtype-info";
    vtype_info_dlg.update = 1;
    vtype_info_dlg.tbl = tbl;
    vtype_info_dlg.vtype_name = '';
    vtype_info_dlg.vtype_code = 0;
    vtype_info_dlg.row_id = 0;

    vtype_info_dlg.update_show = function (vtype_code, vtype_name, row_id) {
        vtype_info_dlg.update = 1;
        vtype_info_dlg.init(vtype_code, vtype_name, row_id);
        $('#dlg-notice').hide();
        $(vtype_info_dlg.dom_id).modal();
    };

    vtype_info_dlg.create_show = function () {
        vtype_info_dlg.update = 0;
        vtype_info_dlg.init('', '', 0, 0);
        $('#dlg-notice').show();
        $(vtype_info_dlg.dom_id).modal();
    };

    vtype_info_dlg.hide = function () {
        $(vtype_info_dlg.dom_id).modal('hide');
    };

    vtype_info_dlg.init = function (vtype_code, vtype_name, row_id) {
        vtype_info_dlg.vtype_code = vtype_code;
        vtype_info_dlg.vtype_name = vtype_name;
        vtype_info_dlg.row_id = row_id;
        vtype_info_dlg.init_dlg();
    };
    vtype_info_dlg.init_dlg = function () {
        $(vtype_info_dlg.dom_id + ' #vtype_code').val(vtype_info_dlg.vtype_code);
        $(vtype_info_dlg.dom_id + ' #vtype_name').val(vtype_info_dlg.vtype_name);
        $(vtype_info_dlg.dom_id + ' #vtype_list_id').val(vtype_info_dlg.row_id);
        if (vtype_info_dlg.update === 1) {
             $(vtype_info_dlg.dom_id + ' #vtype_code').attr("disabled", "true");
            $(vtype_info_dlg.dom_id + ' #vtype-div').show();
        } else {
             $(vtype_info_dlg.dom_id + ' #vtype_code').removeAttr("disabled");
        }

    };

    vtype_info_dlg.check_args = function () {
        var vtype_code=$(vtype_info_dlg.dom_id + ' #vtype_code').val()
        var vtype_name=$(vtype_info_dlg.dom_id + ' #vtype_name').val();
        if(!vtype_code||vtype_code==""){
            alert("类型编号不能为空")
            return
        }
        if(!vtype_name||vtype_name==""){
            alert("类型名称不能为空")
            return
        }
        vtype_info_dlg.vtype_code = vtype_code;
        vtype_info_dlg.vtype_name = vtype_name
        vtype_info_dlg.row_id = $(vtype_info_dlg.dom_id + ' #vtype_list_id').val();

        return true;
    };
    vtype_info_dlg.post = function () {
        if (vtype_info_dlg.update === 1) {
            ywl.ajax_post_json('/vtype/edit', {vtype_name: vtype_info_dlg.vtype_name, id: vtype_info_dlg.row_id},
                function (ret) {
                    if (ret.code === TPE_OK) {
                        vtype_info_dlg.tbl.reload();
                        ywl.notify_success('更新类型成功！');
                        vtype_info_dlg.hide();
                    } else {
                        ywl.notify_error('更新类型失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，更新类型失败！');
                }
            );
        } else {
            ywl.ajax_post_json('/vtype/add', {vtype_code: vtype_info_dlg.vtype_code, vtype_name: vtype_info_dlg.vtype_name},
                function (ret) {
                    if (ret.code === TPE_OK) {
                        vtype_info_dlg.tbl.reload();
                        ywl.notify_success('添加类型成功！');
                        vtype_info_dlg.hide();
                    }  else {
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
    $(vtype_info_dlg.dom_id + " #btn-save").click(function () {
        if (!vtype_info_dlg.check_args()) {
            return;
        }
        vtype_info_dlg.post();
    });
    return vtype_info_dlg
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

        }else if (col_key==="action"){
            var row_data = tbl.get_row(row_id);

            function download(id,type) {
                ywl.ajax_post_json('/plugin/download', {
                        id: id,
                        type: type
                    },
                    function (ret) {
                        if (ret.code === TPE_OK) {

                            ywl.notify_success('添加类型成功！');
                        } else {
                            ywl.notify_error('添加类型失败：' + ret.message);
                        }
                    },
                    function () {
                        ywl.notify_error('网络故障，添加类型失败！');
                    }
                );
            }

            $(cell_obj).find('[ywl-btn-download_u]').click(function () {
                // download(row_data.id,)
            });
            $(cell_obj).find('[ywl-btn-download_c]').click(function () {
                alert("c")
            });
            $(cell_obj).find('[ywl-btn-download_t]').click(function () {
                alert("t")
            });
            $(cell_obj).find('[ywl-btn-download_m]').click(function () {
                alert("m")
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
            if (fields.update_url != "" && fields.update_url != null) {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-download_u="' + fields.ID + '">下载update</a>&nbsp');

            }
            if (fields.core_url != "" && fields.core_url != null) {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-download_c="' + fields.ID + '">下载core</a>&nbsp');

            }
            if (fields.tools_url != "" && fields.tools_url != null) {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-download_t="' + fields.ID + '">下载tools</a>&nbsp');

            }
            if (fields.module_url != "" && fields.module_url != null) {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-download_m="' + fields.ID + '">下载module</a>&nbsp');

            }
                return ret.join('');
        }
         render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T"," ") + ' </span>';
        };
    };
};



