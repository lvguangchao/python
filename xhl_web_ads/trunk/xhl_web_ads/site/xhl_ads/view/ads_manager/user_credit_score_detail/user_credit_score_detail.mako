<%!
    page_title_ = '主播信用分详情'
    page_menu_ = ['anchor', 'user_credit_score_detail']
    page_id_ = 'user_credit_score_detail'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/user_credit_score_detail/user_credit_score_detail.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="creditscore-detail">
        <input type="hidden" value="${user_id_select}" id="user_id_select">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="fa fa-repeat fa-fw"></i> 刷新</a>
##                 <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="batch-edit"><i class="fa fa-repeat fa-fw"></i> 批量调整</a>
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h5 type="text" >触发时间:</h5>
            </div>
            <div class="input-group input-group-sm" ywl-filter="trigger_begintime" style="display:inline-block;">
                <input id="trigger_begin_time" type="text" class="form-control" placeholder="开始时间 "
                       style="display:inline-block;"
                       maxlength="20">
            </div>
            <div class="input-group input-group-sm" ywl-filter="trigger_endtime" style="display:inline-block;">
                <input id="trigger_end_time" type="text" class="form-control" placeholder="结束时间 "
                       style="display:inline-block;"
                       maxlength="20">
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <h5 type="text" >变动时间:</h5>
            </div>
            <div class="input-group input-group-sm" ywl-filter="create_begintime" style="display:inline-block;">
                <input id="create_begin_time" type="text" class="form-control" placeholder="开始时间 "
                       style="display:inline-block;"
                       maxlength="20">
            </div>
            <div class="input-group input-group-sm" ywl-filter="create_endtime" style="display:inline-block;">
                <input id="create_end_time" type="text" class="form-control" placeholder="结束时间 "
                       style="display:inline-block;"
                       maxlength="20">
            </div>
            <div  class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="搜索 用户ID " style="display:inline-block;" maxlength="20">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button" class="btn btn-default"><i class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="creditscore-detail"></table>
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
<script type="text/javascript">
    $(document).ready(function () {
        laydate.render({
            elem: '#trigger_begin_time',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#trigger_begin_time").val(value);
            }
        });
        laydate.render({
            elem: '#trigger_end_time',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#trigger_end_time").val(value);
            }
        });
        laydate.render({
            elem: '#create_begin_time',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#create_begin_time").val(value);
            }
        });
        laydate.render({
            elem: '#create_end_time',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#create_end_time").val(value);
            }
        });
    })

</script>

