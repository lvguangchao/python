<%!
    page_title_ = '素材管理'
    page_menu_ = ['ads', 'adsinfo']
    page_id_ = 'adsinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/ads_info/adsinfo.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="adsinfo-list">
        <input type="hidden" id="order_id" value="${order_id}">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="搜索 素材名称 " style="display:inline-block;" maxlength="20">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button" class="btn btn-default"><i class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="adsinfo-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
                <a href="#" id="btn-delete-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-trash"></i> 删除</a>
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
	<div class="modal fade" id="dialog-adsinfo-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">编辑素材信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_name" class="col-sm-3 control-label"><strong>素材名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_name" type="text" maxlength="20" class="form-control" placeholder="设置名称"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>广告视频时长：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_time"  type="number" oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"/>
                                </div>
                            </div>

##                             <div class="form-group form-group-sm">
##                                 <label for="ads_materialurl" class="col-sm-3 control-label"><strong>视频：</strong></label>
##                                 <div class="col-sm-6">
##                                     <input id="ads_materialurl" type="file" maxlength="32" class="form-control" placeholder="设置类型名称"/>
##                                 </div>
##                             </div>
                            <div class="form-group form-group-sm">
                                <label for="ads_thumbnailurl" class="col-sm-3 control-label"><strong>图片：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_thumbnailurl" type="file" maxlength="32" onchange="previewFile(this)" class="form-control" placeholder="设置类型名称"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_thumbnailurl"
                                       class="col-sm-3 control-label"><strong>预览区：</strong></label>
                                <div class="col-sm-6">
                                    <img src=""  style="color: red;" height="%50" width="50%" id="preview" alt="reading for image ..." />
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_contents" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="ads_contents" style="height: 160px;width: 290px" type="text" maxlength="250" class="form-control" placeholder="简介"></textarea>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>web上传进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data1"></progress>
                                    <br/>
                                    <p id="progress1">0 bytes</p>
                                    <p id="info1"></p></div>
                            </div>

                             <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>SSH上传进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data2"></progress>
                                    <br/>
                                    <p id="progress2">0 bytes</p>
                                    <p id="info2"></p></div>
                            </div>


                            <div id="dlg-notice">
##                                 <div class="form-group form-group-sm">
##                                     <div class="col-sm-3"></div>
##                                     <div class="col-sm-6">
##                                         注意，新建类型编号 <span class="mono h4">不可重复</span> ！
##                                     </div>
##                                 </div>
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
<%block name="extend_content2">
	<div class="modal fade" id="dialog-adsinfovedio-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">上传素材视频</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm">
                                <input type="hidden" id="ads_id">
                                <label for="ads_materialurl" class="col-sm-3 control-label"><strong>视频：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_materialurl" type="file" maxlength="32" class="form-control" placeholder="设置类型名称"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>web上传进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data1"></progress>
                                    <br/>
                                    <p id="progress1">0 bytes</p>
                                    <p id="info1"></p></div>
                            </div>

                             <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>SSH上传进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data2"></progress>
                                    <br/>
                                    <p id="progress2">0 bytes</p>
                                    <p id="info2"></p></div>
                            </div>


                            <div id="dlg-notice">
##                                 <div class="form-group form-group-sm">
##                                     <div class="col-sm-3"></div>
##                                     <div class="col-sm-6">
##                                         注意，新建类型编号 <span class="mono h4">不可重复</span> ！
##                                     </div>
##                                 </div>
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









