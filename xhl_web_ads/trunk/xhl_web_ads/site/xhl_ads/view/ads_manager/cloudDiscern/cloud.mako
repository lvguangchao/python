<%!
    page_title_ = '云识别查询'
    page_menu_ = ['plan', 'cloud']
    page_id_ = 'cloud'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/cloudDiscern/cloud.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="cloud-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>
            <div class="">
                <div class="input-group input-group-sm"
                     style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">审核结果</span>
                    <div class="input-group-btn" ywl-filter="verify_result"
                         style="display:inline-block;margin-left:-4px;">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                            <span>所有</span>
                            <span class="caret"></span></button>
                        <ul class="dropdown-menu">
                            <li>所有</li>
                        </ul>
                    </div>
                </div>
                <div class="input-group input-group-sm"
                     style="display:inline-block;margin-right:10px; vertical-align: top;">
                <span class="input-group-addon"
                      style="display:inline-block;width:auto; line-height:28px;height:30px;padding:0 10px;font-size:13px;">识别来源</span>
                    <div class="input-group-btn" ywl-filter="cloud_from"
                         style="display:inline-block;margin-left:-4px;">
                        <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
                            <span>所有</span>
                            <span class="caret"></span></button>
                        <ul class="dropdown-menu">
                            <li>所有</li>
                        </ul>
                    </div>
                </div>
                 <div class="input-group input-group-sm" ywl-filter="createtime" style="display:inline-block;">
                    <input id="createtime" type="text" class="form-control" placeholder="创建时间"
                           style="display:inline-block;"
                           maxlength="20">
                </div>
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;vertical-align: top;">
                    <input type="text" class="form-control" placeholder="搜索 play_id " style="display:inline-block;">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button"
                                                                                                         class="btn btn-default"><i
                            class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>

        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline" toc-table="cloud-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">

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
            elem: '#createtime',
            done: function (value, date, endDate) {
                $("#createtime").val(value);
            }
        });
    });

</script>










