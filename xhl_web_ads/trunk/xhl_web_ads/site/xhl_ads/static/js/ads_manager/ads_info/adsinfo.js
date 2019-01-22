var v_dlg=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#adsinfo-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='adsinfo-list']",
        data_source: {
            type: 'ajax-post',
            url: '/adsinfo/list'
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
            {title: "ads_id", key: "ads_id",width: 30},
            {title: "素材名称", key: "ads_name",width: 50},
            {title: "时间间隔(s)", key: "ads_time",width: 50},
            {
                title: "视频URL",
                key: "ads_materialurl",
                width: 10,
                render: "moviedown",
                fields: {ads_id: "ads_id",ads_materialurl:"ads_materialurl"}
            },
            {
                title: "图片url",
                key: "ads_thumbnailurl",
                width: 10,
                render: "picturedown",
                fields: { ads_id: "ads_id",ads_thumbnailurl:"ads_thumbnailurl"}
            },
            {
                title: "日志时间", key: "logtime", width: 180, render: 'format_time',sort:true,
                fields: {logtime: 'logtime'}
            },
            {
                title: "操作",
                key: "action",
                width: 50,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'ads_id', protocol: 'ads_id'}
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

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");


    $("#btn-delete-host").click(function () {
        var ids = [];
        var _objs = $(host_table.selector + " tbody tr td [data-check-box]");
        $.each(_objs, function (i, _obj) {
            if ($(_obj).is(':checked')) {
                var _row_data = host_table.get_row(_obj);
                ids.push(_row_data.ads_id);
            }
        });

        if (ids.length === 0) {
            ywl.notify_error('请选择要批量删除的插件类型！');
            return;
        }

        var _fn_sure = function (cb_stack, cb_args) {
            ywl.ajax_post_json_time_out('/adsinfo/delete', {ids: ids}, 1000 * 30,
                function (ret) {
                    if (ret.code === TPE_OK) {
                        host_table.reload();
                        ywl.notify_success('删除成功！');
                    } else {
                        ywl.notify_error('删除失败！'+ ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，删除失败！');
                }
            );
        };
        var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>您确定要删除选定的素材吗？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
    });

    v_dlg = ywl.create_adsinfo_info_dlg(host_table);

    $("#dialog-adsinfovedio-info" + " #btn-save").click(function () {
        var domid = "#dialog-adsinfovedio-info"
        function progressHandlingFunction(e) {
              var ads_materialurl=$("#ads_materialurl").val()
              if (ads_materialurl && ads_materialurl != "") {
                  if (e.lengthComputable) {
                      $(domid+' #process_data1').attr({value: e.loaded, max: e.total}); //更新数据到进度条
                      var percent = e.loaded / e.total * 100;
                      $(domid+' #progress1').html(e.loaded + "/" + e.total + " bytes. " + percent.toFixed(2) + "%");
                  }
              }
            }

        var t = null  //定时对象
        var task_gen = null  //task编号
        $.get("/get/task/gen", function (ret) {
                task_gen = ret.data
                var fileInput = $("#ads_materialurl")[0];
                if (fileInput && fileInput.files.length != 0) {
                    byteSize = fileInput.files[0].size;
                    //step-2  定时获取文件上传进度
                    t = setInterval(function () {
                        $.get("/get/task/process", {task_gen: task_gen}, function (ret) {
                                if (ret.code === TPE_OK) {
                                    $(domid + ' #process_data2').attr({value: ret.data, max: byteSize}); //更新数据到进度条
                                    var percent = ret.data / byteSize * 100;
                                    $(domid + ' #progress2').html(ret.data + "/" + byteSize + " bytes. " + percent.toFixed(2) + "%");
                                } else {
                                    ywl.notify_error('获取进度信息失败：' + ret.message);
                                }
                            }
                        );
                    }, 200);
                }

                //step-3  开始文件上传，提交表单
                // var ads_materialurl = $("#ads_materialurl")[0].files[0];        //获取上传文件名称
                var ads_materialurl = $("#ads_materialurl")[0].files[0];        //获取上传文件名称
                var ads_id = $("#ads_id").val()
                var form = new FormData();                  //创建表单对象

                form.append("file", ads_materialurl);                //向表单对象添加name和value,将上传文件名称添加到value
                form.append("task_gen", task_gen);                //向表单对象添加name和value,将上传文件名称添加到value
                form.append("ads_id", ads_id);                //向表单对象添加name和value,将上传文件名称添加到value
                $.ajax({                                    //jquery的ajax提交
                    type: 'POST',
                    url: '/adsinfo/vadd',
                    data: form,                             //提交数据为表单对象
                    processData: false,                     //默认为 true，数据被处理为 URL 编码格式。如果为 false，则阻止将传入的数据处理为 URL 编码的格式。
                    contentType: false,                     //指 定 请 求 内 容 的 类 型
                    success: function (ret) {
                        clearInterval(t);                       //删除定时请求
                        $(domid + " #btn-save").removeAttr("disabled");
                        if (ret.code === TPE_OK) {
                            host_table.reload();
                            ywl.notify_success('添加成功！');
                            $(domid + ' #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                            $(domid + ' #progress1').html("0 bytes");
                            $(domid + ' #process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                            $(domid + ' #progress2').html("0 bytes");
                            $("#dialog-adsinfovedio-info").modal("hide");
                        }
                        else {
                            ywl.notify_error('添加失败：' + ret.message);
                        }
                    },
                    error: function (xhr, errorText, errorStatus) {  //如果发生错误，返回错误信息
                        $(domid + " #btn-save").removeAttr("disabled");
                        $(domid + ' #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                        $(domid + ' #progress1').html("0 bytes");
                        $(domid + ' #process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                        $(domid + ' #progress2').html("0 bytes");
                        clearInterval(t);                       //删除定时请求
                        $(domid + ' #progress').html("0 bytes");
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

    $("#btn-add-host").click(function () {
         v_dlg.create_show();
    })


    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_adsinfo_info_dlg = function (tbl) {
    var adsinfo_info_dlg = {};
    adsinfo_info_dlg.dom_id = "#dialog-adsinfo-info";
    adsinfo_info_dlg.update = 1;
    adsinfo_info_dlg.tbl = tbl;
    adsinfo_info_dlg.ads_name = '';
    adsinfo_info_dlg.ads_contents = '';
    adsinfo_info_dlg.row_id = 0;

    adsinfo_info_dlg.update_show = function (ads_name,  ads_contents,ads_time,row_id) {
        adsinfo_info_dlg.update = 1;
        adsinfo_info_dlg.init(ads_name, ads_contents,ads_time,row_id);
        $('#dlg-notice').hide();
        $(adsinfo_info_dlg.dom_id).modal();
    };

    adsinfo_info_dlg.create_show = function () {
        adsinfo_info_dlg.update = 0;
        adsinfo_info_dlg.init('', '', '','', 0);
        $('#dlg-notice').show();
        $(adsinfo_info_dlg.dom_id).modal();
    };

    adsinfo_info_dlg.hide = function () {
        $(adsinfo_info_dlg.dom_id).modal('hide');
    };

    adsinfo_info_dlg.init = function (ads_name, ads_contents,ads_time,row_id) {
        adsinfo_info_dlg.ads_name = ads_name;
        adsinfo_info_dlg.ads_contents = ads_contents;
        adsinfo_info_dlg.ads_time = ads_time;
        adsinfo_info_dlg.row_id = row_id;
        adsinfo_info_dlg.init_dlg();
    };
    adsinfo_info_dlg.init_dlg = function () {

        $('#process_data1').attr({value: 0, max: 0}); //更新数据到进度条
        $('#progress1').html("0 bytes");
        $('#process_data2').attr({value: 0, max: 0}); //更新数据到进度条
        $('#progress2').html("0 bytes");

        $(adsinfo_info_dlg.dom_id + ' #ads_name').val(adsinfo_info_dlg.ads_name);
        $(adsinfo_info_dlg.dom_id + ' #ads_contents').val(adsinfo_info_dlg.ads_contents);
        $(adsinfo_info_dlg.dom_id + ' #ads_time').val(adsinfo_info_dlg.ads_time);

        var obj1 = document.getElementById('ads_materialurl');
        obj1.outerHTML=obj1.outerHTML
        var obj2 = document.getElementById('ads_thumbnailurl');
        obj2.outerHTML=obj2.outerHTML
        $("#preview").attr("src","");

    };

    adsinfo_info_dlg.check_args = function () {
        var ads_name=$(adsinfo_info_dlg.dom_id + ' #ads_name').val()
        var ads_contents=$(adsinfo_info_dlg.dom_id + ' #ads_contents').val()
        var ads_time=$(adsinfo_info_dlg.dom_id + ' #ads_time').val()
        if(!ads_name||ads_name==""){
            alert("名称不能为空")
            return
        }
        if(!ads_time||ads_time==""){
            alert("时间间隔不能为空")
            return
        }

        if(!ads_contents||ads_contents==""){
            alert("描述不能为空")
            return
        }
        adsinfo_info_dlg.ads_name = ads_name;
        adsinfo_info_dlg.ads_time = ads_time;
        adsinfo_info_dlg.ads_contents = ads_contents
        return true;
    };
    adsinfo_info_dlg.post = function () {
        function progressHandlingFunction(e) {
              var ads_materialurl=$("#ads_materialurl").val()
              if (ads_materialurl && ads_materialurl != "") {
                  if (e.lengthComputable) {
                      $('#process_data1').attr({value: e.loaded, max: e.total}); //更新数据到进度条
                      var percent = e.loaded / e.total * 100;
                      $('#progress1').html(e.loaded + "/" + e.total + " bytes. " + percent.toFixed(2) + "%");
                  }
              }
            }

        if (adsinfo_info_dlg.update === 1) {
            var t = null  //定时对象
            var task_gen = null  //task编号
            $.get("/get/task/gen", function (ret) {
                    task_gen = ret.data
                    var fileInput = $("#ads_materialurl")[0];
                    if (fileInput && fileInput.files.length != 0) {
                        byteSize = fileInput.files[0].size;
                        //step-2  定时获取文件上传进度
                        t = setInterval(function () {
                            $.get("/get/task/process", {task_gen: task_gen}, function (ret) {
                                    if (ret.code === TPE_OK) {
                                        $('#process_data2').attr({value: ret.data, max: byteSize}); //更新数据到进度条
                                        var percent = ret.data / byteSize * 100;
                                        $('#progress2').html(ret.data + "/" + byteSize + " bytes. " + percent.toFixed(2) + "%");
                                    } else {
                                        ywl.notify_error('获取进度信息失败：' + ret.message);
                                    }
                                }
                            );
                        }, 200);
                    }

                    //step-3  开始文件上传，提交表单
                    // var ads_materialurl = $("#ads_materialurl")[0].files[0];        //获取上传文件名称
                    var ads_thumbnailurl = $("#ads_thumbnailurl")[0].files[0];        //获取上传文件名称
                    var form = new FormData();                  //创建表单对象
                    var ads_name = $("#ads_name").val();
                    var ads_contents=$("#ads_contents").val();
                    var ads_time=$("#ads_time").val();

                    form.append("ads_contents", ads_contents);                    //向表单对象添加name和value
                    // form.append("file", ads_materialurl);
                    form.append("file_pic", ads_thumbnailurl);
                    form.append("task_gen", task_gen);
                    form.append("ads_name", ads_name);
                    form.append("ads_time", ads_time);
                    form.append("ads_id", adsinfo_info_dlg.row_id);
                    $.ajax({                                    //jquery的ajax提交
                        type: 'POST',
                        url: '/adsinfo/edit',
                        data: form,                             //提交数据为表单对象
                        processData: false,                     //默认为 true，数据被处理为 URL 编码格式。如果为 false，则阻止将传入的数据处理为 URL 编码的格式。
                        contentType: false,                     //指 定 请 求 内 容 的 类 型
                        success: function (ret) {
                            clearInterval(t);                       //删除定时请求
                            $(adsinfo_info_dlg.dom_id + " #btn-save").removeAttr("disabled");
                            if (ret.code === TPE_OK) {
                                adsinfo_info_dlg.tbl.reload();
                                ywl.notify_success('添加成功！');
                                $('#process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#progress1').html("0 bytes");
                                $('#process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#progress2').html("0 bytes");
                                adsinfo_info_dlg.hide();
                            }
                            else {
                                ywl.notify_error('添加失败：' + ret.message);
                            }
                        },
                        error: function (xhr, errorText, errorStatus) {  //如果发生错误，返回错误信息
                            $(adsinfo_info_dlg.dom_id + " #btn-save").removeAttr("disabled");
                            $('#process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#progress1').html("0 bytes");
                            $('#process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#progress2').html("0 bytes");
                            clearInterval(t);                       //删除定时请求
                            $('#progress').html("0 bytes");
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
        } else {

            var t = null  //定时对象
            var task_gen = null  //task编号
            $.get("/get/task/gen", function (ret) {
                    task_gen = ret.data
                    var fileInput = $("#ads_materialurl")[0];
                    if (fileInput && fileInput.files.length != 0) {
                        byteSize = fileInput.files[0].size;
                        //step-2  定时获取文件上传进度
                        t = setInterval(function () {
                            $.get("/get/task/process", {task_gen: task_gen}, function (ret) {
                                    if (ret.code === TPE_OK) {
                                        $('#process_data2').attr({value: ret.data, max: byteSize}); //更新数据到进度条
                                        var percent = ret.data / byteSize * 100;
                                        $('#progress2').html(ret.data + "/" + byteSize + " bytes. " + percent.toFixed(2) + "%");
                                    } else {
                                        ywl.notify_error('获取进度信息失败：' + ret.message);
                                    }
                                }
                            );
                        }, 200);
                    }

                    //step-3  开始文件上传，提交表单
                    // var ads_materialurl = $("#ads_materialurl")[0].files[0];        //获取上传文件名称
                    var ads_thumbnailurl = $("#ads_thumbnailurl")[0].files[0];        //获取上传文件名称
                    var form = new FormData();                  //创建表单对象
                    var ads_name = $("#ads_name").val()
                    var ads_contents=$("#ads_contents").val()
                    var ads_time=$("#ads_time").val()
                    var order_id=$("#order_id").val()

                    form.append("ads_contents", ads_contents);                    //向表单对象添加name和value
                    // form.append("file", ads_materialurl);
                    form.append("file_pic", ads_thumbnailurl);
                    form.append("task_gen", task_gen);
                    form.append("ads_name", ads_name);                //向表单对象添加name和value,将上传文件名称添加到value
                    form.append("ads_time", ads_time);                //向表单对象添加name和value,将上传文件名称添加到value
                    form.append("order_id", order_id);                //向表单对象添加name和value,将上传文件名称添加到value
                    $.ajax({                                    //jquery的ajax提交
                        type: 'POST',
                        url: '/adsinfo/add',
                        data: form,                             //提交数据为表单对象
                        processData: false,                     //默认为 true，数据被处理为 URL 编码格式。如果为 false，则阻止将传入的数据处理为 URL 编码的格式。
                        contentType: false,                     //指 定 请 求 内 容 的 类 型
                        success: function (ret) {
                            clearInterval(t);                       //删除定时请求
                            $(adsinfo_info_dlg.dom_id + " #btn-save").removeAttr("disabled");
                            if (ret.code === TPE_OK) {
                                adsinfo_info_dlg.tbl.reload();
                                ywl.notify_success('添加成功！');
                                $('#process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#progress1').html("0 bytes");
                                $('#process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                                $('#progress2').html("0 bytes");
                                adsinfo_info_dlg.hide();
                            }
                            else {
                                ywl.notify_error('添加失败：' + ret.message);
                            }
                        },
                        error: function (xhr, errorText, errorStatus) {  //如果发生错误，返回错误信息
                            $(adsinfo_info_dlg.dom_id + " #btn-save").removeAttr("disabled");
                            $('#process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#progress1').html("0 bytes");
                            $('#process_data2').attr({value: 0, max: 0}); //更新数据到进度条
                            $('#progress2').html("0 bytes");
                            clearInterval(t);                       //删除定时请求
                            $('#progress').html("0 bytes");
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
        }
        return true;
    };
    $(adsinfo_info_dlg.dom_id + " #btn-save").click(function () {
        if (!adsinfo_info_dlg.check_args()) {
            return;
        }
        adsinfo_info_dlg.post();
    });
    return adsinfo_info_dlg
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

            $(cell_obj).find('[ywl-btn-edit]').click(function () {
                v_dlg.update_show(row_data.ads_name,row_data.ads_contents,row_data.ads_time,row_data.ads_id)
            });
            $(cell_obj).find('[ywl-btn-vadd]').click(function () {
                $("#dialog-adsinfovedio-info"+" #ads_id").val(row_data.ads_id);
               $("#dialog-adsinfovedio-info").modal()
            });
        }
    };

    // 重载表格渲染器的部分渲染方式，加入本页面相关特殊操作f成功
    tbl.on_render_created = function (render) {

        var url='http://download.xiaohulu.com/obs/adsdownload/'

        render.make_check_box = function (row_id, fields) {
            return '<span><input type="checkbox" data-check-box="' + fields.id + '" id="host-select-' + row_id + '"></span>';
        };
        render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
        };

        render.make_action_btn = function (row_id, fields) {
            var ret = [];
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-edit="' + fields.ID + '">修改</a>&nbsp');
            ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-vadd="' + fields.ID + '">上传视频</a>&nbsp');
            return ret.join('');
        }


        render.moviedown = function (row_id, fields) {
            return fields.ads_materialurl?'<a href="'+url+fields.ads_id+'/'+fields.ads_materialurl+'" target="_blank">' +fields.ads_materialurl+ ' </a>':"<label style='color: #0eb320'>--</label>";
        };

        render.picturedown = function (row_id, fields) {
            return fields.ads_thumbnailurl?'<a href="'+url+fields.ads_id+'/'+fields.ads_thumbnailurl+'" target="_blank">' +fields.ads_thumbnailurl+ ' </a>':"<label style='color: #0eb320'>--</label>";
        };

    };
};


