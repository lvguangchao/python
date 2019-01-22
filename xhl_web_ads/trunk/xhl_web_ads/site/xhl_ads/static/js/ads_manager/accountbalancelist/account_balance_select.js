var v_dlg = null;


ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#accountbase-list';
    // alert(cb_args);
    // alert(cb_stack);
    var user_id = document.getElementById("user_id").innerHTML;
    var user_type = document.getElementById("user_type").innerHTML;
    // alert(user_id);
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='account-list']",
        data_source: {
            type: 'ajax-post',
            url: '/accountbalance/income_list?id=' + user_id +'&user_type='+user_type
        },
        // column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {title: "结算log ID", key: "income_log_id", width: 50},
            {title: "公会ID", key: "union_id", width: 50},
            {title: "经纪人ID", key: "agent_id", width: 50},
            {title: "用户ID", key: "user_id", width: 150},
            {title: "任务ID", key: "task_id", width: 150},
            {
                title: "playID", key: "play_id", width: 150
            },
            {title: "平台ID", key: "plat_id", width: 150},
            {title: "房间ID", key: "room_id", width: 150},
            {title: "描述", key: "comment", width: 150},
            {title: "结算价格", key: "income", width: 150},
            {title: "结算类型", key: "income_type_name", width: 150},
            {
                title: "结算来源", key: "income_from_name", width: 150
            },
            {
                title: "时间", key: "logtime", width: 120
            }
        ],
        paging: {selector: dom_id, per_page: paging_big},
        // 可用的属性设置
        have_header: true
        // 可用的回调函数
        // on_created: ywl.on_host_table_created,
        // on_header_created: ywl.on_host_table_header_created

    };
    var temp = host_table_options;
    // var income_type=$("#income_type").val()
    temp = host_table_options;
    var host_table = ywl.create_table(temp);
    // host_table.load_data(cb_stack, {})
    // $("[ywl-filter='select']").click(function () {
    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();

    $(dom_id + " [ywl-filter='update']").click(function () {
        // host_table.load_data(cb_stack, {})
        var isFirefox = /firefox/i.test(navigator.userAgent);

        $.get("/accountbalance/update?id=" + user_id, function (result) {
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

};

