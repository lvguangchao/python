<%!
    page_title_ = '密码修改'
    page_menu_ = ['pwd_update']
    page_id_ = 'pwd_update'
%>
<%inherit file="../page_base.mako"/>

<%block name="extend_js">
    <script type="text/javascript" src="${ static_url('js/auth/login.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>

<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="box" id="user-list">
        <!-- begin filter -->
        <div class="page">

            <div class="tab-pane active">
                <form>
                    <div class="input-group input-group-sm">
                        <label>原始密码</label><input type="password" id="raw_pwd" class="form-control" maxlength="10"/></div>
                    <div class="input-group input-group-sm">
                        <label>新密码</label><input type="password" id="pwd_first" class="form-control" maxlength="10"/></div>
                    <div class="input-group input-group-sm">
                        <label>确认密码</label><input type="password" id="pwd_second" class="form-control" maxlength="10"/></div>
                    <div class="input-group input-group-sm">
                        <input class="btn btn-success" value="提交" type="button" onclick="uploadPwd()"/>
                        <input class="btn" value="重置" type="button" onclick="reset()"/></div>
                </form>
            </div>
        </div>
        <!-- end filter -->
    </div>
</div>

<script type="text/javascript">



</script>









