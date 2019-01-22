<%!
    page_title_ = '提现'
    page_menu_ = ['financial', 'withdrawanchorlistinfo']
    page_id_ = 'withdrawanchorlistinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/withdrawanchor_info/withdrawanchorlist.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/bootstrap-multiselect.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
    <link href="${ static_url('css/bootstrap-multiselect.css') }" rel="stylesheet">


</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="withdrawanchorlist-list">
        <!-- begin filter -->
        <div class="page-filter" style="height: auto">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="update"><i
                        class="glyphicon glyphicon-folder-open"></i> 导出excel</a>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h6 type="text">开始时<br>间(创建):</h6>
            </div>
            <div class="input-group input-group-sm" ywl-filter="start_time" style="display:inline-block; width: 90px">
                <input class="form-control" style="display:inline-block;"
                       id="start_time">
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h6 type="text">结束<br>时间:</h6>
            </div>
            <div class="input-group input-group-sm" ywl-filter="end_time" style="display:inline-block; width: 90px">
                <input class="form-control" style="display:inline-block;"
                       id="end_time">
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h6 type="text">开始时<br>间(修改):</h6>
            </div>
            <div class="input-group input-group-sm" ywl-filter="start_time2" style="display:inline-block; width: 90px">
                <input class="form-control" style="display:inline-block;"
                       id="start_time2">
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h6 type="text">结束<br>时间:</h6>
            </div>
            <div class="input-group input-group-sm" ywl-filter="end_time2" style="display:inline-block; width: 90px">
                <input class="form-control" style="display:inline-block;"
                       id="end_time2">
            </div>
            <div class="input-group input-group-sm" ywl-filter="id" style="display:inline-block;">
                <input type="text" class="form-control" placeholder="提现ID " style="display:inline-block;"
                       maxlength="20" id="id">
            </div>

            <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
                <input type="text" class="form-control" placeholder="用户ID " style="display:inline-block;"
                       maxlength="20" id="user_id">
            </div>
            <div class="input-group input-group-sm" ywl-filter="phone" style="display:inline-block;">
                <input type="text" class="form-control" placeholder="手机号 " style="display:inline-block;"
                       maxlength="20" id="phone">
            </div>
            <div class="input-group input-group-sm" ywl-filter="bank_name" style="display:inline-block;">
                <input type="text" class="form-control" placeholder="银行名称" style="display:inline-block;"
                       maxlength="20" id="bank_name">
            </div>

            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">状态</span>
                <div class="input-group-btn" ywl-filter="income_from" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>

            <div class="input-group input-group-sm" style="display:inline-block; vertical-align: top;">
                <button type="button" class="btn btn-sm btn-default" ywl-filter="select">
                    <i class="glyphicon glyphicon-search"></i> 查询
                </button>
            </div>


            <div class="input-group input-group-sm" style="display:inline-block; vertical-align: top;">
                <button type="button" class="btn btn-sm btn-default" onclick="excelImportAds_show()" id="btn01">
                    <i class="glyphicon glyphicon-import"></i> 导入
                </button>
            </div>


        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="withdrawanchorlist-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-host-15" class="btn btn-sm btn-warning"><i class="fa fa-plus-circle fa-fw"></i>
                    设置为已审核</a>
                <a href="#" id="btn-host-11" class="btn btn-sm btn-danger"><i class="fa fa-plus-circle fa-fw"></i>
                    设置为审核未通过</a>
                <a href="#" id="btn-host-20" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i>
                    设置为已提交财务</a>
                <a href="#" id="btn-host-30" class="btn btn-sm btn-danger"><i class="fa fa-plus-circle fa-fw"></i>
                    设置为打款异常</a>
                <a href="#" id="btn-host-35" class="btn btn-sm btn-info"><i class="fa fa-plus-circle fa-fw"></i>
                    设置为打款异常已处理</a>
                <a href="#" id="btn-host-40" class="btn btn-sm btn-success"><i
                        class="fa fa-plus-circle fa-fw"></i>
                    设置为已完成</a>
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


<div class="modal fade" id="dialog-withdrawanchorinfo-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">批量导入修改状态</h3>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-left: 50px;">
                <button class="btn btn-sm btn-default" style="line-height: 0.1;">
                    上传excel表格： <input type="file" name="infile" id="files_ads"
                                      style="display: inline-block "><br><br>

                </button>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-left: 50px; margin-top: 5px">
                <label>导入状态选择:</label>
                <select id="add_withdrawanchor_select" name="add_withdrawanchor_select" style="display:inline-block;">
                    <option value="10">未处理</option>
                    <option value="11">审核未通过</option>
                    <option value="15">已审核</option>
                    <option value="20">已提交财务</option>
                    <option value="30">打款异常</option>
                    <option value="35">打款异常已处理</option>
                    <option value="40">已完成</option>
                </select>

            </div>

            <div class="input-group input-group-sm" style="display:inline-block;">

                <button type="button" class="btn btn-sm btn-default" onclick="excelRemindAds()" id="btn01">
                    <i class="glyphicon glyphicon-import"></i> 导入
                </button>

            </div>

            <div class="col-sm-6">

                ##                                     <option value=""></option>
                                </div>
            <div class="modal-footer">
                ## 					<button type="button" class="btn btn-sm btn-primary" id="btn-save"><i class="fa fa-check fa-fw"></i> 确定</button>

                <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                        class="fa fa-close fa-fw"></i> 取消
                </button>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="dialog-withdrawanchorimport-remind" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">现在导入的状态提醒</h2>
            </div>
            <div class="col-sm-6">
                <h4>总数量为:</h4><a style="color: red" id="remind_num"></a>
                <h4>总价值为:</h4><a style="color: red" id="remind_money"></a>
                <h4>将要变更的状态为:</h4><a style="color: red" id="remind_state"></a>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-sm btn-primary" id="btn-save" onclick="excelImportAds()">确认导入
                </button>
                <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                        class="fa fa-close fa-fw"></i> 取消
                </button>
            </div>
        </div>
    </div>
</div>


<div class="modal fade" id="dialog-withdrawanchoredit-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">修改备注信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="needschedule-list-action">
                    <input type="hidden" id="vtype_list_id">
                    <div class="form-horizontal">
                        <div id="group">
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>备注内容：</strong></label>
                                <div class="col-sm-6">
                                    <input class="form-control" id="commit_data" placeholder="备注内容" type="text"
                                           min="0">
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


<div class="modal fade" id="demo" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">编辑类型信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <input type="hidden" id="ptype_id">
                    <div class="form-horizontal">
                        <div class="form-group form-group-sm" id="vtype-div">
                            <label for="contract_name"
                                   class="col-sm-3 control-label"><strong>姓名：</strong></label>
                            <div class="col-sm-6">
                                <input id="id_user_name" type="text" maxlength="20" class="form-control"
                                       placeholder="设置姓名"/>
                            </div>
                        </div>

                        <div class="form-group form-group-sm">
                            <label for="contract_price"
                                   class="col-sm-3 control-label"><strong>身份证号：</strong></label>
                            <div class="col-sm-6">
                                <input id="id_number" type="text"
                                       class="form-control"
                                       placeholder="身份证号"/>
                            </div>
                        </div>
                        <div class="form-group form-group-sm">
                            <label for="adsver_id"
                                   class="col-sm-3 control-label"><strong>银行名称：</strong></label>
                            <div class="col-sm-6">
                                <input id="bank_name2" type="text"
                                       class="form-control"
                                       placeholder="银行名称"/>
                            </div>
                        </div>
                        <div class="form-group form-group-sm">
                            <label for="contract_desc"
                                   class="col-sm-3 control-label"><strong>银行卡号：</strong></label>
                            <div class="col-sm-6">
                                <input id="bank_card_number" type="number" class="form-control"
                                       placeholder="银行卡号"/>
                            </div>
                        </div>
                        <div class="form-group form-group-sm">
                            <label for="contract_desc"
                                   class="col-sm-3 control-label"><strong>持卡人姓名：</strong></label>
                            <div class="col-sm-6">
                                <input id="hold_user_name" type="text" class="form-control"
                                       placeholder="持卡人姓名"/>
                            </div>
                        </div>
                        <div class="form-group form-group-sm">
                            <label for="contract_desc"
                                   class="col-sm-3 control-label"><strong>开户所在支行：</strong></label>
                            <div class="col-sm-6">
                                <input id="bank_sub_name" type="text" class="form-control"
                                       placeholder="开户所在支行"/>
                            </div>
                        </div>
                        <div class="form-group form-group-sm">
                            <label for="contract_desc"
                                   class="col-sm-3 control-label"><strong>QQ号：</strong></label>
                            <div class="col-sm-6">
                                <input id="qq_number" type="number" class="form-control"
                                       placeholder="QQ号"/>
                            </div>
                        </div>

                        <div id="dlg-notice">

                        </div>
                    </div>
                </form>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-sm btn-primary" id="btn-save3"><i class="fa fa-check fa-fw"></i>
                    确定
                </button>
                <button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i
                        class="fa fa-close fa-fw"></i> 取消
                </button>
            </div>
        </div>
    </div>
</div>




<script type="text/javascript">
    $(document).ready(function () {
        laydate.render({
            elem: '#start_time',
            ##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#start_time").val(value);
            }
        });
    });
    $(document).ready(function () {
        laydate.render({
            elem: '#end_time',
            ##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#end_time").val(value);
            }
        });
    });
    $(document).ready(function () {
        laydate.render({
            elem: '#start_time2',
            ##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#start_time2").val(value);
            }
        });
    });
    $(document).ready(function () {
        laydate.render({
            elem: '#end_time2',
            ##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#end_time2").val(value);
            }
        });
    })

</script>