<%!
    page_title_ = '监播素材替换'
    page_menu_ = ['audit', 'source-edit']
    page_id_ = 'source-edit'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/playlog_screen/playlog_screen.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="adsinfo-list">
        <!-- begin filter -->
##         <div class="page-filter">
##             <div class="" style="float:right;">
##                 <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
##             </div>
##
##             <div class="">
##                 <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
##                     <input type="text" class="form-control" placeholder="搜索 素材名称 " style="display:inline-block;" maxlength="20">
##                     <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button" class="btn btn-default"><i class="fa fa-search fa-fw"></i></button></span>
##                 </div>
##
##             </div>
##         </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="adsinfo-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-batch-edit-host" class="btn btn-sm btn-primary"><i class="glyphicon glyphicon-pencil"></i> 批量替换新老监播内容</a>
                <a href="#" id="btn-edit-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-pencil"></i> 单个替换新老监播内容</a>
            </div>


            <div class="" style="float:right;">
                <nav>
                    <ul class="pagination pagination-sm"></ul>
                </nav>
            </div>

##             <div style="float:right;margin-right:30px;">
##                 <div class="breadcrumb-container">
##                     <ol class="breadcrumb">
##                         <li><i class="fa fa-list fa-fw"></i> 记录总数 <strong ywl-field="recorder_total">0</strong></li>
##                         <li>页数 <strong><span ywl-field="page_current">1</span>/<span ywl-field="page_total">1</span></strong></li>
##                         <li>每页显示
##                             <label>
##                                 <select></select>
##                             </label>
##                             条记录
##                         </li>
##                     </ol>
##                 </div>
##             </div>

        </div>
        <!-- end page-nav -->
    </div>
</div>

<%block name="extend_content">
	<div class="modal fade" id="dialog-screenbatch-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">监播信息替换</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="screen-batch-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="screen_type" class="col-sm-3 control-label"><strong>替换内容：</strong></label>
                                <div class="col-sm-6">
                                    <input name="screen_type" type="radio" value="1" />替换视频
                                    <input name="screen_type" type="radio" value="2" />替换截图
                                    <input name="screen_type" type="radio" value="3" />同时替换
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-4 control-label"><strong>输入替换play_Id用","隔开：</strong></label>
                                <div class="col-sm-5">
                                    <textarea id="play_ids"  style="height: 150px"  class="form-control"></textarea>
                                </div>
                            </div>

##
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

<div class="modal fade" id="dialog-screen-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">监播信息修改</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="screen-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="screen_type" class="col-sm-3 control-label"><strong>play_id：</strong></label>
                                <div class="col-sm-6">
                                    <input id="play_ids" type="number"/>
                                    <button id="play_log_search" type="button">查询</button>
                                </div>

                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="record_path" class="col-sm-3 control-label"><strong>监播视频：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="record_path"  style="height: 150px"  class="form-control"></textarea>
                                </div>
                            </div>
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="screen_path" class="col-sm-3 control-label"><strong>监播截图：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="screen_path"  style="height: 150px"  class="form-control"></textarea>
                                </div>
                            </div>

##
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











