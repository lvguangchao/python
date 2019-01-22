var v_dlg=null
ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#cloud-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='cloud-list']",
        data_source: {
            type: 'ajax-post',
            url: '/cloud/list'
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
            {title: "play_id", key: "play_id",width: 30},
            {title: "口播词", key: "expect_words",width: 30},
            {title: "云识别口播词", key: "actual_words",width: 50},
            {title: "匹配率", key: "match_ratio",width: 10,render: 'format_ratio',
                fields: {match_ratio: 'match_ratio'}},
            {title: "来源", key: "from",width: 10,render: 'format_from',
                fields: {from: 'from'}},
            {title: "审核状态", key: "verify_status",width: 50,render: "formatvs",
                fields: {verify_status:"verify_status"}},
            {title: "审核结果", key: "verify_result",width: 50,render: "formatvr",
                fields: {verify_result:"verify_result"}},
            {
                title: "日志时间", key: "log_time", width: 180, render: 'format_time',
                fields: {logtime: 'log_time'}
            }
            // ,{
            //     title: "操作",
            //     key: "action",
            //     width: 50,
            //     header_align: 'left', cell_align: 'left',
            //     render: 'make_action_btn',
            //     fields: {ID: 'id', protocol: 'id'}
            // }

        ],
        paging: {selector: dom_id, per_page: paging_normal},

        // 可用的属性设置
        have_header: true,

        // 可用的回调函数
        on_created: ywl.on_host_table_created,
        on_header_created: ywl.on_host_table_header_created


    };

    // $("#createtime").val(getDate())

    var host_table = ywl.create_table(host_table_options);

    $(dom_id + " [ywl-filter='reload']").click(host_table.reload);

    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='search']","",'search');
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='createtime']",'','createtime');
    ywl.create_table_filter_verifyr_list(host_table, dom_id + " [ywl-filter='verify_result']");
    ywl.create_table_filter_verifyf_list(host_table, dom_id + " [ywl-filter='cloud_from']");

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
            $(cell_obj).find('[ywl-btn-edit]').click(function () {

                $.get("/needinfo/get?id="+row_data.need_id, function (ret) {
                   v_dlg.update_show(ret.package_id, ret.need_play_type ,
                       ret.anchor_level,ret.position, ret.ads_id,ret.need_name,ret.enable,ret.description,ret.need_id)
                } );
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
            return ret.join('');
        }
         render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T"," ") + ' </span>';
        };

        // render.format_words = function (row_id, fields) {
        //         if
        //     return fields.need_alloc_type==1?"可以重复":fields.need_alloc_type==2?"不可重复":"";
        // };

        render.format_ratio = function (row_id, fields) {
           return fields.match_ratio?fields.match_ratio.toFixed(0)+"%":0
        };

        render.format_from = function (row_id, fields) {
             var temp=''
             if(fields.from==1){
                 temp="<span class='badge badge-success warning'>客户端</span>"
             }else if(fields.from==2){
                temp="<span class='badge badge-success mono'>服务端</span>"
             }
            return temp
        };
        render.formatvs = function (row_id, fields) {
             var temp='未知'
            if(fields.verify_status==0){
                temp='<span class="badge badge-danger mono">未审核</span>'
            }else if(fields.verify_status==1){
                temp='<span class="badge badge-success mono">已审核</span>'
            }
            return '<label style="color: red">'+temp+'</label>'
         };
         render.formatvr = function (row_id, fields) {
             var temp='未知'
            if(fields.verify_result==0){
                temp='<span class="badge badge-success mono">成功</span>'
            }else if(fields.verify_result==-1){
                temp='<span class="badge badge-warning mono">初始状态</span>'
            }else {
                temp='<span class="badge badge-danger mono">失败</span>'
            }
            return '<label style="color: red">'+temp+'</label>'
         };
    };
};



ywl.create_table_filter_verifyr_list = function (tbl, selector, on_created) {
	var _tblf_st = {};

	// 此表格绑定的DOM对象的ID，用于JQuery的选择器
	_tblf_st.selector = selector;
	// 此过滤器绑定的表格控件
	_tblf_st._table_ctrl = tbl;
	_tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

	// 过滤器内容
	_tblf_st.filter_name = 'verify_result';
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
		node += '<li><a href="javascript:;" ywl-verifyr-from="">全部</a></li>';
		node += '<li role="separator" class="divider"></li>';
        node+='<li><a href="javascript:;" ywl-verifyr-from="' + -1+ '"> 初始状态 </a></li>'
		node+='<li><a href="javascript:;" ywl-verifyr-from="' + 0+ '"> 成功 </a></li>'
		node+='<li><a href="javascript:;" ywl-verifyr-from="' + 1+ '"> 失败 </a></li>'
		_tblf_st.filter_value = _tblf_st.filter_default;
		$(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
		$(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('全部');
		// 点击事件绑定
		$(_tblf_st.selector + ' ul [ywl-verifyr-from]').click(_tblf_st._on_select);

		if (_.isFunction(on_created)) {
			on_created(_tblf_st);
		}

		cb_stack.exec();
	};

	_tblf_st._on_select = function () {
		var verifyr = $(this).attr("ywl-verifyr-from");
		var verifyr_html = $(this).html();
        play_verify_result=verifyr
		var cb_stack = CALLBACK_STACK.create();
		cb_stack
			.add(function (cb_stack) {
				_tblf_st.filter_value = verifyr;
				$(_tblf_st.selector + ' button span:first').html(verifyr_html);
				cb_stack.exec();
			});
		cb_stack.exec();
	};

	return _tblf_st;
};
ywl.create_table_filter_verifyf_list = function (tbl, selector, on_created) {
	var _tblf_st = {};

	// 此表格绑定的DOM对象的ID，用于JQuery的选择器
	_tblf_st.selector = selector;
	// 此过滤器绑定的表格控件
	_tblf_st._table_ctrl = tbl;
	_tblf_st._table_ctrl.append_filter_ctrl(_tblf_st);

	// 过滤器内容
	_tblf_st.filter_name = 'cloud_from';
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
		node += '<li><a href="javascript:;" ywl-verifyr-from="">全部</a></li>';
		node += '<li role="separator" class="divider"></li>';
		node+='<li><a href="javascript:;" ywl-verifyr-from="' + 1+ '"> 客户端 </a></li>'
		node+='<li><a href="javascript:;" ywl-verifyr-from="' + 2+ '"> 服务器 </a></li>'
		_tblf_st.filter_value = _tblf_st.filter_default;
		$(_tblf_st.selector + ' button span:first').html(_tblf_st.filter_value);
		$(_tblf_st.selector + ' ul').empty().append($(node));
        $(_tblf_st.selector + ' button span:first').html('全部');
		// 点击事件绑定
		$(_tblf_st.selector + ' ul [ywl-verifyr-from]').click(_tblf_st._on_select);

		if (_.isFunction(on_created)) {
			on_created(_tblf_st);
		}

		cb_stack.exec();
	};

	_tblf_st._on_select = function () {
		var verifyr = $(this).attr("ywl-verifyr-from");
		var verifyr_html = $(this).html();
        play_verify_result=verifyr
		var cb_stack = CALLBACK_STACK.create();
		cb_stack
			.add(function (cb_stack) {
				_tblf_st.filter_value = verifyr;
				$(_tblf_st.selector + ' button span:first').html(verifyr_html);
				cb_stack.exec();
			});
		cb_stack.exec();
	};

	return _tblf_st;
};
