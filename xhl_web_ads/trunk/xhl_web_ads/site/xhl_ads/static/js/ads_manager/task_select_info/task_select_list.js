var v_dlg = null;
var icom_dupdate = '';
var plat_list = '';
var create_table_filter_schedule_list = null;
var create_table_filter_package_list = null;



var level_dat = '';
var schedule_id_dat = '';
var package_id_dat = '';
var task_result_dat = '';




function getRoominfo(that) {
    var source_link = $(that).attr("value");
    if (source_link == "null" || source_link == '') {
        alert("暂时无法获取直播间地址");
        return;
    }
    window.open(source_link);
}

// var ywl_plat_id=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#taskselectlist-list';


    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='taskselectlist-list']",
        data_source: {
            type: 'ajax-post',
            url: '/taskselectlist/list'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [

            {
                title: "任务ID", key: "task_id", width: 10, render: 'format_task', fields: {id: 'task_id'}
            },
            {title: "用户ID", key: "user_id", width: 10},
            {title: "主播级别", key: "anchor_level", width: 10},
            {
                title: "schedule_id", key: "schedule_id", width: 10, render: 'format_ads',
                fields: {ads_schedule_id_list: 'schedule_id'}
            },
            {
                title: "平台ID", key: "plat_id", width: 10
            }, {
                title: "平台名称", key: "platfrom_name", width: 10
            },
            {
                title: "昵称", key: "emcee", width: 10
            },
            {
                title: "房间ID", key: "room_id", width: 10, render: 'format_roominfo',
                fields: {source_link: 'source_link', room_id: "room_id"}
            },

            // {
            //     title: "任务状态", key: "task_status_name", width: 10, render: 'format_task_status',
            //     fields: {anchor_balance: 'task_status_name', union_balance: "task_status_name"}
            // },
            {
                title: "任务状态", key: "task_name", width: 10, render: 'format_task_result',
                fields: {anchor_balance: 'task_name', union_balance: "task_name"}
            },
            {
                title: "完成程度", key: "play_log", width: 10, render: 'format_result_end',
                fields: {
                    anchor_balance: 'play_log',
                    union_balance: "play_log",
                    task_play_log_end: "task_play_log_end",
                    task_play_log: "task_play_log"
                }
            },
            {title: "预计收入", key: "estmate_income", width: 10},
            {
                title: "任务接受时间", key: "task_create_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'task_create_time'}
            },
            {
                title: "开始推流时间", key: "stream_start_time", width: 10, render: 'format_time', sort: true,
                fields: {logtime: 'stream_start_time'}
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
    document.getElementById("date").value = "" + getDate() + "";

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    });

    $(dom_id + " [ywl-filter='select']").click(function () {
        host_table.load_data(cb_stack, {}, 'search')
    });

    $(dom_id + " [ywl-filter='update']").click(function () {
        // host_table.load_data(cb_stack, {})
        var level = level_dat;
        var schedule_id = schedule_id_dat;
        var package_id = package_id_dat;
        var task_result = task_result_dat;

        var room_id = $('input[id=room_id]').val();
        var user_id = $('input[id=user_id]').val();
        var date = $('input[id=date]').val();
        var task_id = $('input[id=task_id]').val();

        var isFirefox = /firefox/i.test(navigator.userAgent);

        $.get("/taskselectlist/update?level=" + level + "&schedule_id=" + schedule_id + "&package_id=" + package_id + "&task_result=" + task_result + "&room_id=" + room_id + "&user_id=" + user_id + "&date=" + date + "&task_id=" + task_id, function (result) {
            // alert(result.data);
            var url = result.data;
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

    });


    ywl.create_table_filter_task_result_list(host_table, dom_id + " [ywl-filter='task_result']");
    // ywl.create_table_filter_task_status_list(host_table, dom_id + " [ywl-filter='task_status']");
    // ywl.create_table_filter_close_account_list(host_table, dom_id + " [ywl-filter='close_account']");
    // ywl.create_table_filter_is_audit_list(host_table, dom_id + " [ywl-filter='is_audit']");

    ywl.create_table_filter_leveltype_list(host_table, dom_id + " [ywl-filter='level']");
    create_table_filter_schedule_list = ywl.create_table_filter_shch_list(host_table, dom_id + " [ywl-filter='schedule_id']");
    create_table_filter_package_list = ywl.create_table_filter_package_list(host_table, dom_id + " [ywl-filter='package_id']");
    // create_table_filter_platform_list = ywl.create_table_filter_platform_list(host_table, dom_id + " [ywl-filter='platform_id']");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='date']", "", "date");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='user_id']", "", "user_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='plat_id']", "", "plat_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='room_id']", "", "room_id");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='task_id']", "", "task_id");

    $.get("/advertisingplanlist/scheduleid?level=" + icom_dupdate, function (ret) {
            plat_list = ret;
            create_table_filter_schedule_list.init();
        }
    );
    $.get("/taskselectlist/package_list?", function (ret) {
            plat_list = ret;
            create_table_filter_package_list.init();
        }
    );

    // create_table_filter_package_list.init();

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

        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }

    })
}


function showDetailVideo(that) {
    if ($(that).attr("value") && $(that).attr("value") != "null" && $(that).attr("value") != "" && $(that).attr("value") != "None") {
        var arr = $(that).attr("value").split(",");
        window.open(arr)

    } else {
        alert("该播放记录暂无视频信息");
    }

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
    $.get("/taskselectlist/play_log?task_id=" + id, function (ret) {
        if (ret.code === 0) {
            $("#taskplayloginfo tbody").html("");
            for (var i = 0; i < ret.data.length; i++) {
                $("#taskplayloginfo").append("<tr><td>" + ret.data[i].play_id + "</td><td>" + ret.data[i].user_id + "</td><td>" + ret.data[i].status + "</td><td>" + ret.data[i].popularity + "</td><td><a href='javascript:void(0)' onclick='showDetail(this)' class='btn btn-sm btn-primary' value=" + ret.data[i].screen_shot_path + ">查看截图</a></td><td><a href='javascript:void(0)' onclick='showDetailVideo(this)' class='btn btn-sm btn-primary' value=" + ret.data[i].record_path + ">查看视频</a></td><td>" + ret.data[i].verify_status + "</td><td>" + ret.data[i].verify_result + "</td><td>" + ret.data[i].income + "</td><td>" + ret.data[i].log_create_time + "</td><tr>")
            }

            $("#dialog-taskplayloginfo-info").modal();

        } else if (ret.code === -1) {
            ywl.notify_error('' + ret.message);
        }

    })
}


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

        render.format_task_result = function (row_id, fields) {
            var temp = '未知';
            if (fields.union_balance === '未开始') {
                temp = '<span class="badge badge-danger mono">未开始</span>'
            } else if (fields.union_balance === '已完成') {
                temp = '<span class="badge badge-success mono">已完成</span>'
            } else if (fields.union_balance === '进行中') {
                temp = '<span class="badge badge-primary mono">进行中</span>'
            } else if (fields.union_balance === '已放弃') {
                temp = '<span class="badge badge-danger mono">已放弃</span>'
            } else if (fields.union_balance === '已过期') {
                temp = '<span class="badge badge-danger mono">已过期</span>'
            }
            return '<label style="color: red">' + temp + '</label>'
        };

        // render.format_task_status = function (row_id, fields) {
        //     var temp = '未处理'
        //     if (fields.union_balance === '未开始') {
        //         temp = '<span class="badge badge-danger mono">未开始</span>'
        //     } else if (fields.union_balance === '已结束') {
        //         temp = '<span class="badge badge-success mono">已结束</span>'
        //     } else if (fields.union_balance === '正在进行') {
        //         temp = '<span class="badge badge-primary mono">正在进行</span>'
        //     }
        //     return '<label style="color: red">' + temp + '</label>'
        // };

        render.format_roominfo = function (row_id, fields) {

            var room_id = fields.room_id == null ? '' : fields.room_id
            return '<a href="javascript:void (0);" onclick="getRoominfo(this)" value=' + fields.source_link + ' >' + room_id + '</a>'

        };

        render.format_result_end = function (row_id, fields) {

            if (fields.task_play_log_end < fields.task_play_log) {
                temp = '<span class="badge badge-danger mono">' + fields.union_balance + '</span>'
            } else {
                temp = '<span class="badge badge-success mono">' + fields.union_balance + '</span>'
            }

            return '<label style="color: red">' + temp + '</label>'
        };

        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };
    };
};


ywl.create_table_filter_task_result_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'task_result';
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
        node += '<li><a href="javascript:;" ywl-income-from="' + 0 + '">未开始 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 1 + '">进行中 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 2 + '">已完成 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 3 + '">已放弃 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 4 + '">已过期 </a></li>'
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
        task_result_dat = income_from;

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

ywl.create_table_filter_task_status_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'task_status';
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
        node += '<li><a href="javascript:;" ywl-income-from="' + 0 + '">未开始 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 1 + '">正在进行 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 5 + '">已结束 </a></li>'
        node += '<li><a href="javascript:;" ywl-income-from="' + 15 + '">正在进行&&已结束 </a></li>'
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
        node += '<li><a href="javascript:;" ywl-level-from="">所有</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // node += '<li><a href="javascript:;" ywl-income-from="' + 0 + '"> 未处理 </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="S">S </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="A">A </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="B">B </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="C">C </a></li>'
        node += '<li><a href="javascript:;" ywl-level-from="D">D </a></li>'
        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('所有');

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
        level_dat = income_from;
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

        $.get("/advertisingplanlist/scheduleid?level=" + icom_dupdate, function (ret) {
                // var auxArr = [];
                // $.each(ret, function (k, v) {
                //     $("#ads_schedule_id_list").append("<option value='" + v["schedule_id"] + "'>" + v["description"] + "</option>");
                // });
                plat_list = ret;
                create_table_filter_shch_list.init();
            }
        );

    };


    return _tblf_st;
};


ywl.create_table_filter_shch_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'schedule_id';
    _tblf_st.filter_default = '';
    _tblf_st.filter_value = '';

    _tblf_st.get_filter = function () {
        var _ret = {};
        _ret[_tblf_st.filter_name] = _tblf_st.filter_value;
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
        // var plat_list = '';
        // $.get("/advertisingplanlist/scheduleid?level=" + icom_dupdate, function (ret) {
        //         // var auxArr = [];
        //         // $.each(ret, function (k, v) {
        //         //     $("#ads_schedule_id_list").append("<option value='" + v["schedule_id"] + "'>" + v["description"] + "</option>");
        //         // });
        //         plat_list = ret;
        //     }
        // );
        node += '<li><a href="javascript:;" ywl-schedule-id="">所有</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // alert(plat_list);
        // console.log(plat_list);
        if (plat_list === '') {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-schedule-id="' + '' + '">' + '' + '</a></li>';
            });
        } else {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-schedule-id="' + g[0] + '">' + g[1] + '</a></li>';
            });
        }

        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('所有');

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-schedule-id]').click(_tblf_st._on_select);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var plat_id_html = $(this).html();
        var plat_id = $(this).attr("ywl-schedule-id");
        schedule_id_dat = plat_id;


        var cb_stack = CALLBACK_STACK.create();
        cb_stack
            .add(_tblf_st._table_ctrl.load_data)
            .add(function (cb_stack) {
                _tblf_st.filter_value = plat_id;
                $(_tblf_st.selector + ' button span:first').html(plat_id_html);
                // cb_stack.exec();
            });
        cb_stack.exec();
    };

    return _tblf_st;
};


ywl.create_table_filter_package_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'package_id';
    _tblf_st.filter_default = '';
    _tblf_st.filter_value = '';

    _tblf_st.get_filter = function () {
        var _ret = {};
        _ret[_tblf_st.filter_name] = _tblf_st.filter_value;
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
        // var plat_list = '';
        // $.get("/advertisingplanlist/scheduleid?level=" + icom_dupdate, function (ret) {
        //         // var auxArr = [];
        //         // $.each(ret, function (k, v) {
        //         //     $("#ads_schedule_id_list").append("<option value='" + v["schedule_id"] + "'>" + v["description"] + "</option>");
        //         // });
        //         plat_list = ret;
        //     }
        // );
        node += '<li><a href="javascript:;" ywl-schedule-id="">所有</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // alert(plat_list);
        // console.log(plat_list);
        if (plat_list === '') {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-schedule-id="' + '' + '">' + '' + '</a></li>';
            });
        } else {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-schedule-id="' + g[0] + '">' + g[1] + '</a></li>';
            });
        }

        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('所有');

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-schedule-id]').click(_tblf_st._on_select);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var plat_id_html = $(this).html();
        var plat_id = $(this).attr("ywl-schedule-id");
        package_id_dat = plat_id;


        var cb_stack = CALLBACK_STACK.create();
        cb_stack
            .add(_tblf_st._table_ctrl.load_data)
            .add(function (cb_stack) {
                _tblf_st.filter_value = plat_id;
                $(_tblf_st.selector + ' button span:first').html(plat_id_html);
                // cb_stack.exec();
            });
        cb_stack.exec();
    };

    return _tblf_st;
};


ywl.create_table_filter_platform_list = function (tbl, selector, on_created) {
    var _tblf_st = {};

    // 此表格绑定的DOM对象的ID，用于JQuery的选择器
    _tblf_st.selector = selector;
    // 此过滤器绑定的表格控件
    _tblf_st._table_ctrl = tbl;
    _tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

    // 过滤器内容
    _tblf_st.filter_name = 'platform_id';
    _tblf_st.filter_default = '';
    _tblf_st.filter_value = '';

    _tblf_st.get_filter = function () {
        var _ret = {};
        _ret[_tblf_st.filter_name] = _tblf_st.filter_value;
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
        // var plat_list = '';
        // $.get("/advertisingplanlist/scheduleid?level=" + icom_dupdate, function (ret) {
        //         // var auxArr = [];
        //         // $.each(ret, function (k, v) {
        //         //     $("#ads_schedule_id_list").append("<option value='" + v["schedule_id"] + "'>" + v["description"] + "</option>");
        //         // });
        //         plat_list = ret;
        //     }
        // );
        node += '<li><a href="javascript:;" ywl-plat-id="">所有</a></li>';
        node += '<li role="separator" class="divider"></li>';
        // alert(plat_list);
        console.log(plat_list);
        if (plat_list === '') {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-plat-id="' + '' + '">' + '' + '</a></li>';
            });
        } else {
            $.each(plat_list, function (i, g) {
                node += '<li><a href="javascript:;" ywl-plat-id="' + g[0] + '">' + g[1] + '</a></li>';
            });
        }


        _tblf_st.filter_value = _tblf_st.filter_default;
        $(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
        $(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('所有');

        // 点击事件绑定
        $(_tblf_st.selector + ' ul [ywl-plat-id]').click(_tblf_st._on_select);

        if (_.isFunction(on_created)) {
            on_created(_tblf_st);
        }

        cb_stack.exec();
    };

    _tblf_st._on_select = function () {
        var plat_id_html = $(this).html();
        var plat_id = $(this).attr("ywl-plat-id");
        ywl_plat_id = plat_id
        var cb_stack = CALLBACK_STACK.create();
        cb_stack
            .add(_tblf_st._table_ctrl.load_data)
            .add(function (cb_stack) {
                _tblf_st.filter_value = plat_id;
                $(_tblf_st.selector + ' button span:first').html(plat_id_html);
                // cb_stack.exec();
            });
        cb_stack.exec();
    };

    return _tblf_st;
};