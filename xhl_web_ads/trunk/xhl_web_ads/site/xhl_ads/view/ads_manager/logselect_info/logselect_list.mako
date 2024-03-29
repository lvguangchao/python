<%!
    page_title_ = '日志审计'
    page_menu_ = ['audit', 'logselectinfo']
    page_id_ = 'logselectinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/logselect_plan_info/logselect_plan_list.js') }"></script>
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
    <div class="box" id="logselectplanlist-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h4 type="text" >开始时间:</h4>
            </div>
            <div class="input-group input-group-sm" ywl-filter="start_time" style="display:inline-block;">
                <input  class="form-control" style="display:inline-block;"
                       id="start_time">
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h4 type="text" >结束时间:</h4>
            </div>
            <div class="input-group input-group-sm" ywl-filter="end_time" style="display:inline-block;">
                <input  class="form-control" style="display:inline-block;"
                       id="end_time">
            </div>

            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">log类型</span>
                <div class="input-group-btn" ywl-filter="level" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">

                    </ul>
                </div>
            </div>

            <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
                <input type="text" class="form-control" placeholder="搜索用户名称" style="display:inline-block;"
                       maxlength="20">

            </div>


            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <button type="button" class="btn btn-sm btn-default" ywl-filter="select">
                    <i class="glyphicon glyphicon-search"></i> 查询
                </button>
            </div>


        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="logselectplanlist-list"></table>
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



<div class="modal fade" id="dialog-scheduleinfo-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">对应描述信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <table class="table table-bordered table-hover">
                        <thead>
                        <tr>
                            <th id="name1"></th>
                            <th id="name2"></th>

                        </tr>
                        </thead>
                        <tbody>
                        <td id="user_id"></td>
                        <td id="user_type"></td>


                        </tbody>
                    </table>
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
    })

</script>