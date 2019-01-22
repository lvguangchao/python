<%!
    page_title_ = '经纪公司主播'
    page_menu_ = ['anchor', 'anchor_agent']
    page_id_ = 'anchor_agent'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/anchor/anchor_agent_maped.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="anchor-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="export"><i class="glyphicon glyphicon-folder-open"></i> 导出</a>
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="">

                <div class="input-group input-group-sm" ywl-filter="agent_name" style="display:inline-block;">
                    <input id="agent_name" type="text" class="form-control" placeholder="经纪公司名称"
                           style="display:inline-block;"
                           maxlength="20">
                </div>
                <div class="input-group input-group-sm" ywl-filter="room_id" style="display:inline-block;">
                    <input id="room_id" type="text" class="form-control" placeholder="房间ID"
                           style="display:inline-block;"
                           maxlength="20">
                </div>
                <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
                    <input id="user_id" type="text" class="form-control" placeholder="用户ID"
                           style="display:inline-block;"
                           maxlength="20">
                </div>
                <div class="input-group input-group-sm" ywl-filter="anchor_name"
                     style="display:inline-block;vertical-align: top;">
                    <input type="text" id='anchor_name' class="form-control" placeholder="搜索 主播名称 " style="display:inline-block;">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button"
                                                                                                         class="btn btn-default"><i
                            class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="anchor-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-addagent-host" class="btn btn-sm btn-primary"><i
                        class="fa fa-plus-circle fa-fw"></i> 添加经纪公司</a>
                <a href="#" id="btn-addanchor-host" class="btn btn-sm btn-primary"><i
                        class="fa fa-plus-circle fa-fw"></i> 添加主播</a>
                <a href="#" id="btn-delete-host" class="btn btn-sm btn-primary"><i
                        class="glyphicon glyphicon-trash"></i> 删除</a>

            </div>


            <div class="" style="float:right;">
                <nav>
                    <ul class="pagination pagination-sm"></ul>
                </nav>
            </div>

            <div style="float:right;margin-right:30px;">
                <div class="breadcrumb-container">
                    <ol class="breadcrumb">
                        <li><i class="fa fa-list fa-fw"></i> 记录总数 <strong ywl-field="recorder_total">0</strong></li>
                        <li>页数 <strong><span ywl-field="page_current">1</span>/<span
                                ywl-field="page_total">1</span></strong></li>
                        <li>每页显示
                            <label>
                                <select></select>
                            </label>
                            条记录
                        </li>
                    </ol>
                </div>
            </div>

        </div>
        <!-- end page-nav -->
    </div>
</div>

<%block name="extend_content">
    <div class="modal fade" id="dialog-anchor-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">编辑信息</h3>
                </div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="needinfo-list-action">
                        <div class="form-horizontal">
                            <div id="agent_add">
                                <div class="form-group form-group-sm">
                                    <label for="agent_name"
                                           class="col-sm-3 control-label"><strong>经纪公司名称：</strong></label>
                                    <div class="col-sm-6">
                                        <select id="agent_id">
                                            <option value="">请选择</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="plat_id" class="col-sm-3 control-label"><strong>平台号：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="plat_id" type="number"
                                               oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="plat_id" class="col-sm-3 control-label"><strong>用户id：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="user_id" type="number"
                                               oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="room_id" class="col-sm-3 control-label"><strong>房间号：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="room_id" type="number"
                                               oninput="if(value.length>10)value=value.slice(0,10)"
                                               class="form-control"/>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="price" class="col-sm-3 control-label"><strong>价格：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="price" type="number"
                                               oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="rate" class="col-sm-3 control-label"><strong>经纪公司收入比例：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="rate" type="number"
                                               oninput="if(value.length>6)value=value.slice(0,6)" class="form-control" placeholder="单位为 %"/>
                                    </div>
                                </div>
                                <div class="form-group form-group-sm">
                                    <label for="comment" class="col-sm-3 control-label"><strong>主播昵称：</strong></label>
                                    <div class="col-sm-6">
                                        <input id="comment" type="text" class="form-control" maxlength="20"
                                               placeholder="主播昵称"/>
                                    </div>
                                </div>
                            </div>
                            <div id="dlg-notice">
                              <div class="form-group form-group-sm">
                                <label for="price" class="col-sm-3 control-label"><strong>价格：</strong></label>
                                <div class="col-sm-6">
                                    <input id="price2"  type="number" oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                </div>
                            </div>
                            </div>
                        </div>
                    </form>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i>
                        确定
                    </button>
                    <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                            class="fa fa-close fa-fw"></i> 取消
                    </button>
                </div>
            </div>
        </div>
    </div>

</%block>

<div class="modal fade" id="dialog-agent-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">添加经纪公司</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="needinfo-agent-action">
                    <div class="form-horizontal">

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="agent_name" class="col-sm-3 control-label"><strong>经纪公司名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="agent_name" type="text" class="form-control" maxlength="20"
                                           placeholder="经纪公司名称"/>
                                </div>
                            </div>

                    </div>
                </form>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i>
                    确定
                </button>
                <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                        class="fa fa-close fa-fw"></i> 取消
                </button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="dialog-incomerate-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">经纪公司的收入比例</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="needinfo-incomerate-action">
                    <input type="hidden" id="agent_user_map_id">
                    <div class="form-horizontal">
                        <div class="form-group form-group-sm" >
                            <label for="price" class="col-sm-3 control-label"><strong>比例：</strong></label>
                            <div class="col-sm-6">
                                <input id="income_rate"  type="number" oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                            </div>
                        </div>
                        <div id="dlg-notice">
                                <div class="form-group form-group-sm">
                                    <div class="col-sm-3"></div>
                                    <div class="col-sm-6">
                                        注意，比例单位为  <span class="mono h4">%</span> ！
                                    </div>
                                </div>
                            </div>
                    </div>
                </form>

            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i>
                    确定
                </button>
                <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                        class="fa fa-close fa-fw"></i> 取消
                </button>
            </div>
        </div>
    </div>
</div>









