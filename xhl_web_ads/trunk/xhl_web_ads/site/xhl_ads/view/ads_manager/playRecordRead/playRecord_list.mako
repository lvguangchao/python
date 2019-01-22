<%!
    page_title_ = '播放记录'
    page_menu_ = ['plan', 'playrecordread']
    page_id_ = 'playrecord'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
     <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ads_manager/playRecordRead/playRecord.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="playrecord-list">
        <input type="hidden" value="${type}" id="show_type">
        <input type="hidden" value="${date}" id="show_date">
        <!-- begin filter -->
        <div class="page-filter" style="height: auto">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="export"><i class="glyphicon glyphicon-folder-open"></i> 导出</a>
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

             <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">播放状态</span>
                <div class="input-group-btn" ywl-filter="status" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">审核状态</span>
                <div class="input-group-btn" ywl-filter="verify_status" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">审核结果</span>
                <div class="input-group-btn" ywl-filter="verify_result" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">结算状态</span>
                <div class="input-group-btn" ywl-filter="is_account" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">套餐</span>
                <div class="input-group-btn" ywl-filter="package_type" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" ywl-filter="room_id" style="display:inline-block;">
                <input type="text" class="form-control" id="room_id" placeholder="房间id " style="display:inline-block;"
                       maxlength="20">
            </div>
            <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
                <input type="text" class="form-control" id="user_id" placeholder="用户id " style="display:inline-block;"
                       maxlength="20">
            </div>
            <div class="input-group input-group-sm" ywl-filter="play_id" style="display:inline-block;">
                <input type="text" class="form-control" id="play_id" placeholder="play_id " style="display:inline-block;"
                       maxlength="20">
            </div>
            <div class="input-group input-group-sm" ywl-filter="begintime" style="display:inline-block;">
                <input id="begin_time" type="text" class="form-control" placeholder="任务创建时间 "
                       style="display:inline-block;"
                       maxlength="20">
            </div>
    ##             <div class="input-group input-group-sm" ywl-filter="endtime" style="display:inline-block;">
    ##                 <input id="end_time" type="text" class="form-control" placeholder="结束时间" style="display:inline-block;"
    ##                        maxlength="20">
    ##             </div>

          <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <button type="button" class="btn btn-sm btn-default"  ywl-filter="select" style="margin-top: 6px;">
                    <i class="glyphicon glyphicon-search"></i> 查询
                </button>
            </div>



        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="playrecord-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

##             <div class="input-group input-group-sm" style="display:inline-block;">
##                 <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
##                 <a href="#" id="btn-delete-host" class="btn btn-sm btn-success"><i class="glyphicon glyphicon-trash"></i> 删除</a>
##             </div>


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
    <div class="modal fade" id="dialog-playdetail-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content"  style="width: 650px">
                <div class="modal-header">
                    <h3 class="modal-title">截图地址信息</h3>
                </div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">

                            <div class="form-group form-group-sm" id="vtype-div">
                                <div class="col-sm-12" id="shot_path">

                                </div>
                            </div>

                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                            class="fa fa-close fa-fw"></i> 取消
                    </button>
                </div>
            </div>
        </div>
    </div>

</%block>


<%block name="extend_content2">
	<div class="modal fade" id="dialog-playrecord-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">补贴主播金额</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>结算金额：</strong></label>
                                <div class="col-sm-6">
                                    <input id="income"  min="0" type="number" oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"/>
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

<%block name="extend_content3">
	<div class="modal fade" id="dialog-import-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">excel 导入</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                       <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>请选择excel文件：</strong></label>
                                <div class="col-sm-6">
                                    <input type="file" id="excel_file" class="form-control"/>
                                </div>
                            </div>

                        <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>excel导入进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data1"></progress>
                                    <br/>
                                    <p id="progress1">0 bytes</p>
                                    <p id="info1"></p></div>
                        </div>
                        <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>excel处理进度：</strong></label>
                                <div class="col-sm-6">
                                    <progress value="0" max="0" id="process_data2"></progress>
                                    <br/>
                                    <p id="progress2">0/0</p>
                                    <p id="info2"></p></div>
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

<%block name="extend_content4">
	<div class="modal fade" id="dialog-verify-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">审核播放记录</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="play_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>审核结果：</strong></label>
                                <div class="col-sm-6">
                                    <select id="verify_result">
                                        <option value="0">成功</option>
                                        <option value="1">失败</option>
                                    </select>
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

<%block name="extend_content5">
	<div class="modal fade" id="dialog-needinfo-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">need_info信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="needschedule-list-action">
                        <input type="hidden" id="vtype_list_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="group_name" class="col-sm-3 control-label"><strong>需求名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="need_name" type="text" class="form-control" readonly url="sss"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>套餐名称：</strong></label>
                                <div class="col-sm-6">
                                <input id="package_name" type="text" class="form-control" readonly/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="anchor_alloc_type" class="col-sm-3 control-label"><strong>播放类型：</strong></label>
                                <div class="col-sm-6">
                                    <input id="need_play_type" class="form-control" value="1" readonly/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="enable" class="col-sm-3 control-label"><strong>是否启用：</strong></label>
                                <div class="col-sm-6">
                                    <input name="enable" type="radio" value="1" disabled/>Yes
                                    <input name="enable" type="radio" value="0" disabled/>No
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="comment" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="comment" style="height: 100px;width: 290px" type="text"
                                              maxlength="200" class="form-control" readonly></textarea>
                                </div>
                            </div>
                            <div id="dlg-notice">
##                                 <div class="form-group form-group-sm">
##                                     <div class="col-sm-3"></div>
##                                     <div class="col-sm-6">
##                                         注意，广告位复选框需勾选中 <span class="mono h4">下拉选择才有效</span> ！
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

</%block>

<%block name="extend_content6">
	<div class="modal fade" id="playlog-export-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">播放记录excle导出</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="play_id">
                        <div class="form-horizontal">
                             <div class="form-group form-group-sm">
                               <label for="" class="col-sm-3 control-label"><strong>excel生成进度：</strong></label>
                               <div class="col-sm-6">
                                   <progress value="0" max="0" id="process_data1"></progress>
                                   <br/>
                                   <p id="progress1">0/0</p>
                                   <p id="info1"></p></div>
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

</%block>

<script type="text/javascript">

     ywl.add_page_options({
        ## 	有些参数由后台python脚本生成到模板中，无法直接生成到js文件中，所以必须通过这种方式传递参数到js脚本中。
        packageList: ${package_list}
    });



    $(document).ready(function () {
        laydate.render({
            elem: '#begin_time',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#begin_time").val(value);
            }
        });
    })

</script>



