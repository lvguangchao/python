var v_dlg=null
var host_table=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#autoreview-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='autoreview-list']",
        data_source: {
            type: 'ajax-post',
            url: '/autoreview/list'
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
            {title: "auto_id", key: "auto_id",width: 30},
            {
                title: "审核比例", key: "", width: 50, render: "formatnum",
                fields: {auto_max: "auto_max",auto_now:"auto_now",auto_date:'auto_date'}
            },
            {title: "任务创建日期", key: "auto_date",width: 50},
            {
                title: "审核状态",
                key: "auto_status",
                width: 10,
                render: "formatstatus",
                fields: {auto_status: "auto_status"}
            },
             {title: "审核人", key: "auto_user",width: 50},
            {
                title: "结算比例", key: "", width: 50, render: "formatAccount",
                fields: {verify_num: "verify_num",account_num:"account_num",auto_date:'auto_date',count_money_num:'count_money_num'}
            },

            {
                title: "结算刷新时间", key: "update_time", width: 50, render: 'format_time',
                fields: {logtime: 'update_time'}
            },
            {title: "数据同步操作人", key: "syn_user", width: 50},
            {
                title: "数据同步时间", key: "syn_datetime", width: 40, render: 'format_time',
                fields: {logtime: 'syn_datetime'}
            },
            {
                title: "操作",
                key: "action",
                width: 160,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'ads_id', auto_status: 'auto_status',score_status:'score_status'}
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




    $("#btn-add-host").click(function () {
         v_dlg.create_show();
    })

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");


    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
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
            var date = row_data.auto_date;
            var id = row_data.auto_id;
            var option = {
                url_create: "/autoreview/create?id=" + id,
                url_select: '/autoreview/select',
                dom_id: '#dialog-auto-info',
                url: '/autoreview/audit',
                params: {
                    "date": date,
                    "id": id
                },
                msg: '自动化审核'
            }

            $(cell_obj).find('[ywl-btn-auto]').click(function () {

                var _fn_sure = function (cb_stack, cb_args) {
                    option.that = $(this);
                    process.block_process(option);

                }
                 var cb_stack = CALLBACK_STACK.create();

                ywl.dlg_confirm(cb_stack, {
                    msg: '<p>您确定要开始自动化审核吗？此操作不可恢复！！</p>',
                    fn_yes: _fn_sure
                });
            });

            $(cell_obj).find('[ywl-btn-flush]').click(function () {

                var date = row_data.auto_date;
                var id = row_data.auto_id;
                ywl.ajax_post_json('/autoreview/flush', {
                        date: date,
                        id: id
                    },
                    function (ret) {
                        if (ret.code === TPE_OK) {
                            host_table.reload();
                            ywl.notify_success('刷新成功！');
                        } else {
                            ywl.notify_error('刷新失败：' + ret.message);
                        }
                    },
                    function () {
                        ywl.notify_error('网络故障，刷新失败！');
                    }
                );

            });

            $(cell_obj).find('[ywl-btn-syndata]').click(function () {
                var option = {
                    url_create: "/plat/data/create",
                    url_select: '/plat/data/select',
                    dom_id: '#dialog-syndata-info',
                    url: '/plat/data/synch',
                    params: {
                        "date": date,
                        "id": id
                    },
                    msg: '数据同步'
                };

                var _fn_sure = function () {
                    option.that = $(this);
                    process.block_process(option);
                };
                var cb_stack = CALLBACK_STACK.create();
                ywl.dlg_confirm(cb_stack, {
                    msg: '<p>您确定要开始同步日期:' + date + ' 数据吗？此操作不可恢复！！</p>',
                    fn_yes: _fn_sure
                });

            });
            $(cell_obj).find('[ywl-btn-score]').click(function () {
                var auto_id = row_data.auto_id;
                var date = row_data.auto_date;
                $.ajax({
                    url: "/credit/update?credit_time=" + date + '&auto_id=' + auto_id,
                    type: 'get',
                    success: function (data) {
                        if (data.code == TPE_OK) {
                            alert('信用分更新成功');
                            host_table.reload();
                        } else {
                            alert("信用分更新失败" + data.message);
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        alert('网络故障，信用分更新失败');
                    }
                });

            })

        }
    };

    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

        var url='http://download.xiaohulu.com/obs/adsdownload/'

        render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };
        render.format_time = function (row_id, fields) {
            var temp=fields.logtime?fields.logtime:""
            if (temp){
                return '<span class="badge badge-primary mono">' + temp.replace("T", " ") + ' </span>';
            }else {
                return ''
            }
        };

        render.make_action_btn = function (row_id, fields) {
            var ret = [];
            if (fields.auto_status==1){
                ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" disabled="true">自动化审核</a>&nbsp');
            }else {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-auto="' + fields.ID + '">自动化审核</a>&nbsp');
            }
            if (fields.score_status==1){
                ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" disabled="true">更新信用分</a>&nbsp');
            }else {
                ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-score="' + fields.ID + '">更新信用分</a>&nbsp');
            }
            ret.push('<a href="javascript:;" class="btn btn-sm btn-info" protocol=' + fields.protocol + ' ywl-btn-flush="' + fields.ID + '">刷新</a>&nbsp');
            ret.push('<a href="javascript:;" class="btn btn-sm btn-success" protocol=' + fields.protocol + ' ywl-btn-syndata="' + fields.ID + '">数据同步</a>&nbsp');
            return ret.join('');
        }

        render.formatstatus = function (row_id, fields) {
            var temp = '未知'
            if (fields.auto_status == 0) {
                temp = '<span class="badge badge-danger mono">未审核</span>'
            } else if (fields.auto_status == 1) {
                temp = '<span class="badge badge-success mono">已审核</span>'
            }
            return '<label style="color: red">' + temp + '</label>'
        }
        render.formatnum = function (row_id, fields) {
            var temp=''
            var date=fields.auto_date?fields.auto_date.substr(0,10):getDate()

            if (fields.auto_now < fields.auto_max) {
                temp = '<span class="badge badge-danger mono" style="text-decoration: underline">' + fields.auto_now + "/" + fields.auto_max + '</span>'
            } else {
                temp = '<span class="badge badge-success mono" style="text-decoration: underline">' + fields.auto_now + "/" + fields.auto_max + '</span>'
            }
           return '<a href="/playrecord/read/list?type=1&date=\''+date+ '\'"  target="_blank" >'+temp+'</a>'

        }
        render.formatAccount = function (row_id, fields) {
            var temp = ''
            var min=fields.account_num?fields.account_num:0
            var max=fields.verify_num?fields.verify_num:0
            var count_money_num=fields.count_money_num?fields.count_money_num:0
            var date=fields.auto_date?fields.auto_date.substr(0,10):getDate()

            if (fields.account_num < fields.count_money_num) {
                temp = '<span class="badge badge-danger mono" style="text-decoration: underline">' +min + "/"+ count_money_num + "/"+ max + '</span>'
            } else {
                temp = '<span class="badge badge-success mono" style="text-decoration: underline">' + min + "/"+count_money_num + "/" + max + '</span></a>'
            }
            return '<a href="/playrecord/read/list?type=2&date=\''+date+ '\'"  target="_blank" >'+temp+'</a>'
        }




    };
};

