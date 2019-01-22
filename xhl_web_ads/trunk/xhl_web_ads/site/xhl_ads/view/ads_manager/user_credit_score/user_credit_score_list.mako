<%!
    page_title_ = '主播信用分'
    page_menu_ = ['anchor', 'user_credit_score_list']
    page_id_ = 'user_credit_score_list'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/user_credit_score/user_credit_score.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="creditscore-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="batch-edit"><i class="fa fa-repeat fa-fw"></i> 批量调整</a>
            </div>

            <div class="">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block; vertical-align: top;">
                    <input type="text" class="form-control" placeholder="用户ID " style="display:inline-block;" maxlength="20">
                </div>
                <div class="input-group input-group-sm" ywl-filter="nick_name" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="直播间昵称 " style="display:inline-block;" maxlength="20">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button" class="btn btn-default"><i class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="creditscore-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
##                 <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
##                 <a href="#" id="btn-delete-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-trash"></i> 删除</a>
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
                        <li>页数 <strong><span ywl-field="page_current">1</span>/<span ywl-field="page_total">1</span></strong></li>
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
	<div class="modal fade" id="dialog-creditscore-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">主播信用分信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" >
                                <label for="action" class="col-sm-3 control-label"><strong>调整原因(用户可见)：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="action" type="text" maxlength="20" class="form-control" placeholder="调整原因"></textarea>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="summand" class="col-sm-3 control-label"><strong>调整值：</strong></label>
                                <div class="col-sm-6">
                                    <input id="summand"  type="number" oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                </div>
                            </div>
                            <div id="dlg-notice">
                                <div class="form-group form-group-sm">
                                    <div class="col-sm-3"></div>
                                    <div class="col-sm-6">
                                        注意,<span class="mono h4">调整值>0 为增加,调整值<0 为扣除 </span> ！
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
				</div>

				<div class="modal-footer">
					<button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i> 确定</button>
					<button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i class="fa fa-close fa-fw"></i> 取消</button>
				</div>
			</div>
		</div>
	</div>

</%block>


<div class="modal fade" id="dialog-creditscore-batch-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">主播信用分信息(批量)</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="creditscore-batch-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" >
                                <label for="action" class="col-sm-3 control-label"><strong>调整原因(用户可见)：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="action" type="text" maxlength="20" class="form-control" placeholder="调整原因"></textarea>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="summand" class="col-sm-3 control-label"><strong>调整值：</strong></label>
                                <div class="col-sm-6">
                                    <input id="summand"  type="number" oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>输入user_Id用","隔开：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="user_ids"  style="height: 150px"  class="form-control"></textarea>
                                </div>
                            </div>
                            <div id="dlg-notice">
                                <div class="form-group form-group-sm">
                                    <div class="col-sm-3"></div>
                                    <div class="col-sm-6">
                                        注意,<span class="mono h4">调整值>0 为增加,调整值<0 为扣除 </span> ！
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
				</div>

				<div class="modal-footer">
					<button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i> 确定</button>
					<button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i class="fa fa-close fa-fw"></i> 取消</button>
				</div>
			</div>
		</div>
	</div>






