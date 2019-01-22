<%!
    page_title_ = '对账查询'
    page_menu_ = ['financial', 'check']
    page_id_ = 'check'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/ads_manager/checkAccount/checkAccount.js') }"></script>
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
<div class="modal fade" id="dialog-checkdetail-info" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">异常账户信息列表</h3>
            </div>
            <div class="modal-body">
                <form enctype="multipart/form-data" id="version-list-action">
                    <table class="table table-bordered table-hover" id="checkdetail">
                        <thead>
                        <tr>
                            <th>detail_id</th>
                            <th>user_id</th>
                            <th>check_id</th>
                            <th>user_type</th>
                            <th>agent_id</th>
                            <th>union_id</th>
                            <th>balance</th>
                            <th>income</th>
                            <th>withdraw</th>
                        </tr>
                        </thead>
                        <tbody>
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
<%block name="extend_content2">
	<div class="modal fade" id="dialog-auto-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">对账进度信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm">
                                <label for="" class="col-sm-3 control-label"><strong>对账进度：</strong></label>
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

    $(document).ready(function () {
        laydate.render({
            elem: '#createtime',
            done: function (value, date, endDate) {
                $("#createtime").val(value);
            }
        });
    });

</script>










