var v_dlg = null
var order_shcedule_id=null
var host_table=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#cal-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='cal-list']",
        data_source: {
            type: 'ajax-post',
            url: '/ads/cal/list'
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
            {title: 'order_id', key: 'order_id', width: 30},
            {title: '广告名称', key: 'order_sche_name', width: 30},
            {title: '广告日期', key: 'order_date', width: 30},
            // {title: 'package_id', key: 'package_id',width: 30},
            {title: '播放次数', key: 'need_play_num', width: 30},
            // {title: 'order_status', key: 'order_status',width: 30},
            {title: 'S(当日/人)', key: 'order_s', width: 30},
            {title: 'A(当日/人)', key: 'order_a', width: 30},
            {title: 'B(当日/人)', key: 'order_b', width: 30},
            {title: 'C(当日/人)', key: 'order_c', width: 30},
            {title: 'D(当日/人)', key: 'order_d', width: 30},
            {title: '素材ID', key: 'adsinfo_id', width: 30, render: "adsinfo_format", fields: {adsinfo_id: 'adsinfo_id'}},
            {title: '创建人', key: 'create_people', width: 30},
            {title: '套餐状态', key: 'status', width: 30, render: 'format_status', fields: {status: 'status'}},
            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {order_id: 'order_id', adsinfo_id: 'adsinfo_id', package_id: 'package_id'}
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
        var vtype_list = [];
        var _objs = $(host_table.selector + " tbody tr td [data-check-box]");
        $.each(_objs, function (i, _obj) {
            if ($(_obj).is(':checked')) {
                var _row_data = host_table.get_row(_obj);
                vtype_list.push(_row_data.need_id);
            }
        });

        if (vtype_list.length === 0) {
            ywl.notify_error('请选择要批量删除的需求！');
            return;
        }

        var _fn_sure = function (cb_stack, cb_args) {
            ywl.ajax_post_json_time_out('/needinfo/delete', {ids: vtype_list}, 1000 * 30,
                function (ret) {
                    if (ret.code === TPE_OK) {
                        host_table.reload();
                        ywl.notify_success('删除成功！');
                    } else {
                        ywl.notify_error('删除失败！' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，删除失败！');
                }
            );
        };
        var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>您确定要删除选定的需求吗？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
    });

    v_dlg = ywl.create_adscal_info_dlg(host_table);

    $("#btn-add-host").click(function () {
        v_dlg.create_show();
    })

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_adscal_info_dlg = function (tbl) {
    var adscal_info_dlg = {};
    adscal_info_dlg.dom_id = "#dialog-adscal-info";
    adscal_info_dlg.update = 1;
    adscal_info_dlg.tbl = tbl;
    adscal_info_dlg.package_id = '';
    adscal_info_dlg.need_play_type = 0;
    adscal_info_dlg.anchor_level = 0;
    adscal_info_dlg.position = 0;
    adscal_info_dlg.ads_id = 0;
    adscal_info_dlg.need_name = 0;
    adscal_info_dlg.enable = 0;
    adscal_info_dlg.description = 0;
    adscal_info_dlg.row_id = 0;

    adscal_info_dlg.update_show = function (package_name, begin_time, end_time,
                                            need_desc, ads_play_num_desc, serving_meth,
                                            is_allow_repeat, adser) {
        adscal_info_dlg.update = 1;
        adscal_info_dlg.init(package_name, begin_time, end_time,
            need_desc, ads_play_num_desc, serving_meth,
            is_allow_repeat, adser);
        $('#dialog-adscal-info #btn-save').hide();
        $(adscal_info_dlg.dom_id).modal();
    };

    adscal_info_dlg.create_show = function () {
        adscal_info_dlg.update = 0;
        adscal_info_dlg.init('', '', '', '', '', '', '', '', 0);
        $('#dialog-adscal-info #btn-save').show();
        $(adscal_info_dlg.dom_id).modal();
    };

    adscal_info_dlg.hide = function () {
        $(adscal_info_dlg.dom_id).modal('hide');
    };

    adscal_info_dlg.init = function (package_name, begin_time, end_time,
                                     need_desc, ads_play_num_desc, serving_meth,
                                     is_allow_repeat, adser) {
        document.getElementById("adscal-list-action").reset();
        // 清空checkbox
        $('input:checkbox').each(function () {
            $(this).prop('checked', false);
        })
        $('#adscal-list-action').find('input,textarea').attr('readonly', false);

        if (adscal_info_dlg.update == 1) {

            $('#adscal-list-action').find('input,textarea').attr('readonly', true);
            end_time = end_time ? end_time.replace("T", ' ') : '';
            begin_time = begin_time ? begin_time.replace("T", ' ') : '';
            $("#package_name").val(package_name);
            $("#begin_time").val(begin_time);
            $("#end_time").val(end_time);
            $("#adser").val(adser);

            need_desc_json = need_desc ? JSON.parse(need_desc) : ''
            ads_play_num_desc_json = ads_play_num_desc ? JSON.parse(ads_play_num_desc) : ''
            $("#serving_meth").val(serving_meth);
            $(":radio[name='is_allow_repeat'][value='" + is_allow_repeat + "']").prop('checked', 'checked');
            if (need_desc_json) {
                $("#S").val(need_desc_json.S)
                $("#A").val(need_desc_json.A)
                $("#B").val(need_desc_json.B)
                $("#C").val(need_desc_json.C)
                $("#D").val(need_desc_json.D)
            }
            if (ads_play_num_desc_json) {
                if (ads_play_num_desc_json.video) {
                    $(":checkbox[name='play'][value='1']").prop('checked', 'checked')
                    $("#play_num1").val(ads_play_num_desc_json.video)

                }
                if (ads_play_num_desc_json.subscript) {
                    $(":checkbox[name='play'][value='2']").prop('checked', 'checked')
                    $("#play_num2").val(ads_play_num_desc_json.subscript)

                }
            }
        }

        adscal_info_dlg.init_dlg();
    };
    adscal_info_dlg.init_dlg = function () {


    };

    adscal_info_dlg.check_args = function () {
        var package_name = $(adscal_info_dlg.dom_id + ' #package_name').val()
        if (!package_name) {
            alert('请填写广告名称')
            return
        }
        var adser = $(adscal_info_dlg.dom_id + ' #adser').val()
        if (!adser) {
            alert('请填写广告主');
            return
        }
        var begin_time = $(adscal_info_dlg.dom_id + ' #begin_time').val()
        if (!begin_time) {
            alert('请填写广告日期')
            return
        }
        var end_time = $(adscal_info_dlg.dom_id + ' #end_time').val()
        // var need_play_type=$("input[name='need_play_type']:checked").val()
        if (!end_time) {
            alert('请填写结束日期')
            return
        }
        var ads_play_num_desc = []
        var ads_play_num = 0
        var json = {};
        $.each($(":checkbox[name='play']:checked"), function () {
            var num = $(this).val();
            var counts = $("#play_num" + num).val();
            ads_play_num += parseInt(counts)
            var type = num == 1 ? 'video' : num == 2 ? 'subscript' : 'other';
            json[type] = counts;
        });
        ads_play_num_desc.push(JSON.stringify(json))

        if (!ads_play_num) {
            alert('请选择广告播放次数')
            return;
        }
        ads_play_num_desc.join("")
        var serving_meth = $(adscal_info_dlg.dom_id + ' #serving_meth').val()
        if (!serving_meth) {
            alert('请选择广告投放方式')
            return
        }
        var s = $(adscal_info_dlg.dom_id + ' #S').val()
        var a = $(adscal_info_dlg.dom_id + ' #A').val()
        var b = $(adscal_info_dlg.dom_id + ' #B').val()
        var c = $(adscal_info_dlg.dom_id + ' #C').val()
        var d = $(adscal_info_dlg.dom_id + ' #D').val()


        var is_allow_repeat = $("input[name='is_allow_repeat']:checked").val();
        // var need_desc=$("#need_desc").val()

        adscal_info_dlg.package_name = package_name;
        adscal_info_dlg.adser = adser;
        adscal_info_dlg.begin_time = begin_time;
        adscal_info_dlg.end_time = end_time;
        adscal_info_dlg.ads_play_num_desc = ads_play_num_desc;
        adscal_info_dlg.serving_meth = serving_meth;
        adscal_info_dlg.is_allow_repeat = is_allow_repeat;
        // adscal_info_dlg.need_desc=need_desc;
        adscal_info_dlg.s = s;
        adscal_info_dlg.a = a;
        adscal_info_dlg.b = b;
        adscal_info_dlg.c = c;
        adscal_info_dlg.d = d;
        adscal_info_dlg.ads_play_num = ads_play_num;

        return true;
    };
    adscal_info_dlg.post = function () {
        if (adscal_info_dlg.update === 1) {
            adscal_info_dlg.hide();

        } else {
            function _fn_sure() {
               ywl.ajax_post_json('/ads/cal/add', {
                    package_name: adscal_info_dlg.package_name,
                    adser: adscal_info_dlg.adser,
                    begin_time: adscal_info_dlg.begin_time,
                    end_time: adscal_info_dlg.end_time,
                    ads_play_num_desc: adscal_info_dlg.ads_play_num_desc,
                    serving_meth: adscal_info_dlg.serving_meth,
                    is_allow_repeat: adscal_info_dlg.is_allow_repeat,
                    // need_desc: adscal_info_dlg.need_desc,
                    s: adscal_info_dlg.s,
                    a: adscal_info_dlg.a,
                    b: adscal_info_dlg.b,
                    c: adscal_info_dlg.c,
                    d: adscal_info_dlg.d,
                    ads_play_num: adscal_info_dlg.ads_play_num
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        adscal_info_dlg.tbl.reload();
                        ywl.notify_success('添加成功！');
                        var cal_date = $("#cal_date").val();
                        getAnchorToday(1, cal_date);
                        adscal_info_dlg.hide();
                    } else {
                        alert(ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，添加失败！');
                }
            );
            }
            var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>您确定要下单么？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
        }
        return true;
    };
    $(adscal_info_dlg.dom_id + " #btn-save").click(function () {
        if (!adscal_info_dlg.check_args()) {
            return;
        }
        adscal_info_dlg.post();
    });
    return adscal_info_dlg
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
                var package_id = $(this).attr('package_id')
                $.get("/contract/package/getbyId?package_id=" + package_id, function (ret) {
                    v_dlg.update_show(ret.package_name, ret.begin_time,
                        ret.end_time, ret.need_desc, ret.ads_play_num_desc, ret.serving_meth, ret.is_allow_repeat, ret.adser)
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
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" ywl-btn-edit  package_id="' + fields.package_id + '">查看详情</a>&nbsp');
            if (!fields.adsinfo_id) {
                ret.push('<a href="javascript:void(0);" onclick="create_adsinfo(' + fields.order_id + ')"  class="btn btn-sm btn-success">添加素材</a>');
            }
            return ret.join('');
        }
        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };

        render.adsinfo_format = function (row_id, fields) {
            var temp = ''
            if (fields.adsinfo_id) {
                temp = '<a href="javascript:void(0)" onclick="show_adsInfo(' + fields.adsinfo_id + ')">' +
                    '【'+fields.adsinfo_id+'】</a>'
            } else {
                temp = '<span class="badge badge-danger mono">缺素材</span>'
            }
            return temp;
        };
        render.format_status = function (row_id, fields) {

            var temp = '未知'
            if (fields.status == 1) {
                temp = '<span class="badge badge-success mono">正在执行</span>'
            } else if (fields.status == 2) {
                temp = '<span class="badge badge-primary mono">完成</span>'
            }
            return '<label style="color: red">' + temp + '</label>'
        };

    };
};


ywl.create_table_filter_search_box = function (tbl, selector, on_created, filter_name) {
    var _tblf_sb = {};
    // 此过滤器绑定的DOM对象，用于JQuery的选择器
    _tblf_sb.selector = selector;

    // 此过滤器绑定的表格控件
    _tblf_sb._table_ctrl = tbl;
    _tblf_sb._table_ctrl.append_filter_ctrl(_tblf_sb);

    // 过滤器内容
    _tblf_sb.filter_name = filter_name ? filter_name : 'search';
    _tblf_sb.filter_default = '';

    _tblf_sb.get_filter = function () {
        var _val = $(_tblf_sb.selector + " input").val();

        var _ret = {};
        _ret[_tblf_sb.filter_name] = _val;
        var cal_date = $("#cal_date").val();
        // var type=$("#type").val();
        _ret['cal_date'] = cal_date;
        // _ret['type'] = type;
        return _ret;

        //return [{k: self.filter_name, v: _val}];
    };

    _tblf_sb.reset = function (cb_stack, cb_args) {
        var _val = $(_tblf_sb.selector + " input").val();

        if (_val != _tblf_sb.filter_default) {
            $(_tblf_sb.selector + " input").val(_tblf_sb.filter_default);
        }

        cb_stack.exec();
    };

    _tblf_sb.init = function (cb_stack, cb_args) {
        // 绑定搜索按钮点击事件
        $(_tblf_sb.selector + " button").click(function () {
            _tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {}, 'search');
        });
        // 绑定搜索输入框中按下回车键
        $(_tblf_sb.selector + " input").keydown(function (event) {
            if (event.which == 13) {
                _tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {}, 'search');
            }
        });

        if (_.isFunction(on_created)) {
            on_created(_tblf_sb);
        }

        cb_stack.exec();
    };

    return _tblf_sb;
};
 // 获取今日主播数量
function getAnchorToday(type, date) {
    $.get("/anchor/invetor/getbyId?type=" + type + "&date=" + date, function (ret) {
        if (ret.code === 0) {
            $("#anchor_invetoy tbody").html("");
            $("#anchor_invetoy").append("<tr>" +
                "<td>" + "已占主播 " + "</td>" +
                "<td>" + ret.data.S + "</td>" +
                "<td>" + ret.data.A + "</td>" +
                "<td>" + ret.data.B + "</td>" +
                "<td>" + ret.data.C + "</td>" +
                "<td>" + ret.data.D + "</td>" +
                "<tr>");

            $("#anchor_invetoy").append("<tr>" +
                "<td><label style='color: red'>" + "剩余可用 " + "</label></td>" +
                "<td><label style='color: red'>" + (ret.data.S_all - ret.data.S) + "</label></td>" +
                "<td><label style='color: red'>" + (ret.data.A_all - ret.data.A) + "</label></td>" +
                "<td><label style='color: red'>" + (ret.data.B_all - ret.data.B) + "</label></td>" +
                "<td><label style='color: red'>" + (ret.data.C_all - ret.data.C) + "</label></td>" +
                "<td><label style='color: red'>" + (ret.data.D_all - ret.data.D) + "</label></td>" +
                "<tr>");
        } else {
            ywl.notify_error('主播库存获取失败');
        }
    })
}
// 添加素材跳转
function create_adsinfo(order_id) {
    // window.open('/adsinfo/list?order_id=' + order_id);
   // 设置 order_id
    document.getElementById("adsinfo-add-action").reset();
    $("#dialog-adsinfo-add #preview").attr("src","");
    order_shcedule_id=order_id
    $("#dialog-adsinfo-add").modal();
}

function progressHandlingFunction(e) {
    var ads_materialurl = $("#dialog-adsinfo-add #ads_materialurl").val()
    if (ads_materialurl && ads_materialurl != "") {
        if (e.lengthComputable) {
            $('#dialog-adsinfo-add' + ' #process_data1').attr({value: e.loaded, max: e.total}); //更新数据到进度条
            var percent = e.loaded / e.total * 100;
            $('#dialog-adsinfo-add' + ' #progress1').html(e.loaded + "/" + e.total + " bytes. " + percent.toFixed(2) + "%");
        }
    }
}

 $('#dialog-adsinfo-add' + " #btn-save").click(function () {
     $(this).attr('disabled','disabled');
      var t = null  //定时对象
            var task_gen = null  //task编号
            $.get("/get/task/gen", function (ret) {
                    task_gen = ret.data
                    var fileInput = $("#dialog-adsinfo-add #ads_materialurl")[0];
                    if (fileInput && fileInput.files.length != 0) {
                        var byteSize = fileInput.files[0].size;
                        //step-2  定时获取文件上传进度
                        t = setInterval(function () {
                            $.get("/get/task/process", {task_gen: task_gen}, function (ret) {
                                    if (ret.code === TPE_OK) {
                                        $('#dialog-adsinfo-add #process_data2').attr({value: ret.data, max: byteSize}); //更新数据到进度条
                                        var percent = ret.data / byteSize * 100;
                                        $('#dialog-adsinfo-add #progress2').html(ret.data + "/" + byteSize + " bytes. " + percent.toFixed(2) + "%");
                                    } else {
                                        ywl.notify_error('获取进度信息失败：' + ret.message);
                                    }
                                }
                            );
                        }, 200);
                    }

                    //step-3  开始文件上传，提交表单
                    var ads_materialurl = $("#dialog-adsinfo-add #ads_materialurl")[0].files[0];        //获取上传文件名称
                    var ads_thumbnailurl = $("#dialog-adsinfo-add #ads_thumbnailurl")[0].files[0];        //获取上传文件名称
                    var form = new FormData();                  //创建表单对象
                    var ads_name = $("#dialog-adsinfo-add #ads_name").val()
                    var ads_contents=$("#dialog-adsinfo-add #ads_contents").val()
                    var ads_time=$("#dialog-adsinfo-add #ads_time").val()
                    // var order_id=$("#order_id").val()

                    form.append("ads_contents", ads_contents);
                    form.append("file", ads_materialurl);
                    form.append("file_pic", ads_thumbnailurl);
                    form.append("task_gen", task_gen);
                    form.append("ads_name", ads_name);
                    form.append("ads_time", ads_time);
                    form.append("order_id", order_shcedule_id);
                    $.ajax({
                        type: 'POST',
                        url: '/adsinfo/add/sale',
                        data: form,                             //提交数据为表单对象
                        processData: false,                     //默认为 true，数据被处理为 URL 编码格式。如果为 false，则阻止将传入的数据处理为 URL 编码的格式。
                        contentType: false,                     //指 定 请 求 内 容 的 类 型
                        success: function (ret) {
                            clearInterval(t);                       //删除定时请求
                            $('#dialog-adsinfo-add' + " #btn-save").removeAttr("disabled");
                            if (ret.code === TPE_OK) {
                                // adsinfo_info_dlg.tbl.reload();
                                ywl.notify_success('添加成功！');
                                $('#dialog-adsinfo-add #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#dialog-adsinfo-add #progress1').html("0 bytes");
                                $('#dialog-adsinfo-add #process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#dialog-adsinfo-add #progress2').html("0 bytes");
                                $("#dialog-adsinfo-add").modal('hide');
                                 host_table.reload();
                            }
                            else {
                                ywl.notify_error('添加失败：' + ret.message);
                            }
                        },
                        error: function (xhr, errorText, errorStatus) {  //如果发生错误，返回错误信息
                            $(adsinfo_info_dlg.dom_id + " #btn-save").removeAttr("disabled");
                            $('#dialog-adsinfo-add #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#dialog-adsinfo-add #progress1').html("0 bytes");
                            $('#dialog-adsinfo-add #process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#dialog-adsinfo-add #progress2').html("0 bytes");
                            clearInterval(t);                       //删除定时请求
                            $('#dialog-adsinfo-add #progress').html("0 bytes");
                            ywl.notify_error('网络故障，添加失败！');
                        },
                        xhr: function () { //获取ajaxSettings中的xhr对象，为它的upload属性绑定progress事件的处理函数
                            myXhr = $.ajaxSettings.xhr();
                            if (myXhr.upload) { //检查upload属性是否存在
                                //绑定progress事件的回调函数
                                myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                            }
                            return myXhr; //xhr对象返回给jQuery使用
                        }

                    })
                }
            );
    });