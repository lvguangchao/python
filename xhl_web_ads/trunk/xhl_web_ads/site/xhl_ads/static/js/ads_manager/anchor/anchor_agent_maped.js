var v_dlg=null

function initAgentSelect() {
    $('#agent_id').empty();
   $.get("/anchor/select4all", {}, function (ret) {
        var auxArr = [];
        $.each(ret, function (k, v) {
            auxArr.push("<option value='" + v["agent_id"] + "'>" + v["agent_name"] + "</option>");
        });
        $('#agent_id').append(auxArr.join(''));
    });
}


ywl.on_init = function (cb_stack, cb_args) {
    var dom_id = '#anchor-list';
    // var tbl_dom_id = '#ywl_host_list';
    //===================================
    // 创建页面控件对象
    //===================================
    var host_table_options = {
        selector: dom_id + " [toc-table='anchor-list']",
        data_source: {
            type: 'ajax-post',
            url: '/anchor/agent/maped'
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
            {title: "agent_user_map_id", key: "agent_user_map_id",width: 30},
            {title: "经纪公司名称", key: "agent_name",width: 30},
            {title: "平台", key: "plat_id",width: 50},
            {title: "房间号", key: "room_id",width: 10},
            {title: "用户ID", key: "user_id",width: 10},
            {title: "主播昵称", key: "comment",width: 10},
            {title: "结算价格", key: "price",width: 10},
            {title: "经纪公司收入比例", key: "rate",width: 10,render: 'format_rate',
                fields: {rate: 'rate'}},
            {title: "创建时间 ", key: "createtime",width: 10,render: 'format_time',
                fields: {logtime: 'createtime'}},
            {
                title: "操作",
                key: "action",
                width: 150,
                header_align: 'left', cell_align: 'left',
                render: 'make_action_btn',
                fields: {ID: 'id', protocol: 'id'}
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
    $("#btn-delete-host").click(function () {
        var vtype_list = [];
        var _objs = $(host_table.selector + " tbody tr td [data-check-box]");
        $.each(_objs, function (i, _obj) {
            if ($(_obj).is(':checked')) {
                var _row_data = host_table.get_row(_obj);
                vtype_list.push(_row_data.agent_user_map_id);
            }
        });

        if (vtype_list.length === 0) {
            ywl.notify_error('请选择要批量删除的需求！');
            return;
        }

        var _fn_sure = function (cb_stack, cb_args) {
            ywl.ajax_post_json_time_out('/anchor/agnet/delete', {ids: vtype_list}, 1000 * 30,
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
            msg: '<p>您确定要删除选定的需求吗？此操作不可恢复！！</p>',
            fn_yes: _fn_sure
        });
    });

    v_dlg = ywl.create_anchor_agent_maped_dlg(host_table);

    $("#btn-addanchor-host").click(function () {
        $("#needinfo-list-action")[0].reset()
         v_dlg.create_show();
    })

    $("#btn-addagent-host").click(function () {
        $("#needinfo-agent-action")[0].reset()
        $("#dialog-agent-info").modal()
    })

    $('#dialog-agent-info' + " #btn-save").click(function () {
        var agent_name = $("#dialog-agent-info #agent_name").val();
        if (!agent_name || agent_name == "") {
            alert("请输入经纪公司名称");
            return;
        }
        ywl.ajax_post_json('/anchor/agnet/name/add', {
                agent_name: agent_name
            },
            function (ret) {
                if (ret.code === TPE_OK) {
                    ywl.notify_success('新建经纪公司成功！');
                    $("#dialog-agent-info").modal('hide')
                } else {
                    ywl.notify_error('新建经纪公司失败：' + ret.message);
                }
            },
            function () {
                ywl.notify_error('网络故障，新建经纪公司失败！');
            }
        );
    });

  $('#dialog-incomerate-info' + " #btn-save").click(function () {
        var agent_user_map_id = $("#dialog-incomerate-info #agent_user_map_id").val();
        var rate = $("#dialog-incomerate-info #income_rate").val();
        if (!rate || rate == "") {
            alert("请输入经纪公司收入比例");
            return;
        }
        ywl.ajax_post_json('/anchor/agent/incomerate/edit', {
                agent_user_map_id: agent_user_map_id,
                rate: rate
            },
            function (ret) {
                if (ret.code === TPE_OK) {
                    ywl.notify_success('修改比例成功！');
                      host_table.reload();
                    $("#dialog-incomerate-info").modal('hide')
                } else {
                    ywl.notify_error('修改比例失败：' + ret.message);
                }
            },
            function () {
                ywl.notify_error('网络故障，修改比例失败！');
            }
        );
    });


    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='agent_name']",{},'agent_name');
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='room_id']",{},'room_id');
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='anchor_name']",{},'anchor_name');
    ywl.create_table_filter_search_box(host_table, dom_id + " [ywl-filter='user_id']",{},'user_id');

    cb_stack
        .add(host_table.load_data)
        .add(host_table.init)
        .exec();
};


 $("[ywl-filter='export']").click(function () {
        var agent_name = $("#agent_name").val();
        var room_id = $("#room_id").val();
        var anchor_name = $("#anchor_name").val();
        var user_id = $("#user_id").val();
        var isFirefox = /firefox/i.test(navigator.userAgent);
        $.post("/anchor/agent/maped/export?agent_name=" + agent_name+'&room_id='+
            room_id+'&anchor_name='+anchor_name+'&user_id='+user_id, function (result) {
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


ywl.create_anchor_agent_maped_dlg = function (tbl) {
    var anchor_agent_maped_dlg = {};
    anchor_agent_maped_dlg.dom_id = "#dialog-anchor-info";
    anchor_agent_maped_dlg.update = 1;
    anchor_agent_maped_dlg.tbl = tbl;
    anchor_agent_maped_dlg.agent_id = '';
    anchor_agent_maped_dlg.plat_id = '';
    anchor_agent_maped_dlg.room_id = ''
    anchor_agent_maped_dlg.user_id = ''
    anchor_agent_maped_dlg.price = ''
    anchor_agent_maped_dlg.rate = ''
    anchor_agent_maped_dlg.comment = comment
    anchor_agent_maped_dlg.agent_user_map_id = 0;

    anchor_agent_maped_dlg.update_show = function (agent_user_map_id, price) {
        anchor_agent_maped_dlg.update = 1;
        anchor_agent_maped_dlg.init(agent_user_map_id, price);
        $(anchor_agent_maped_dlg.dom_id+ ' #dlg-notice').show();
        $(anchor_agent_maped_dlg.dom_id+' #agent_add').hide();
        $(anchor_agent_maped_dlg.dom_id).modal();
    };

    anchor_agent_maped_dlg.create_show = function () {
        anchor_agent_maped_dlg.update = 0;
        anchor_agent_maped_dlg.init('','');
        $(anchor_agent_maped_dlg.dom_id+' #dlg-notice').hide();
        $(anchor_agent_maped_dlg.dom_id+' #agent_add').show();

        $(anchor_agent_maped_dlg.dom_id).modal();
    };

    anchor_agent_maped_dlg.hide = function () {
        $(anchor_agent_maped_dlg.dom_id).modal('hide');
    };

    anchor_agent_maped_dlg.init = function (agent_user_map_id, price) {
        anchor_agent_maped_dlg.agent_user_map_id = agent_user_map_id;
        anchor_agent_maped_dlg.price = price;
        anchor_agent_maped_dlg.init_dlg();
    };
    anchor_agent_maped_dlg.init_dlg = function () {
        if(anchor_agent_maped_dlg.update==0){
            initAgentSelect()
        }else if(anchor_agent_maped_dlg.update==1){
            $(anchor_agent_maped_dlg.dom_id + ' #price2').val(anchor_agent_maped_dlg.price)
        }

    };

    anchor_agent_maped_dlg.check_args = function () {
        if (anchor_agent_maped_dlg.update == 0) {
            var agent_id = $(anchor_agent_maped_dlg.dom_id + ' #agent_id').val()
            var plat_id = $(anchor_agent_maped_dlg.dom_id + ' #plat_id').val()
            var user_id = $(anchor_agent_maped_dlg.dom_id + ' #user_id').val()
            var room_id = $(anchor_agent_maped_dlg.dom_id + ' #room_id').val()
            var price = $(anchor_agent_maped_dlg.dom_id + ' #price').val()
            var comment = $(anchor_agent_maped_dlg.dom_id + ' #comment').val()
            var rate = $(anchor_agent_maped_dlg.dom_id + ' #rate').val()
            if (!agent_id || agent_id == "") {
                alert("请选择主播经纪公司");
                return;
            }
            if (!plat_id || plat_id == "") {
                alert("请输入平台号");
                return;
            }
            if (!user_id || user_id == "") {
                alert("请输入user_id");
                return;
            }
            if (!room_id || room_id == "") {
                alert("请输入房间号");
                return;
            }
            if (!price || price == "") {
                alert("请输入价格");
                return;
            }
            if (!comment || comment == "") {
                alert("请输入主播昵称");
                return;
            }  if (!rate || rate == "") {
                alert("请输入经纪公司收入比例");
                return;
            }
            anchor_agent_maped_dlg.agent_id = agent_id;
            anchor_agent_maped_dlg.plat_id = plat_id;
            anchor_agent_maped_dlg.room_id = room_id
            anchor_agent_maped_dlg.user_id = user_id
            anchor_agent_maped_dlg.price = price
            anchor_agent_maped_dlg.comment = comment
            anchor_agent_maped_dlg.rate = rate
        } else {
            var price2 = $(anchor_agent_maped_dlg.dom_id + ' #price2').val()
            anchor_agent_maped_dlg.price = price2

        }
        return true;
    };
    anchor_agent_maped_dlg.post = function () {
        if (anchor_agent_maped_dlg.update === 1) {
            ywl.ajax_post_json('/anchor/agnet/edit', {
                    agent_user_map_id: anchor_agent_maped_dlg.agent_user_map_id,
                    price: anchor_agent_maped_dlg.price
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        anchor_agent_maped_dlg.tbl.reload();
                        ywl.notify_success('更新成功！');
                        anchor_agent_maped_dlg.hide();
                    } else {
                        ywl.notify_error('更新失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，更新失败！');
                }
            );
        } else {
            ywl.ajax_post_json('/anchor/agnet/add', {
                    comment: anchor_agent_maped_dlg.comment,
                    agent_id: anchor_agent_maped_dlg.agent_id,
                    plat_id: anchor_agent_maped_dlg.plat_id,
                    user_id: anchor_agent_maped_dlg.user_id,
                    room_id: anchor_agent_maped_dlg.room_id,
                    price: anchor_agent_maped_dlg.price,
                    rate: anchor_agent_maped_dlg.rate
                },
                function (ret) {
                    if (ret.code === TPE_OK) {
                        anchor_agent_maped_dlg.tbl.reload();
                        ywl.notify_success('添加成功！');
                        anchor_agent_maped_dlg.hide();
                    }  else {
                        ywl.notify_error('添加失败：' + ret.message);
                    }
                },
                function () {
                    ywl.notify_error('网络故障，添加失败！');
                }
            );

        }
        return true;
    };
    $(anchor_agent_maped_dlg.dom_id + " #btn-save").click(function () {
        if (!anchor_agent_maped_dlg.check_args()) {
            return;
        }
        anchor_agent_maped_dlg.post();
    });
    return anchor_agent_maped_dlg
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
               v_dlg.update_show(row_data.agent_user_map_id, row_data.price)
            });
            $(cell_obj).find('[ywl-btn-incomerate]').click(function () {
                    var rate=row_data.rate?row_data.rate:0;
                    var agent_user_map_id=row_data.agent_user_map_id
                    $("#dialog-incomerate-info #agent_user_map_id").val(agent_user_map_id);
                    $("#dialog-incomerate-info #income_rate").val(rate);
                    $("#dialog-incomerate-info").modal();

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

                // if (fields.ret_code === 9999 && fields.cost_time > 0) {
                    ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-edit="' + fields.ID + '">修改价格</a>&nbsp');
                    ret.push('<a href="javascript:;" class="btn btn-sm btn-primary" protocol=' + fields.protocol + ' ywl-btn-incomerate="' + fields.ID + '">修改收入比例</a>&nbsp');
                // }


            return ret.join('');
        }
         render.format_time = function (row_id, fields) {
            return '<span class="badge badge-primary mono">' + fields.logtime.replace("T"," ") + ' </span>';
        };

         render.format_rate = function (row_id, fields) {
             var rate=fields.rate?fields.rate:0

            return '<span class="badge badge-danger mono">' +rate + '% </span>';
        };

        render.format_playtype = function (row_id, fields) {
            return fields.need_play_type==1?"大广告":fields.need_play_type==2?"角标播放":"";
        };
        render.format_alloc_type = function (row_id, fields) {

            return fields.need_alloc_type==1?"可以重复":fields.need_alloc_type==2?"不可重复":"";
        };

        render.format_ads = function (row_id, fields) {
            var temp=[]
            if(fields.ads_id){
                var arr=fields.ads_id.split(",");
                for(var i in arr){
                    temp.push('<a href="javascript:void(0)" onclick="show_adsInfo('+arr[i]+')">【'+arr[i]+'】</a>')
                }
            }
            return temp.join("  ");
        };

        render.format_enable = function (row_id, fields) {
            return fields.enable==1?"启用":fields.enable==0?"禁用":"";
        };
    };
};



