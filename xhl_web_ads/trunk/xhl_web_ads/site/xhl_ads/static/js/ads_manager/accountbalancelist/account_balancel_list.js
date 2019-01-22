var v_dlg = null;
var icom_dupdate = '';
var plat_list = '';
var create_table_filter_shch_list = null;
var host_table = null;
var user_type_data = null;
var agent_id_data = null;
var union_id_data = null;
var user_id_data = null;
var platform_id_data = null;
var room_id_data = null;


function package_list() {
    $.get("/accountbalance/get_package", function (ret) {
            $("#package_id").find("option").remove();
            $.each(ret, function (k, v) {
                $("#package_id").append("<option value='" + v[0] + "'>" + v[1] + "</option>");
            });
            $('#package_id').attr('rebuild');
        }
    );
}

function need_list(user_id) {
    $.get("/accountbalance/get_need_id?user_id=" + user_id, function (ret) {
            $("#need_id").find("option").remove();
            $("#play_id").find("option").remove();
            $("#need_id").append("<option value=''></option>");
            $.each(ret, function (k, v) {
                $("#need_id").append("<option user='" + user_id + "' value='" + v[0] + "'>" + v[1] + "</option>");
            });
            $('#need_id').attr('rebuild');
        }
    );
}

function play_list(that) {
    var need_id = $(that).find("option:selected").val();
    var user_id = $(that).find("option:selected").attr('user');
    $.get("/accountbalance/get_play_id?user_id=" + user_id + "&need_id=" + need_id, function (ret) {
            $("#play_id").find("option").remove();
            $.each(ret, function (k, v) {
                $("#play_id").append("<option value='" + v[0] + "'>" + v[0] + "</option>");
            });
            $('#play_id').attr('rebuild');
        }
    );
}


ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#accountbalancelist-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='accountbalancelist-list']",
        data_source: {
            type: 'ajax-post',
            url: '/accountbalance/list'
        },

        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: "用户ID", key: "user_id", width: 10
            },
            {title: "用户身份", key: "user_type_name", width: 10},
            {title: "用户昵称", key: "u_nickname", width: 10},
            {title: "房间ID", key: "room_id", width: 10},
            {title: "平台ID", key: "platform_id", width: 10},
            {title: "经纪人昵称", key: "agent_name", width: 10},
            {
                title: "经纪人ID", key: "agent_id", width: 10
            },
            {title: "公会ID", key: "union_id", width: 10},
            {title: "公会名称", key: "union_name", width: 10},
            {title: "账户余额", key: "balance", width: 10},
            {
                title: "最后统计日", key: "last_stat_date", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'last_stat_date'}
            },
            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {
                    ID: 'user_id',
                    protocol: 'user_id',
                    user_type: 'user_type',
                    agent_id: 'agent_id',
                    union_id: 'union_id',
                    user_id: 'user_id',
                    platform_id: 'platform_id',
                    room_id: 'room_id'
                }
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
    });

    $(dom_id + " [ywl-filter='select']").click(function () {
        host_table.load_data(cb_stack, {},'search')

    });
    package_list();
    // need_list();
    ywl.create_table_filter_user_type_list(host_table, dom_id + " [ywl-filter='user_type']");
    //
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='room_id']", "", "room_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_user_name']", "", "user_name");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_user_id']", "", "user_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_union_name']", "", "union_name");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_union_id']", "", "union_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_agent_id']", "", "id_agent_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='id_agent_name']", "", "id_agent_name");

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();

}
;

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
            $("#btn-save").click(function () {
                if (!whitelist_infodlg.check_args()) {
                    return;
                }
                whitelist_infodlg.post();
            });
        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }

    })
}


function showDetail(that) {
    if ($(that).attr("value") && $(that).attr("value") != "null" && $(that).attr("value") != "" && $(that).attr("value") != "None") {
        var arr = $(that).attr("value").split(",");
        var node = '';
        for (r in arr) {

            node += '<a href=' + arr[r].replace("pic.hub520.com", "pic.xiaohulu.com") + ' target="_blank">' + arr[r].replace("pic.hub520.com", "pic.xiaohulu.com") + '</a>' + "<br/>";
        }
        $("#shot_path").empty();
        $("#shot_path").html(node);
        $("#dialog-playdetail-info").modal();

    } else {
        alert("该播放记录暂无截图信息");
    }

}


function show_taskInfo(id) {
    $.get("/accountbalance/income_list?task_id=" + id, function (ret) {
        if (ret.code === 0) {
            $("#taskplayloginfo tbody").html("");
            for (var i = 0; i < ret.data.length; i++) {

                $("#taskplayloginfo").append("<tr><td>" + ret.data[i].income_log_id + "</td><td>" + ret.data[i].union_id + "</td><td>" + ret.data[i].agent_id + "</td><td>" + ret.data[i].user_id + "</td><td>" + ret.data[i].task_id + "</td><td>" + ret.data[i].play_id + "</td><td>" + ret.data[i].plat_id + "</td><td>" + ret.data[i].room_id + "</td><td>" + ret.data[i].comment + "</td><td>" + ret.data[i].income + "</td><td>" + ret.data[i].income_type_name + "</td><td>" + ret.data[i].income_from_name + "</td><td>" + ret.data[i].logtime.replace('T',' ') + "</td><tr>")
            }

            $("#dialog-taskplayloginfo-info").modal();

        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }

    })
}


function add_income(user_id) {
    $('#add-userincome-action')[0].reset();
    $('#dialog-addincomelist-info').modal();
}




$("#dialog-addincomelist-info" + " #btn-save").click(function () {
    var income_num = $("#income_num").val();
    var play_id = $("#play_id").val();
    var comment = $("#comment").val();
    // user_id = user_id_data;
    if(!income_num){
        alert('金额不能为空')
        return
    }
    if(!play_id){
        alert('play_id不能为空')
        return
    }
    if(!comment){
        alert('描述不能为空')
        return
    }


    ywl.ajax_post_json('/account/income/close/add', {
            income_num: income_num,
            play_id: play_id,
            comment: comment
            // user_id:user_id
        },
        function (ret) {
            if (ret.code === TPE_OK) {
                host_table.reload();
                ywl.notify_success('增加余额成功！');
                $('#dialog-addincomelist-info').modal('hide');
            } else {
                ywl.notify_error('增加余额失败：' + ret.message);
            }
        },
        function () {
            ywl.notify_error('网络故障，增加余额失败！');
        }
    );

});


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

        render.make_action_btn = function (row_id, fields) {
            var ret = [];
            var arr_user_type = fields.user_type;
            if (arr_user_type == 1){
                var arr = fields.ID;
            }else if(arr_user_type==2) {
                var arr = fields.union_id;
            }else if(arr_user_type==3) {
                var arr = fields.agent_id;
            }

            ret.push('<a href=/accountbalance/income_list?id='+arr+'&user_type='+ arr_user_type +' class="btn btn-sm btn-primary" target="_blank">查看</a>');
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" onclick="add_income()">增加</a>&nbsp');
            return ret.join('');
        };


        render.format_ads = function (row_id, fields) {
            var temp = [];
            if (fields.ads_schedule_id_list) {
                var arr = fields.ads_schedule_id_list;
                temp.push('<a href="javascript:void(0)" onclick="show_adsInfo(' + arr + ')">【' + arr + '】</a>')

            }
            return temp.join("  ");
        };

        render.format_task = function (row_id, fields) {
            var temp = [];
            if (fields.id) {
                var arr = fields.id;
                temp.push('<a href="javascript:void(0)" onclick="show_taskInfo(' + arr + ')">【' + arr + '】</a>')

            }
            return temp.join("  ");
        };


        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };
    };
};


ywl.create_table_filter_user_type_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'user_type';
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
                cb_stack.exec();
            });
    };
    _tblf_st.init = function (cb_stack) {
        var node = '';
        var user_list = ywl.page_options.user_list;
        node += '<li><a href="javascript:;" ywl-income-from="">所有</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // node += '<li><a href="javascript:;" ywl-income-from="' + 0 + '"> 未处理 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 1 + '">普通主播 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 2 + '">公会用户 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 3 + '">经纪公司 </a></li>'

        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('所有');

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-income-from]').click(_tblf_st._on_select);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var income_from = $(this).attr("ywl-income-from");
        // icom_dupdate = income_from;
        if (income_from == 1) {
            $("#id_user_name").show();
            $("#id_user_id").show();
            $("#room_id").show();
            $("#id_union_name").hide();
            $("#id_union_id").hide();
            $("#id_agent_id").hide();
            $("#id_agent_name").hide()
        } else if (income_from == 2) {
            $("#id_user_name").hide();
            $("#room_id").hide();
            $("#id_user_id").hide();
            $("#id_union_name").show();
            $("#id_union_id").show();
            $("#id_agent_id").hide();
            $("#id_agent_name").hide()
        } else if (income_from == 3) {
            $("#id_user_name").hide();
            $("#room_id").hide();
            $("#id_user_id").hide();
            $("#id_union_name").hide();
            $("#id_union_id").hide();
            $("#id_agent_id").show();
            $("#id_agent_name").show()
        } else {
            $("#id_user_name").show();
            $("#id_user_id").show();
            $("#room_id").show();
            $("#id_union_name").show();
            $("#id_union_id").show();
            $("#id_agent_id").show();
            $("#id_agent_name").show()
        }
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
