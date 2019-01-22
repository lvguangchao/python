var v_dlg = null;
var icom_dupdate = '';
var plat_list = '';
var create_table_filter_shch_list = null;


function show_adsInfo(id) {
    $.get("/logselectinfo/op_content?id=" + id, function (ret) {
        if (ret.code === 0) {
            document.getElementById('name2').innerHTML = ret.data.apply_name;
            document.getElementById('name1').innerHTML = ret.data.id_name;
            document.getElementById('user_type').innerHTML = ret.data.apply_state;
            document.getElementById('user_id').innerHTML = ret.data.id_id;

            $("#dialog-scheduleinfo-info").modal();

        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }
    })
}

ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#logselectplanlist-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='logselectplanlist-list']",
        data_source: {
            type: 'ajax-post',
            url: '/logselectinfo/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: "op_id", key: "op_id", width: 10, fields: {id: 'op_id'}
            },
            {title: "日志类型", key: "op_name", width: 10},

            {
                title: "操作内容", key: "op_desc", width: 10, render: 'format_ads',
                fields: {op_desc: 'op_desc', op_id: 'op_id'}
            },
            // {title: "描述", key: "op_content", width: 10},
            {
                title: "创建时间", key: "create_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'create_time'}
            }, {
                title: "操作人", key: "op_user_name", width: 10
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


    // alert(date_now);
    document.getElementById("start_time").value = "" + getDate() + "";
    document.getElementById("end_time").value = "" + getDate() + "";
    // //初始化素材下拉框
    // $(document).ready(function() {
    //     $('#ads_schedule_id_list').multiselect();
    // });

    // $.get("/seleteshchedule/select?id=0", function (ret) {
    //         // var auxArr = [];
    //         $.each(ret, function (k, v) {
    //             $("#ads_schedule_id_list").append("<option value='" + v["schedule_id"] + "'>" + v["description"] + "</option>");
    //         });
    //         // $('#ads_schedule_id_list').append(auxArr.join(''));
    //         $('#ads_schedule_id_list').multiselect('rebuild');
    //
    //     }
    // );

    // $.get("/packinfo/select", function (ret) {
    //         var auxArr = [];
    //         $.each(ret, function (k, v) {
    //             auxArr[k] = "<option value='" + v["package_id"] + "'>" + v["package_name"] + "</option>";
    //         });
    //         $('#package_id').append(auxArr.join(''));
    //
    //     }
    // );

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    });

    $(dom_id + " [ywl-filter='select']").click(function () {
        host_table.load_data(cb_stack, {},'search')
    });

    ywl.create_table_filter_leveltype_list(host_table, dom_id + " [ywl-filter='level']");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='start_time']", "", "start_time");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='end_time']", "", "end_time");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='user_id']", "", "user_id");

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



    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

        render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };


        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };

        render.format_ads = function (row_id, fields) {
            var temp = [];
            if (fields.op_desc) {
                var arr = fields.op_desc;
                var op_id = fields.op_id;
                temp.push('<a href="javascript:void(0)" onclick="show_adsInfo(' + op_id + ')">【' + arr + '】</a>')
            }
            return temp.join("  ");
        };

    };


};

// ywl.create_table_filter_search_box = function (tbl, selector, on_created, filter_name) {
//     var _tblf_sb = {};
//     // 此过滤器绑定的DOM对象，用于JQuery的选择器
//     _tblf_sb.selector = selector;
//
//     // 此过滤器绑定的表格控件
//     _tblf_sb._table_ctrl = tbl;
//     _tblf_sb._table_ctrl.append_filter_ctrl(_tblf_sb);
//
//     // 过滤器内容
//     _tblf_sb.filter_name = filter_name;
//     _tblf_sb.filter_default = '';
//
//     _tblf_sb.get_filter = function () {
//         var _val = $(_tblf_sb.selector + " input").val();
//         var _ret = {};
//         _ret[_tblf_sb.filter_name] = _val;
//         return _ret;
//     };
//     _tblf_sb.init = function (cb_stack, cb_args) {
//         // 绑定搜索按钮点击事件
//         // $(_tblf_sb.selector + " button").click(function () {
//         // 	_tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {});
//         // });
//         // 绑定搜索输入框中按下回车键
//         $(_tblf_sb.selector + " input").keydown(function (event) {
//             if (event.which == 13) {
//                 _tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {});
//             }
//         });
//
//         if (_.isFunction(on_created)) {
//             on_created(_tblf_sb);
//         }
//         cb_stack.exec();
//     };
//     return _tblf_sb;
// };


ywl.create_table_filter_leveltype_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'level';
    _tblf_st.filter_default = '';
    _tblf_st.filter_value = '';

    _tblf_st.get_filter = function () {
        var _ret = {};
        _ret[_tblf_st.filter_name] = _tblf_st.filter_value;
        // _ret["package_id"] = $("#package_id").val();
        return _ret;
    };
    _tblf_st.reset = function (cb_stack, cb_args) {
        if (_tblf_st.filter_value == _tblf_st.filter_default) {
            cb_stack.exec();
            return;
        }
        cb_stack
            .add(function (cb_stack) {
                _tblf_st.filter_value = _tblf_st.filter_default;
                $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
                // cb_stack.exec();
            });
    };

    _tblf_st.init = function (cb_stack) {
        var node = '';
        var user_list = ywl.page_options.user_list;
        node += '<li ><a href="javascript:;" ywl-level-from="">全部</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // node += '<li><a href="javascript:;" ywl-income-from="' + 0 + '"> 未处理 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="1">撤回广告 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="2">补贴金额 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="3">提现修改 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="4">审核记录 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="5">广告投放 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="6">自动化审核 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="7">申诉 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="8">数据同步 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="9">修改ads_task_play_log </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="10">增加用户余额 </a></li>'

        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('全部');

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-level-from]').click(_tblf_st._on_select);

        // $(_tblf_st.selector + ' ul [ywl-level-from]').change(_tblf_st._on_change);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var income_from = $(this).attr("ywl-level-from");
        icom_dupdate = income_from;

        var income_from_html = $(this).html();

        var cb_stack = CALLBACK_STACK.create();
        cb_stack
            .add(_tblf_st._table_ctrl.load_data)
            .add(function (cb_stack) {
                _tblf_st.filter_value = income_from;
                $(_tblf_st.selector + ' button span:first').html(income_from_html);
                // cb_stack.exec();
            });
        cb_stack.exec();
    };


    return _tblf_st;
};

