var v_dlg = null
var host_table =null

ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#contractpackageinfo-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='contractpackageinfo-list']",
        data_source: {
            type: 'ajax-post',
            url: '/contract_package_info_all/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: '<input type="checkbox" id="host-select-all" value="">',
                key: 'select_all',
                sort: false,
                width: 20,
                render: 'make_check_box',
                fields: {id: 'package_id'}
            },
            {
                title: "套餐ID", key: "package_id", width: 30, fields: {package_id: 'package_id'}
            },
            {
                title: "财务编号",
                key: "affairs_num",
                width: 50,
                render: 'affairs_num_id',
                fields: {affairs_num_id: 'affairs_num', package_id: 'package_id'}
            },
            {title: "套餐名称", key: "package_name", width: 50},
            {title: "合同ID", key: "contract_id", width: 10},
            {title: "套餐价格", key: "package_price", width: 10},
            {
                title: "开始时间", key: "begin_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'begin_time'}
            },
            {
                title: "结束时间", key: "end_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'end_time'}
            },
            {title: "主播人数", key: "anchor_need", width: 10},
            {title: "主播播放次数", key: "anchor_play_count", width: 10},

            {title: "S", key: "S", width: 10},
            {title: "A", key: "A", width: 10},
            {title: "B", key: "B", width: 10},
            {title: "C", key: "C", width: 10},
            {title: "D", key: "D", width: 10},
            {title: "状态", key: "status", width: 10 ,render:'format_status', fields: {status: 'status'}},
            // {
            //     title: "创建时间", key: "create_time", width: 180, render: 'format_time', sort: true,
            //     fields: {logtime: 'create_time'}
            // },
            // {title: "create_time", key: "create_time",width: 10},
            {
                title: "操作",
                key: "action",
                width: 100,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'package_id', protocol: 'package_id'}
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


    $("#btn-delete-host").click(function () {
        var ids = [];
        var _objs = $(host_table.selector + " tbody tr td [data-check-box]");
        $.each(_objs, function (i, _obj) {
            if ($(_obj).is(':checked')) {
                var _row_data = host_table.get_row(_obj);
                ids.push(_row_data.package_id);
            }
        });

        if (ids.length === 0) {
            ywl.notify_error('请选择要批量删除的套餐！');
            return;
        }

        var _fn_sure = function (cb_stack, cb_args) {
            ywl.ajax_post_json_time_out('/contract_package_info/delete', {ids: ids}, 1000 * 30,
                function (ret) {
                    if (ret.code === TPE_OK) {
                        host_table.reload();
                        ywl.notify_success('删除套餐成功！');
                    } else {
                        ywl.notify_error('删除套餐失败！' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，删除套餐失败！');
                }
            );
        };
        var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>您确定要删除选定的套餐吗？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
    });

    v_dlg = ywl.create_contractpackageinfo_infodlg(host_table);

    $("#btn-add-host").click(function () {

        v_dlg.create_show();
        $("#affairs_num").val("OS-JBP-00001");
    })

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};

// 修改 财务编号
function show_adsInfo(id, pac_id) {
    // alert(id);
    // alert(pac_id);
    ywl.ajax_post_json('/contract_package_info/edit_affairs', {
            affairs_num: id,
            package_id: pac_id
        },
        function (ret) {
            if (ret.code === TPE_OK) {
                // contractpackageinfo_infodlg.tbl.reload();
                ywl.notify_success('更新类型成功！');
                // contractpackageinfo_infodlg.hide();
            } else {
                ywl.notify_error('更新类型失败：' + ret.message);
            }
        },
        function () {
            ywl.notify_error('网络故障，更新类型失败！');
        }
    );
}


ywl.create_contractpackageinfo_infodlg = function (tbl) {
    var contractpackageinfo_infodlg = {};
    contractpackageinfo_infodlg.dom_id = "#dialog-contractpackageinfo-info";
    contractpackageinfo_infodlg.update = 1;
    contractpackageinfo_infodlg.tbl = tbl;


    contractpackageinfo_infodlg.package_id = 0;
    contractpackageinfo_infodlg.package_name = '';
    contractpackageinfo_infodlg.contract_id = 0;
    contractpackageinfo_infodlg.package_price = '';
    contractpackageinfo_infodlg.begin_time = '';
    contractpackageinfo_infodlg.end_time = '';
    contractpackageinfo_infodlg.anchor_need = 0;
    contractpackageinfo_infodlg.anchor_play_count = 0;
    contractpackageinfo_infodlg.affairs_num = '';
    contractpackageinfo_infodlg.S = 0;
    contractpackageinfo_infodlg.A = 0;
    contractpackageinfo_infodlg.B = 0;
    contractpackageinfo_infodlg.C = 0;
    contractpackageinfo_infodlg.D = 0;

    contractpackageinfo_infodlg.update_show = function (package_id, package_name, contract_id, package_price, begin_time, end_time, anchor_need, anchor_play_count, affairs_num, S, A, B, C, D) {
        contractpackageinfo_infodlg.update = 1;
        contractpackageinfo_infodlg.init(package_id, package_name, contract_id, package_price, begin_time, end_time, anchor_need, anchor_play_count, affairs_num, S, A, B, C, D);
        $('#dlg-notice').hide();
        $(contractpackageinfo_infodlg.dom_id).modal();
    };

    contractpackageinfo_infodlg.create_show = function () {
        contractpackageinfo_infodlg.update = 0;
        contractpackageinfo_infodlg.init('', '', 0, 0);
        $('#dlg-notice').show();
        $(contractpackageinfo_infodlg.dom_id).modal();
    };

    contractpackageinfo_infodlg.hide = function () {
        $(contractpackageinfo_infodlg.dom_id).modal('hide');
    };

    contractpackageinfo_infodlg.init = function (package_id, package_name, contract_id, package_price, begin_time, end_time, anchor_need, anchor_play_count, affairs_num, S, A, B, C, D) {
        contractpackageinfo_infodlg.package_id = package_id;
        contractpackageinfo_infodlg.package_name = package_name;
        contractpackageinfo_infodlg.contract_id = contract_id;
        contractpackageinfo_infodlg.package_price = package_price;
        contractpackageinfo_infodlg.begin_time = begin_time ? begin_time.replace("T", " ") : "";
        contractpackageinfo_infodlg.end_time = end_time ? end_time.replace("T", " ") : "";
        contractpackageinfo_infodlg.anchor_need = anchor_need;
        contractpackageinfo_infodlg.anchor_play_count = anchor_play_count;
        contractpackageinfo_infodlg.affairs_num = affairs_num;
        contractpackageinfo_infodlg.S = S;
        contractpackageinfo_infodlg.A = A;
        contractpackageinfo_infodlg.B = B;
        contractpackageinfo_infodlg.C = C;
        contractpackageinfo_infodlg.D = D;
        contractpackageinfo_infodlg.init_dlg();
    };
    contractpackageinfo_infodlg.init_dlg = function () {
        $(contractpackageinfo_infodlg.dom_id + ' #package_id').val(contractpackageinfo_infodlg.package_id);
        $(contractpackageinfo_infodlg.dom_id + ' #package_name').val(contractpackageinfo_infodlg.package_name);
        $(contractpackageinfo_infodlg.dom_id + ' #contract_id').val(contractpackageinfo_infodlg.contract_id);
        $(contractpackageinfo_infodlg.dom_id + ' #package_price').val(contractpackageinfo_infodlg.package_price);
        $(contractpackageinfo_infodlg.dom_id + ' #begin_time').val(contractpackageinfo_infodlg.begin_time);
        $(contractpackageinfo_infodlg.dom_id + ' #end_time').val(contractpackageinfo_infodlg.end_time);
        $(contractpackageinfo_infodlg.dom_id + ' #anchor_need').val(contractpackageinfo_infodlg.anchor_need);
        $(contractpackageinfo_infodlg.dom_id + ' #anchor_play_count').val(contractpackageinfo_infodlg.anchor_play_count);
        $(contractpackageinfo_infodlg.dom_id + ' #affairs_num').val(contractpackageinfo_infodlg.affairs_num);
        $(contractpackageinfo_infodlg.dom_id + ' #S').val(contractpackageinfo_infodlg.S);
        $(contractpackageinfo_infodlg.dom_id + ' #A').val(contractpackageinfo_infodlg.A);
        $(contractpackageinfo_infodlg.dom_id + ' #B').val(contractpackageinfo_infodlg.B);
        $(contractpackageinfo_infodlg.dom_id + ' #C').val(contractpackageinfo_infodlg.C);
        $(contractpackageinfo_infodlg.dom_id + ' #D').val(contractpackageinfo_infodlg.D);
    };

    contractpackageinfo_infodlg.check_args = function () {
        // var package_id = $(contractpackageinfo_infodlg.dom_id + ' #package_id').val();
        var package_name = $(contractpackageinfo_infodlg.dom_id + ' #package_name').val();
        var contract_id = $(contractpackageinfo_infodlg.dom_id + ' #contract_id').val();
        var package_price = $(contractpackageinfo_infodlg.dom_id + ' #package_price').val();
        var begin_time = $(contractpackageinfo_infodlg.dom_id + ' #begin_time').val();
        var end_time = $(contractpackageinfo_infodlg.dom_id + ' #end_time').val();
        var anchor_need = $(contractpackageinfo_infodlg.dom_id + ' #anchor_need').val();
        var anchor_play_count = $(contractpackageinfo_infodlg.dom_id + ' #anchor_play_count').val();
        var affairs_num = $(contractpackageinfo_infodlg.dom_id + ' #affairs_num').val();
        var S = $(contractpackageinfo_infodlg.dom_id + ' #S').val();
        var A = $(contractpackageinfo_infodlg.dom_id + ' #A').val();
        var B = $(contractpackageinfo_infodlg.dom_id + ' #B').val();
        var C = $(contractpackageinfo_infodlg.dom_id + ' #C').val();
        var D = $(contractpackageinfo_infodlg.dom_id + ' #D').val();
        if (!contract_id || contract_id == "") {
            alert("合同编号不能为空")
            return
        }
        if (!package_name || package_name == "") {
            alert("套餐名称不能为空")
            return
        }

        // contractpackageinfo_infodlg.package_id = package_id
        contractpackageinfo_infodlg.package_name = package_name
        contractpackageinfo_infodlg.contract_id = contract_id
        contractpackageinfo_infodlg.package_price = package_price
        contractpackageinfo_infodlg.begin_time = begin_time
        contractpackageinfo_infodlg.end_time = end_time
        contractpackageinfo_infodlg.anchor_need = anchor_need
        contractpackageinfo_infodlg.anchor_play_count = anchor_play_count
        contractpackageinfo_infodlg.affairs_num = affairs_num
        contractpackageinfo_infodlg.S = S
        contractpackageinfo_infodlg.A = A
        contractpackageinfo_infodlg.B = B
        contractpackageinfo_infodlg.C = C
        contractpackageinfo_infodlg.D = D

        return true;
    };
    contractpackageinfo_infodlg.post = function () {
        if (contractpackageinfo_infodlg.update === 1) {

            ywl.ajax_post_json('/contract_package_info/edit', {
                    package_id: contractpackageinfo_infodlg.package_id,
                    package_name: contractpackageinfo_infodlg.package_name,
                    contract_id: contractpackageinfo_infodlg.contract_id,
                    package_price: contractpackageinfo_infodlg.package_price,
                    begin_time: contractpackageinfo_infodlg.begin_time,
                    end_time: contractpackageinfo_infodlg.end_time,
                    anchor_need: contractpackageinfo_infodlg.anchor_need,
                    anchor_play_count: contractpackageinfo_infodlg.anchor_play_count,
                    affairs_num: contractpackageinfo_infodlg.affairs_num,
                    S: contractpackageinfo_infodlg.S,
                    A: contractpackageinfo_infodlg.A,
                    B: contractpackageinfo_infodlg.B,
                    C: contractpackageinfo_infodlg.C,
                    D: contractpackageinfo_infodlg.D
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        contractpackageinfo_infodlg.tbl.reload();
                        ywl.notify_success('更新类型成功！');
                        contractpackageinfo_infodlg.hide();
                    } else {
                        ywl.notify_error('更新类型失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，更新类型失败！');
                }
            );
        } else {
            ywl.ajax_post_json('/contract_package_info/add', {

                    // package_id: contractpackageinfo_infodlg.package_id,
                    package_name: contractpackageinfo_infodlg.package_name,
                    contract_id: contractpackageinfo_infodlg.contract_id,
                    package_price: contractpackageinfo_infodlg.package_price,
                    begin_time: contractpackageinfo_infodlg.begin_time,
                    end_time: contractpackageinfo_infodlg.end_time,
                    anchor_need: contractpackageinfo_infodlg.anchor_need,
                    anchor_play_count: contractpackageinfo_infodlg.anchor_play_count,
                    affairs_num: contractpackageinfo_infodlg.affairs_num,
                    S: contractpackageinfo_infodlg.S,
                    A: contractpackageinfo_infodlg.A,
                    B: contractpackageinfo_infodlg.B,
                    C: contractpackageinfo_infodlg.C,
                    D: contractpackageinfo_infodlg.D
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        contractpackageinfo_infodlg.tbl.reload();
                        ywl.notify_success('添加类型成功！');
                        contractpackageinfo_infodlg.hide();
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
    $(contractpackageinfo_infodlg.dom_id + " #btn-save").click(function () {
        if (!contractpackageinfo_infodlg.check_args()) {
            return;
        }
        contractpackageinfo_infodlg.post();
    });
    return contractpackageinfo_infodlg
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

                v_dlg.update_show(row_data.package_id, row_data.package_name, row_data.contract_id, row_data.package_price, row_data.begin_time, row_data.end_time, row_data.anchor_need, row_data.anchor_play_count, row_data.affairs_num, row_data.S, row_data.A, row_data.B, row_data.C, row_data.D)
            });

            $(cell_obj).find('[ywl-btn-end]').click(function () {
                function _fn_sure() {
                    ywl.ajax_post_json('/incomeanchor/settle', {
                            "package_id": row_data.package_id,
                            "type": "1"
                        },
                        function (ret) {
                            if (ret.code === TPE_OK) {
                                ywl.notify_success('设置完成成功！');
                                host_table.reload()
                            } else {
                                ywl.notify_error('设置完成失败：' + ret.message);
                            }
                        },
                        function () {
                            ywl.notify_error('网络故障，设置完成失败！');
                        }
                    );
                }
                var cb_stack = CALLBACK_STACK.create();

                ywl.dlg_confirm(cb_stack, {
                    msg: '<p>您确定要将此套餐设置为完成吗？此操作不可恢复！！</p>',
                    fn_yes: _fn_sure
                });
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
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-edit="' + fields.ID + '">修改</a>&nbsp');
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-end="' + fields.ID + '">完成</a>&nbsp');
            return ret.join('');
        };


        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };

        render.affairs_num_id = function (row_id, fields) {
            return '<input style="color:#0c91e5;border-top: 0px;border-left: 0px;,border-right: 0px;" value=" ' + fields.affairs_num_id + '" onchange="show_adsInfo(this.value,' + fields.package_id + ')"></input>';
        };

        render.format_status = function (row_id, fields) {

               var temp='未知'
            if(fields.status==1){
                temp='<span class="badge badge-success mono">正在执行</span>'
            }else if(fields.status==2){
                temp='<span class="badge badge-primary mono">完成</span>'
            }
            return '<label style="color: red">'+temp+'</label>'
        };


    };
};



