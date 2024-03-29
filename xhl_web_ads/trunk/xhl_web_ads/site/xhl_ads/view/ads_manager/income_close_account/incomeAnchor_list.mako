<%!
    page_title_ = '结算详情(关账前)'
    page_menu_ = ['financial', 'needschedule']
    page_id_ = 'needschedule'
%>

## <%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <link rel="shortcut icon" href="${ static_url('favicon.ico') }">
    <link href="${ static_url('plugins/google-cache/open-sans.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/bootstrap/css/bootstrap.min.css') }" rel="stylesheet" type="text/css"/>
    <link href="${ static_url('plugins/font-awesome/css/font-awesome.min.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/gritter/css/jquery.gritter.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/select2/select2.min.css') }" rel="stylesheet">
    <link href="${ static_url('css/main.css') }" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="${ static_url('plugins/underscore/underscore.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/jquery/jquery.min.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/jquery/ajaxfileupload.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/bootstrap/js/bootstrap.min.js') }"></script>
    <!--[if lt IE 9]>
    <script src="${ static_url('plugins/html5shiv/html5shiv.min.js') }"></script>
    <![endif]-->
    <script type="text/javascript" src="${ static_url('js/json2.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/gritter/js/jquery.gritter.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc_const.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc_common.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ui/common.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ui/controls.js') }"></script>
    ##     <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>

    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/select2/select2.min.js') }"></script>


    <script type="text/javascript" src="${ static_url('js/ads_manager/income_close_account/income_anchor_close.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">


    <input type="hidden" value='${package_id}' id="package_id">
    <input type="hidden" value='${package_name}' id="package_name">
    <input type="hidden" value='${income_type}' id="income_type">
    <input type="hidden" value='${total}' id="total">
    <input type="hidden" value='${account_type}' id="account_type">

    <!-- begin filter -->
    <div class="page-filter" style="margin-bottom: 30px;height: auto">
        <div id="time_div">
            <span class="badge badge-warning mono"> 结算类型:<label id="income_name"></label></span>
            <span class="badge badge-danger mono">

                    套餐:${package_name}  总金额:${total}  当前总金额:<label id="total_income"></label>
                </span>
        </div>

        <div class="" style="float:right;">
            <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                    class="fa fa-repeat fa-fw"></i> 刷新</a>
            <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="export"><i
                    class="glyphicon glyphicon-folder-open"></i> 导出excel</a>
        </div>

        <div id="unionselect" class="input-group input-group-sm"
             style="display:inline-block;margin-right:10px;vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">公会</span>
            <select class="js-example-basic-single" name="state" style="vertical-align: top;">
            </select>
        </div>


        <div class="input-group input-group-sm" ywl-filter="income_log_id" style="display:inline-block;">
            <input type="text" class="form-control" id="income_log_id" placeholder="结算id " style="display:inline-block;"
                   maxlength="20">
        </div>
        <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
            <input type="text" class="form-control" id="user_id" placeholder="用户id " style="display:inline-block;"
                   maxlength="20">
        </div>
        <div class="input-group input-group-sm" ywl-filter="task_id" style="display:inline-block;">
            <input type="text" class="form-control" id="task_id" placeholder="任务id " style="display:inline-block;"
                   maxlength="20">
        </div>
        <div class="input-group input-group-sm" ywl-filter="room_id" style="display:inline-block;">
            <input type="text" class="form-control" id="room_id" placeholder="房间id " style="display:inline-block;"
                   maxlength="20">
        </div>
        <div class="input-group input-group-sm" ywl-filter="begintime" style="display:inline-block;">
            <input id="begin_time" type="text" class="form-control" placeholder="开始时间 " style="display:inline-block;"
                   maxlength="20">
        </div>
        <div class="input-group input-group-sm" ywl-filter="endtime" style="display:inline-block;">
            <input id="end_time" type="text" class="form-control" placeholder="结束时间" style="display:inline-block;"
                   maxlength="20">
        </div>

        <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">结算逻辑</span>
            <div class="input-group-btn" ywl-filter="income_from" style="display:inline-block;margin-left:-4px;">
                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                    <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li>所有</li>
                </ul>
            </div>
        </div>

        <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px;vertical-align: top;"
             id="plat_select">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">平台</span>
            <div class="input-group-btn" ywl-filter="plat_id" style="display:inline-block;margin-left:-4px;">
                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                    <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li>所有</li>
                </ul>
            </div>
        </div>


        <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
            <button type="button" class="btn btn-sm btn-default" ywl-filter="select" style="margin-top: 6px;">
                <i class="glyphicon glyphicon-search"></i> 查询
            </button>
        </div>

    </div>

    <div class="box" id="incomeanchor-list">
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="incomeanchor-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">
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
    <div class="modal fade" id="dialog-room-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">编辑类型信息</h3>
                </div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="roominfo-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="contract_name"
                                       class="col-sm-3 control-label"><strong>主播名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="anchor_name" type="text" class="form-control"
                                           readonly/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_materialurl"
                                       class="col-sm-3 control-label"><strong>房间地址：</strong></label>
                                <div class="col-sm-6">
                                    <div class="input-group">
                                        <input id="room_url" type="text" readonly class="form-control">
                                        <span class="input-group-btn"><a class="btn btn-default" href="" id="roomurlBt"
                                                                         target="_blank">转到</a></span>
                                    </div><!-- /input-group -->
                                </div><!-- /.col-lg-6 -->

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

<%block name="extend_contents">
    <div class="modal fade" id="dialog-playdetail-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
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

<script type="text/javascript">
    ywl.add_page_options({
        ## 	有些参数由后台python脚本生成到模板中，无法直接生成到js文件中，所以必须通过这种方式传递参数到js脚本中。
        active_menu: ${self.attr.page_menu_},
        platformList: ${platformList},
        unionList: ${unionList}
    });
    $(document).ready(function () {

        laydate.render({
            elem: '#begin_time',
            done: function (value, date, endDate) {
                $("#begin_time").val(value);
            }
        });
        laydate.render({
            elem: '#end_time',
            done: function (value, date, endDate) {
                $("#end_time").val(value);
            }
        });

        var income_type = $("#income_type").val()
        ywl.init();

        if (income_type == 1 || income_type == 4 || income_type == 3) {
            $("#unionselect").hide()
        } else {
            $("#unionselect").show()
        }
        if (income_type == 3) {
            $("#plat_select").hide()
        } else {
            $("#plat_select").show()
        }

        var income_name = ''
        if (income_type == 1) {
            income_name = "个人结算"
        } else if (income_type == 2) {
            income_name = "公会结算"
        } else if (income_type == 3) {
            income_name = "经纪人结算"
        } else if (income_type == 4) {
            income_name = "平台结算"
        }
        $("#income_name").text(income_name);
    });

</script>








