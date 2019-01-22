<%!
    page_title_ = '角色管理'
    page_menu_ = ['system', 'role']
    page_id_ = 'role'
%>
<%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <script type="text/javascript"
            src="${ static_url('js/sys_manager/role_info/role.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
    	<link rel="stylesheet" href="${ static_url('plugins/ztree3/css/zTreeStyle/zTreeStyle.css')}" type="text/css">
	<script type="text/javascript" src="${ static_url('plugins/ztree3/js/jquery.ztree.core.js')}"></script>
	<script type="text/javascript" src="${ static_url('plugins/ztree3/js/jquery.ztree.excheck.js')}"></script>
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="role-list">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
                <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="reload"><i
                        class="fa fa-repeat fa-fw"></i> 刷新</a>
            </div>

            <div class="">
                <div class="input-group input-group-sm" ywl-filter="search" style="display:inline-block;">
                    <input type="text" class="form-control" placeholder="搜索角色名称 " style="display:inline-block;"
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
               toc-table="role-list"></table>
        <!-- end table -->

        <!-- begin page-nav -->
        <div class="page-nav" ywl-paging="host-list">

            <div class="input-group input-group-sm" style="display:inline-block;">
                <a href="#" id="btn-add-host" class="btn btn-sm btn-primary"><i class="fa fa-plus-circle fa-fw"></i> 添加</a>
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
    <div class="modal fade" id="dialog-role-info" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">角色信息编辑</h3>
                </div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="contract_name"
                                       class="col-sm-3 control-label"><strong>角色名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="role_name" type="text" maxlength="20" class="form-control"
                                           />
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="role-div">
                                <label for="contract_name"
                                       class="col-sm-3 control-label"><strong>角色权限：</strong></label>
                                <div class="col-sm-6">
                                    <div class="zTreeDemoBackground left">
		                                <ul id="treeDemo" class="ztree"></ul>
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

</%block>
