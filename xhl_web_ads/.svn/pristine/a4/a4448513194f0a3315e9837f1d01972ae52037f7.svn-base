var v_dlg=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#creditscore-detail';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='creditscore-detail']",
        data_source: {
            type: 'ajax-post',
            url: '/user/creditscore/detail'
        },
        column_default: {sort: false, header_align: 'center', cell_align: 'center'},
        columns: [
            {
                title: '<input type="checkbox" id="host-select-all" value="">',
                key: 'select_all',
                sort: false,
                width: 20,
                render: 'make_check_box',
                fields: {id: 'user_id'}
            },
            {title: "id", key: "id",width: 30},
            {title: "user_id", key: "user_id",width: 50},
            {title: "变动原因", key: "action",width: 50},
            {title: "触发时间", key: "trigger_time",width: 50,render: 'format_time',
                fields: {logtime: 'trigger_time'}},
            {title: "变动分值", key: "result",width: 50,render: 'format_result',
                fields: {result: 'result'}},
            {title: "变动后信用分", key: "cur_score",width: 50},
            {title: "变动时间", key: "create_time",width: 50,render: 'format_time',
                fields: {logtime: 'create_time'}}

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
    $(dom_id + " [ywl-filter='batch-edit']").click(function () {
        $("#creditscore-batch-action")[0].reset();
        $("#dialog-creditscore-batch-info").modal();
    });
    $("#dialog-creditscore-batch-info" + " #btn-save").click(function () {


        var summand = $("#dialog-creditscore-batch-info #summand").val();
        if(!summand){
            alert('请输入调整值');
            return
        }
        var action = $("#dialog-creditscore-batch-info #action").val();
        var user_ids = $("#dialog-creditscore-batch-info #user_ids").val();
        if (!user_ids) {
            alert('请输入需要修改的user_id');
            return
        }
        user_ids = user_ids.replace(/，/g, ",");

        var user_ids_arrary = user_ids.split(',');
        for (p in user_ids_arrary) {
            if (!isRealNum(user_ids_arrary[p])) {
                alert('user_id 内容不合法');
                return
            }
        }
        var data = {summand: summand, action: action, user_ids: user_ids};
        ywl.ajax_post_json('/user/creditscore/edit', data, function (ret) {
            if (ret.code == 0) {
                ywl.notify_success('调整成功！');
                $("#dialog-creditscore-batch-info").modal('hide');
            } else {
                alert('调整失败，失败user_id:' + ret.data);
            }
        }, function () {
            ywl.notify_error('网络故障，更新失败！');
        });

    });



    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='trigger_begintime']","","trigger_begintime");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='trigger_endtime']","","trigger_endtime");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='create_begintime']","","create_begintime");
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='create_endtime']","","create_endtime");

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

    v_dlg = ywl.create_creditscore_info_dlg(host_table);

    $("#dialog-adsinfovedio-info" + " #btn-save").click(function () {
       
    });

    $("#btn-add-host").click(function () {
         v_dlg.create_show();
    })


    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


ywl.create_creditscore_info_dlg = function (tbl) {
    var creditscore_info_dlg = {};
    creditscore_info_dlg.dom_id = "#dialog-creditscore-info";
    creditscore_info_dlg.update = 1;
    creditscore_info_dlg.tbl = tbl;
    creditscore_info_dlg.user_id = '';
    creditscore_info_dlg.action = '';
    creditscore_info_dlg.summand = '';

    creditscore_info_dlg.update_show = function (user_id) {
        creditscore_info_dlg.update = 1;
        creditscore_info_dlg.init(user_id);
        // $('#dlg-notice').hide();
        $(creditscore_info_dlg.dom_id).modal();
    };

    creditscore_info_dlg.create_show = function () {
        creditscore_info_dlg.update = 0;
        creditscore_info_dlg.init('', '', '','', 0);
        // $('#dlg-notice').show();
        $(creditscore_info_dlg.dom_id).modal();
    };

    creditscore_info_dlg.hide = function () {
        $(creditscore_info_dlg.dom_id).modal('hide');
    };

    creditscore_info_dlg.init = function (user_id) {
        creditscore_info_dlg.user_id = user_id;
        creditscore_info_dlg.init_dlg();
    };
    creditscore_info_dlg.init_dlg = function () {


    };

    creditscore_info_dlg.check_args = function () {
        var action=$(creditscore_info_dlg.dom_id + ' #action').val()
        var summand=$(creditscore_info_dlg.dom_id + ' #summand').val()
        if(!summand){
            alert("调整值不能为空")
            return
        }
        creditscore_info_dlg.action = action;
        creditscore_info_dlg.summand = summand;
        return true;
    };
    creditscore_info_dlg.post = function () {


        if (creditscore_info_dlg.update === 1) {
            ywl.ajax_post_json('/user/creditscore/edit',
                {
                    user_ids: [creditscore_info_dlg.user_id].join(","),
                    action: creditscore_info_dlg.action,
                    summand: creditscore_info_dlg.summand,

                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        creditscore_info_dlg.tbl.reload();
                        ywl.notify_success('更新成功！');
                        creditscore_info_dlg.hide();
                    } else {
                        ywl.notify_error('更新失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，更新失败！');
                }
            );



        } else {


        }
        return true;
    };
    $(creditscore_info_dlg.dom_id + " #btn-save").click(function () {
        if (!creditscore_info_dlg.check_args()) {
            return;
        }
        creditscore_info_dlg.post();
    });
    return creditscore_info_dlg
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
                v_dlg.update_show(row_data.user_id)
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
            if(fields.logtime&&fields.logtime!=""&&fields.logtime!=undefined){
                return '<span class="badge badge-primary mono">' + fields.logtime.replace("T", " ") + ' </span>';
            };

        };
        // render.make_action_btn = function (row_id, fields) {
        //     var ret = [];
        //     ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-detail="' + fields.ID + '">信用分记录</a>&nbsp');
        //     ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-edit="' + fields.ID + '">调整信用分</a>&nbsp');
        //     return ret.join('');
        // }


       render.format_result = function (row_id, fields) {
           var result=fields.result?fields.result:0;
           var temp=''
            if(result>0){
                temp='<span class="badge badge-danger mono">'+result+'</span>'
            }else if(result<0) {
                temp='<span class="badge badge-success mono">'+result+'</span>'
            }
            return temp

        };

    };
};

ywl.create_table_filter_search_box = function (tbl, selector, on_created,filter_name) {
	var _tblf_sb = {};
	// 此过滤器绑定的DOM对象，用于JQuery的选择器
	_tblf_sb.selector = selector;

	// 此过滤器绑定的表格控件
	_tblf_sb._table_ctrl = tbl;
	_tblf_sb._table_ctrl.append_filter_ctrl(_tblf_sb);

	// 过滤器内容
	_tblf_sb.filter_name = filter_name?filter_name:'search';
	_tblf_sb.filter_default = '';

	_tblf_sb.get_filter = function () {
		var _val = $(_tblf_sb.selector + " input").val();

		var _ret = {};
		_ret[_tblf_sb.filter_name] = _val;
		var user_id_select=$("#user_id_select").val();
		_ret['user_id_select'] = user_id_select;
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
			_tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {},'search');
		});
		// 绑定搜索输入框中按下回车键
		$(_tblf_sb.selector + " input").keydown(function (event) {
			if (event.which == 13) {
				_tblf_sb._table_ctrl.load_data(CALLBACK_STACK.create(), {},'search');
			}
		});

		if (_.isFunction(on_created)) {
			on_created(_tblf_sb);
		}

		cb_stack.exec();
	};

	return _tblf_sb;
};

