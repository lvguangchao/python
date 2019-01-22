<%!
    page_title_ = '用户对应结算详情'
    page_menu_ = ['ads', 'needschedule']
    page_id_ = 'needschedule'
%>

## <%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <link rel="shortcut icon" href="${ static_url('favicon.ico') }">
    <link href="${ static_url('plugins/google-cache/open-sans.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/bootstrap/css/bootstrap.min.css') }" rel="stylesheet" type="text/css"/>
    <link href="${ static_url('plugins/font-awesome/css/font-awesome.min.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/gritter/css/jquery.gritter.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/select2/select2.min.css') }" rel="stylesheet">
    <link href="${ static_url('css/main.css') }" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="${ static_url('plugins/underscore/underscore.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/jquery/jquery.min.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/jquery/ajaxfileupload.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/bootstrap/js/bootstrap.min.js') }"></script>
    <!--[if lt IE 9]>
    <script src="${ static_url('plugins/html5shiv/html5shiv.min.js') }"></script>
    <![endif]-->
    <script type="text/javascript" src="${ static_url('js/json2.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/gritter/js/jquery.gritter.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc_const.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc_common.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/toc.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ui/common.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ui/controls.js') }"></script>
    ##     <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>

    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/select2/select2.min.js') }"></script>


    <script type="text/javascript"
            src="${ static_url('js/ads_manager/accountbalancelist/account_balance_select.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>

<div class="page-content">
    <div class="page-filter" style="margin-bottom: 30px;height: auto">
        <div id="user_div">

            <span class="badge badge-warning mono" id="user_id"> 结算ID:${id}</span>
            <span class="badge badge-danger mono"> 结算合计:${income_all}</span>
            <span class="badge badge-danger mono"> 结算类型:${user_name}</span>
            <span class="badge badge-danger mono" id="user_type" style="display: none">${user_type}</span>
        </div>

    </div>

    <div class="box" id="accountbase-list">
        <!-- end filter -->
        <!-- begin table -->
        <div class="" style="float:right;">
            <a href="javascript:;" class="btn btn-sm btn-primary" ywl-filter="update"><i
                    class="glyphicon glyphicon-folder-open"></i> 导出excel</a>
        </div>
        <table class="table table-striped table-bordered table-hover table-data no-footer dtr-inline"
               toc-table="account-list"></table>

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

<script type="text/javascript">
    ywl.add_page_options({
        ## 	有些参数由后台python脚本生成到模板中，无法直接生成到js文件中，所以必须通过这种方式传递参数到js脚本中。
        active_menu: ${self.attr.page_menu_},
        ##         platformList: ${platformList},
        ##         unionList: ${unionList}
    });
    $(document).ready(function () {
        ywl.init();
    });

</script>














