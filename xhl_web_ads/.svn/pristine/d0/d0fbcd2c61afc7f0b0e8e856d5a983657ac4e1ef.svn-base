<%!
    page_title_ = 'need管理'
    page_menu_ = ['market', 'needinfo']
    page_id_ = 'needinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/needinfo/needinfo.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="needinfo-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="搜索 需求名称 " style="display:inline-block;">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button" class="btn btn-default"><i class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="needinfo-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
##                 <a href="#" id="btn-delete-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-trash"></i> 删除</a>
                <a href="#" id="btn-batchadd-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-plus"></i> 批量添加</a>
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
	<div class="modal fade" id="dialog-needinfo-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">编辑需求信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="needinfo-list-action">
                        <input type="hidden" id="vtype_list_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="need_name" class="col-sm-3 control-label"><strong>需求名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="need_name" type="text" class="form-control" placeholder="设置需求名称" maxlength="20"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>套餐：</strong></label>
                                <div class="col-sm-6">
                                    <select id="package_id">
                                        <option value="">请选择</option>
                                    </select>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>播放类型：</strong></label>
                                <div class="col-sm-6">
                                    <input name="need_play_type" type="radio" value="1" checked/>大广告
                                    <input name="need_play_type" type="radio" value="2" />角标播放
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告级别：</strong></label>
                                <div class="col-sm-6">
                                    <input name="anchor_level" type="radio" value="S" />S
                                    <input name="anchor_level" type="radio" value="A"  />A
                                    <input name="anchor_level" type="radio" value="B"  />B
                                    <input name="anchor_level" type="radio" value="C"  />C
                                    <input name="anchor_level" type="radio" value="D"  />D
                                </div>
                            </div>
                              <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【1】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id1">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="1">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position1" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【2】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id2">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="2">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position2" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【3】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id3">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="3">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position3" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【4】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id4">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="4">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position4" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【5】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id5">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="5">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position5" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【6】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id6">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="6">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position6" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【7】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id7">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="7">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position7" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【8】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id8">
                                                <option value="">请选择</option>
                                            </select>
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="8">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position8" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>

                             <div class="form-group form-group-sm">
                                <label for="enable" class="col-sm-3 control-label"><strong>是否启用：</strong></label>
                                <div class="col-sm-6">
                                    <input name="enable" type="radio" value="1" checked/>Yes
                                    <input name="enable" type="radio" value="0" />No
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_contents" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="description" style="height: 100px;width: 290px" type="text"
                                              maxlength="200" class="form-control" placeholder="需求描述"></textarea>
                                </div>
                            </div>
                            <div id="dlg-notice">
                                <div class="form-group form-group-sm">
                                    <div class="col-sm-3"></div>
                                    <div class="col-sm-6">
                                        注意，广告位复选框需勾选中 <span class="mono h4">下拉选择才有效</span> ！
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




<div class="modal fade" id="dialog-adsinfo-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">广告素材信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_name" class="col-sm-3 control-label"><strong>素材名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_name" type="text" maxlength="20" class="form-control" readonly/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>广告视频时长：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_time" type="number" type="number" readonly class="form-control"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_materialurl" class="col-sm-3 control-label"><strong>视频：</strong></label>
                                <div class="col-sm-6">
                                    <div class="input-group">
                                        <input  id="ads_materialurl" type="text" readonly class="form-control">
                                        <span class="input-group-btn"><button class="btn btn-default" url="" id="downMovieBt"
                                        onClick="downloadMovie(this)" target="_blank">下载</button></span>
                                    </div><!-- /input-group -->
                                </div><!-- /.col-lg-6 -->

                            </div>
                            <div class="form-group form-group-sm">
                                <label for="ads_thumbnailurl" class="col-sm-3 control-label"><strong>图片：</strong></label>
                                <div class="col-sm-6">
                                    <img id="ads_thumbnailurl" style="width: 50%;height: 50%;" class="form-control"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_contents" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="ads_contents" style="height: 100px;width: 290px" type="text" readonly class="form-control"></textarea>
                                </div>
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
					<button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i class="fa fa-close fa-fw"></i> 取消</button>
				</div>
			</div>
		</div>
	</div>





