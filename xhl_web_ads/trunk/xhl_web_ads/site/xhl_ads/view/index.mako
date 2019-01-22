<%!
    page_title_ = '广告计划日历'
    page_menu_ = ['ads_cal']
    page_id_ = 'ads_cal'
%>
<%inherit file="page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/ads_caldar/ads_caldar.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">

    <link href="${ static_url('plugins/fullcalendar/fullcalendar.min.css') }" rel='stylesheet' />
##     <link href="${ static_url('plugins/fullcalendar/jquery-ui.structure.css') }" rel='stylesheet' />
<link href="${ static_url('plugins/fullcalendar/fullcalendar.print.min.css') }" rel='stylesheet' media='print' />
<script src="${ static_url('plugins/fullcalendar/lib/moment.min.js') }"></script>
<script src="${ static_url('plugins/fullcalendar/fullcalendar.min.js') }"></script>
<script src="${ static_url('plugins/fullcalendar/locale/zh-cn.js') }"></script>


</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="adsinfo-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="add_cal_schedule"><i class="fa fa-plus-circle fa-fw"></i> 下单</a>
            </div>
##
            <div class="" style="display: flex;flex-wrap: wrap;align-content: space-between;">
                <div style="width: 80px;height: 20px;background-color: rgba(128, 128, 128, 0.79);margin-top: 7px;"></div><span style="font-weight: bold;
    font-family: cursive;"> &nbsp;--已执行--&nbsp;&nbsp; </span>
                 <div style="width: 80px;height: 20px;background-color: rgba(255, 0, 0, 0.66);margin-top: 7px;"></div><span style="font-weight: bold;
    font-family: cursive;">&nbsp;--今日--&nbsp;&nbsp; </span>
                <div style="width: 80px;height: 20px;background-color: green;margin-top: 7px;"></div><span style="font-weight: bold;
    font-family: cursive;"> &nbsp;--未执行 </span>
            </div>
        </div>
        <!-- end filter -->
        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="adsinfo-list">
            <div id="calendar"></div>
        </table>
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


    <div class="modal fade" id="dialog-adscal-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">套餐信息</h3>
                </div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="adscal-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="contract_name"
                                       class="col-sm-3 control-label"><strong>广告名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="package_name" type="text" maxlength="20" class="form-control"
                                           placeholder="设置名称"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_price"
                                       class="col-sm-3 control-label"><strong>广告主：</strong></label>
                                <div class="col-sm-6">
                                    <input id="adser" type="text"
                                           class="form-control"
                                           placeholder="广告主"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>开始时间：</strong></label>
                                <div class="col-sm-6">
                                    <input class="form-control" id="begin_time"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>结束时间：</strong></label>
                                <div class="col-sm-6">
                                    <input class="form-control" id="end_time"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>广告播放次数：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group" aria-label="...">
                                        <label>次</label>
                                        <div class="btn-group">
                                            <input type="checkbox" name="play" value="1">
                                        </div>
                                        <div class="btn-group">
                                            <label>视频:</label>
                                            <input type="number" id="play_num1" value="1" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong></strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group" aria-label="...">
                                        <label>次</label>
                                        <div class="btn-group">
                                            <input type="checkbox" name="play" value="2">
                                        </div>
                                        <div class="btn-group">
                                            <label>角标:</label>
                                            <input type="number" id="play_num2" value="1" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>投放方式：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group" aria-label="...">
                                        <label>天</label>
                                        <div class="btn-group">
                                            &nbsp;<label>分&nbsp;&nbsp;配:</label>
                                            <input type="number" id="serving_meth"  value="1" style="width:50px;" min="1">
                                        </div>
                                    </div>

                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>S级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="S" min="0" type="number"
                                           oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"
                                           placeholder="S级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>A级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="A" min="0" type="number"
                                           oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"
                                           placeholder="A级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>B级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="B" min="0" type="number"
                                           oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"
                                           placeholder="B级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>C级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="C" min="0" type="number"
                                           oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"
                                           placeholder="C级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>D级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="D" min="0" type="number"
                                           oninput="if(value.length>10)value=value.slice(0,10)" class="form-control"
                                           placeholder="D级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>是否可以重复接单:</strong></label>
                                <div class="col-sm-6">
                                    <input name="is_allow_repeat" type="radio" value="1" checked/>Yes
                                    <input name="is_allow_repeat" type="radio" value="0"/>No
                                </div>
                            </div>
                            ##                             <div class="form-group form-group-sm">
                            ##                                 <label for="contract_desc"
                            ##                                        class="col-sm-3 control-label"><strong>备注:</strong></label>
                            ##                                 <div class="col-sm-6">
                            ##                                     <textarea id="need_desc" type="text" maxlength="100" class="form-control"
                            ##                                               placeholder="备注"></textarea>
                            ##                                 </div>
                            ##                             </div>

                            <div id="dlg-notice">
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


<script>

  $(document).ready(function() {
       laydate.render({
            elem: '#begin_time',
            type: "datetime",
            done: function (value, date, endDate) {
                $("#begin_time").val(value);
            }
        });
        laydate.render({
            elem: '#end_time',
            type: "datetime",
            done: function (value, date, endDate) {
                $("#end_time").val(value);
            }
        });
      cal_init()

  });

</script>









