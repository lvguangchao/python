<%!
    page_title_ = '广告计划查询'
    page_menu_ = ['plan', 'advertisingplaninfo']
    page_id_ = 'advertisingplaninfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/advertisting_plan_info/advertising_plan_list.js') }"></script>
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
    <div class="box" id="advertisingplanlist-list">
        <!-- begin filter -->
        <div class="page-filter" style="height: auto">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="input-group input-group-sm" ywl-filter="date" style="display:inline-block; vertical-align: top; margin-top: -1px;">
                <input class="form-control" placeholder="时间 "
                       id="date">
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">level</span>
                <div class="input-group-btn" ywl-filter="level" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>
            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">schedule_id</span>
                <div class="input-group-btn" ywl-filter="schedule_id" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">状态</span>
                <div class="input-group-btn" ywl-filter="plan_status" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>

            <div class="input-group input-group-sm" style="display:inline-block;">
                <button type="button" class="btn btn-sm btn-default" ywl-filter="select">
                    <i class="glyphicon glyphicon-search"></i> 查询
                </button>
            </div>


        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="advertisingplanlist-list"></table>
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
                <h3 class="modal-title">对应schedule_id信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <table class="table table-bordered table-hover">
                        <thead>
                        <tr>
                            <th>schedule_id</th>
                            <th>分组名称</th>
                            <th>投放量</th>
                            <th>公式</th>
                            <th>优先级</th>
                            <th>日志时间</th>


                        </tr>
                        </thead>
                        <tbody>
                        <td id="schedule_id"></td>
                        <td id="group_name"></td>
                        <td id="count"></td>
                        <td id="anchor_if_exp"></td>
                        <td id="lv_priority"></td>
                        <td id="logtime"></td>


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


<div class="modal fade" id="dialog-groupinfo-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">对应group_id信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <table class="table table-bordered table-hover">
                        <thead>
                        <tr>
                            <th>ads_need_group_id</th>
                            <th>分组名称</th>
                            <th>need_id</th>
                            <th>分组等级</th>
                            <th>描述</th>
                            <th>日志时间</th>

                        </tr>
                        </thead>
                        <tbody>
                        <td id="ads_need_group_id"></td>
                        <td id="group_name"></td>
                        <td id="need_id"></td>
                        <td id="anchor_level"></td>
                        <td id="comment"></td>
                        <td id="logtime"></td>


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
            elem: '#date',
##             value:GetDateStr(0),
            done: function (value, date, endDate) {
                $("#date").val(value);
            }
        });
    })

</script>