<%!
    page_title_ = '套餐管理'
    page_menu_ = ['ads', 'contractpackageinfo']
    page_id_ = 'contractpackageinfo'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/contractionfopackage_info/contractionpackageinfo.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">


</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="contractpackageinfo-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="搜索套餐名称 " style="display:inline-block;"
                           maxlength="20">
                    <span class="input-group-btn" style="display:inline-block;margin-left:-4px;"><button type="button"
                                                                                                         class="btn btn-default"><i
                            class="fa fa-search fa-fw"></i></button></span>
                </div>

            </div>
        </div>
        <!-- end filter -->

        <!-- begin table -->
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="contractpackageinfo-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
                <a href="#" id="btn-delete-host" class="btn btn-sm btn-success"><i class="fa fa-plus-circle fa-fw"></i>
                    删除</a>
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

<%block name="extend_content">
    <div class="modal fade" id="dialog-contractpackageinfo-info" tabindex="-1" role="dialog">
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
                                       class="col-sm-3 control-label"><strong>套餐名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="package_name" type="text" maxlength="20" class="form-control"
                                           placeholder="设置名称"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="contract_price"
                                       class="col-sm-3 control-label"><strong>合同ID：</strong></label>
                                <div class="col-sm-6">
                                    <input id="contract_id" type="number"
                                           oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"
                                           placeholder="设置合同ID"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="adsver_id"
                                       class="col-sm-3 control-label"><strong>套餐价格：</strong></label>
                                <div class="col-sm-6">
                                    <input id="package_price" type="number"
                                           oninput="if(value.length>6)value=value.slice(0,6)" class="form-control"
                                           placeholder="设置套餐价格"/>
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
                                       class="col-sm-3 control-label"><strong>主播人数：</strong></label>
                                <div class="col-sm-6">
                                    <input id="anchor_need" type="text" maxlength="32" class="form-control"
                                           placeholder="主播人数"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>主播播放次数：</strong></label>
                                <div class="col-sm-6">
                                    <input id="anchor_play_count" type="text" maxlength="32" class="form-control"
                                           placeholder="主播播放次数"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>财务编码：</strong></label>
                                <div class="col-sm-6">
                                    <input id="affairs_num" type="text" maxlength="32" class="form-control"
                                           placeholder="财务编码"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>S级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="S" type="text" maxlength="32" class="form-control"
                                           placeholder="S级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>A级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="A" type="text" maxlength="32" class="form-control"
                                           placeholder="A级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>B级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="B" type="text" maxlength="32" class="form-control"
                                           placeholder="B级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>C级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="C" type="text" maxlength="32" class="form-control"
                                           placeholder="C级别"/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="contract_desc"
                                       class="col-sm-3 control-label"><strong>D级别:</strong></label>
                                <div class="col-sm-6">
                                    <input id="D" type="text" maxlength="32" class="form-control"
                                           placeholder="D级别"/>
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

</%block>
<script type="text/javascript">

    $(document).ready(function () {

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

    });

</script>

