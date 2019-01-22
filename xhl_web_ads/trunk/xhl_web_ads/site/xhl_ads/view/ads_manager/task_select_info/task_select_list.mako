<%!
    page_title_ = '任务查询'
    page_menu_ = ['plan', 'taskselectlistinfo']
    page_id_ = 'taskselectlistinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/task_select_info/task_select_list.js') }"></script>
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
    <div class="box" id="taskselectlist-list">
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

            <div class="input-group input-group-sm" ywl-filter="date"
                 style="display:inline-block; vertical-align: top; margin-top: -1px;">
                <input class="form-control" placeholder="时间 "
                       id="date" value="">
            </div>

            <div class="input-group input-group-sm" ywl-filter="user_id" style="display:inline-block;">
                <input type="text" class="form-control" id="user_id" placeholder="搜索用户ID" style="display:inline-block;"
                       maxlength="20">

            </div>
            <div class="input-group input-group-sm" ywl-filter="task_id" style="display:inline-block;">
                <input type="text" class="form-control" id="task_id" placeholder="搜索任务ID" style="display:inline-block;"
                       maxlength="20">

            </div>

            ##             <div class="input-group input-group-sm"
            ##                  style="display:inline-block;margin-right:10px; vertical-align: top;">
            ##                 <span class="input-group-addon"
            ##                       style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">平台</span>
            ##                 <div class="input-group-btn" ywl-filter="platform_id" style="display:inline-block;margin-left:-4px;">
            ##                     <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
            ##                         <span class="caret"></span></button>
            ##                     <ul class="dropdown-menu" id="income_from">
            ##                         <li>所有</li>
            ##                     </ul>
            ##                 </div>
            ##             </div>

            <div class="input-group input-group-sm" ywl-filter="room_id" style="display:inline-block;">
                <input type="text" class="form-control" id="room_id" placeholder="搜索房间ID" style="display:inline-block;"
                       maxlength="20">

            </div>


            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
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
            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
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

            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">套餐</span>
                <div class="input-group-btn" ywl-filter="package_id" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>

            <div class="input-group input-group-sm"
                 style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">任务状态</span>
                <div class="input-group-btn" ywl-filter="task_result" style="display:inline-block;margin-left:-4px;">
                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
                        <span class="caret"></span></button>
                    <ul class="dropdown-menu" id="income_from">
                        <li>所有</li>
                    </ul>
                </div>
            </div>

            ##             <div class="input-group input-group-sm"
            ##                  style="display:inline-block;margin-right:10px; vertical-align: top;">
            ##                 <span class="input-group-addon"
            ##                       style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">任务结果</span>
            ##                 <div class="input-group-btn" ywl-filter="task_result" style="display:inline-block;margin-left:-4px;">
            ##                     <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><span>所有</span>
            ##                         <span class="caret"></span></button>
            ##                     <ul class="dropdown-menu" id="income_from">
            ##                         <li>所有</li>
            ##                     </ul>
            ##                 </div>
            ##             </div>

            <div class="input-group input-group-sm" style="display:inline-block;vertical-align: top;">
                <button type="button" class="btn btn-sm btn-default" ywl-filter="select">
                    <i class="glyphicon glyphicon-search"></i> 查询
                </button>
            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="taskselectlist-list"></table>
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
                        <tr>
                            <td id="schedule_id"></td>
                            <td id="group_name"></td>
                            <td id="count"></td>
                            <td id="anchor_if_exp"></td>
                            <td id="lv_priority"></td>
                            <td id="logtime"></td>
                        </tr>
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


<div class="modal fade" id="dialog-taskplayloginfo-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">对应task_play_log信息</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <table class="table table-bordered table-hover" id="taskplayloginfo">
                        <thead>
                        <tr>
                            <th>播放ID</th>
                            <th>用户ID</th>
                            <th>播放状态</th>
                            <th>主播人气</th>
                            <th>直播截图</th>
                            <th>直播视频</th>
                            <th>审核状态</th>
                            <th>播放结果</th>
                            <th>收入</th>
                            <th>创建时间</th>
                        </tr>
                        </thead>
                        <tbody>
                            ##                         <tr>
##                             <td id="play_id"></td>
##                             <td id="user_id"></td>
##                             <td id="status"></td>
##                             <td id="popularity"></td>
##                             <td id="screen_shot_path"></td>
##                             <td id="verify_status"></td>
##                             <td id="verify_result"></td>
##                             <td id="log_create_time"></td>
##                         </tr>
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