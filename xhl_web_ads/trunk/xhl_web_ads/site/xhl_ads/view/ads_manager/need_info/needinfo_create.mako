<%!
    page_title_ = 'needinfo添加'
    page_menu_ = ['ads', 'needinfo']
    page_id_ = 'needinfo'
%>

## <%inherit file="../../page_base.mako"/>
<%block name="extend_js">
    <link rel="shortcut icon" href="${ static_url('favicon.ico') }">
    <link href="${ static_url('plugins/google-cache/open-sans.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/bootstrap/css/bootstrap.min.css') }" rel="stylesheet" type="text/css"/>
    <link href="${ static_url('plugins/font-awesome/css/font-awesome.min.css') }" rel="stylesheet">
    <link href="${ static_url('plugins/gritter/css/jquery.gritter.css') }" rel="stylesheet">
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
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/ads_manager/needinfo/needinfoAdd.js') }"></script>
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
</%block>
<%block name="breadcrumb">
    <ol class="breadcrumb">
        <li><i class="fa fa-server fa-fw"></i> ${self.attr.page_title_}</li>
    </ol>
</%block>
<style>
    input{
            border:1px solid #a5b6c8;background:#eef3f7
    }

    select {
        border:1px solid #a5b6c8;background:#eef3f7
    }
    .disabledClass{
        border:1px solid #96c2f1;background:#eff7ff

    }
    tr th{
            text-align: center;
    }

</style>

<div class="page-content">
    <div class="box" id="needschedule-create">
        <!-- begin filter -->
        <div class="page-filter">
            <div class="" style="float:right;">
##                 <a href="javascript:void (0);" onclick="setCreateTimeDate('less')" class="btn btn-sm btn-default" ywl-filter="reload"><i class="glyphicon glyphicon-minus"></i> </a>
##                 <a href="javascript:void (0);" onclick="setEarlymorning('moring')" class="btn btn-sm btn-default" ywl-filter="reload"><i class="glyphicon glyphicon-time"></i> 凌晨</a>
##                 <a href="javascript:void (0);" onclick="setEarlymorning('noon');" class="btn btn-sm btn-default" ywl-filter="reload"><i class="glyphicon glyphicon-certificate"></i> 中午</a>
##                 <a href="javascript:void (0);" onclick="setCreateTimeDate('add');" class="btn btn-sm btn-default" ywl-filter="reload"><i class="glyphicon glyphicon-plus"></i> </a>
        </div>
        </div>
        <div class="modal-body">
            <div class="modal-body">
                    <form enctype="multipart/form-data" id="needinfo-list-action">
                        <input type="hidden" id="vtype_list_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>需求名称：</strong></label>
                                <div class="col-sm-6">
                                   <input id="need_name" maxlength="20">
                                </div>
                            </div>
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>套餐：</strong></label>
                                <div class="col-sm-6">
                                    <select id="package_id">
                                        <option value="">请选择</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>是否允许重复：</strong></label>
                                <div class="col-sm-6">
                                    <input type="radio" name="ifrepait" value="0" checked>允许重复</input>
                                    <input type="radio" name="ifrepait" value="1">不允许重复</input>
                                </div>
                            </div>
                              <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【1】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group" aria-label="...">

                                        <label>素材:</label>
                                        <select id="ads_id1">
                                            <option value="">请选择</option>
                                        </select>
                                        <input value="30" type="number" id="ads_interval1" style="width: 80px">

                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="1">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position1" style="width:50px;" min="0">
                                        </div>

                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【2】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id2">
                                                <option value="">请选择</option>
                                            </select>
                                        <input value="30" type="number" id="ads_interval2" style="width: 80px">

                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="2">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position2" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【3】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id3">
                                                <option value="">请选择</option>
                                            </select>
                                        <input value="30" type="number" id="ads_interval3" style="width: 80px">

                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="3">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position3" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【4】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id4">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval4" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="4">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position4" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【5】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id5">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval5" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="5">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position5" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【6】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id6">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval6" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="6">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position6" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【7】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id7">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval7" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="7">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position7" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【8】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id8">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval8" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="8">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position8" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【9】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id9">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval9" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="9">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position9" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【10】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id10">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval10" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="10">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position10" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【11】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id11">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval11" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="11">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position11" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>
                             <div class="form-group form-group-sm">
                                <label for="vtype_name" class="col-sm-3 control-label"><strong>广告【12】：</strong></label>
                                <div class="col-sm-6">
                                    <div class="btn-group"  aria-label="...">
                                            <label>素材:</label>
                                            <select id="ads_id12">
                                                <option value="">请选择</option>
                                            </select>
                                         <input value="30" type="number" id="ads_interval12" style="width: 80px">
                                        <div class="btn-group">
                                            <input type="checkbox" name="position" value="12">
                                        </div>
                                        <div class="btn-group">
                                            <label>位置:</label>
                                            <input type="number" id="position12" style="width:50px;" min="0">
                                        </div>
                                    </div>

                                </div>
                            </div>

                             <div class="form-group form-group-sm">
                                <label for="enable" class="col-sm-3 control-label"><strong>是否启用：</strong></label>
                                <div class="col-sm-6">
                                    <input name="enable" type="radio" value="1" checked/>Yes
                                    <input name="enable" type="radio" value="0" />No
                                </div>
                            </div>


##                             <div class="form-group form-group-sm">
##                                 <label for="ads_contents" class="col-sm-3 control-label"><strong>描述：</strong></label>
##                                 <div class="col-sm-6">
##                                     <textarea id="description" style="height: 100px;width: 290px" type="text"
##                                               maxlength="200" class="form-control" placeholder="需求描述"></textarea>
##                                 </div>
##                             </div>
                        </div>
                        <div class="form-horizontal">
                              <div class="form-group form-group-sm">
                                  <div class="col-sm-12">
                                     <table class="table table-bordered">
                                         <tr>
                                             <th>需求等级</th>
                                             <th>请选择</th>
##                                              <th>需求名称</th>
                                             <th>播放类型</th>

                                         </tr>
                                         <tr class="success">
                                             <td>【S】</td>
                                             <td><input type="checkbox" name="groupInfoS"></td>
##                                              <td><input type="text" id="need_nameS" style="width: 200px;"></td>
                                             <td>
                                                 <input name="need_play_typeS" type="radio" value="1" checked/>大广告
                                                 <input name="need_play_typeS" type="radio" value="2"/>角标播放
                                             </td>
                                         </tr>
##    A
                                         <tr class="active">
                                             <td>【A】</td>
                                             <td><input type="checkbox" name="groupInfoA" id="groupInfoA"></td>
##                                              <td><input type="text" id="need_nameA" style="width: 200px;"></td>
                                             <td>
                                                 <input name="need_play_typeA" type="radio" value="1" checked/>大广告
                                                 <input name="need_play_typeA" type="radio" value="2"/>角标播放
                                             </td>
                                         </tr>
##      B
                                         <tr class="danger">
                                             <td>【B】</td>
                                             <td><input type="checkbox" name="groupInfoB"></td>
##                                              <td><input type="text" id="need_nameB" style="width: 200px;"></td>
                                             <td>
                                                 <input name="need_play_typeB" type="radio" value="1" checked/>大广告
                                                 <input name="need_play_typeB" type="radio" value="2"/>角标播放
                                             </td>
                                         </tr>
##   C
                                         <tr class="active">
                                             <td>【C】</td>
                                             <td><input type="checkbox" name="groupInfoC"></td>
##                                              <td><input type="text" id="need_nameC" style="width: 200px;"></td>
                                             <td>
                                                 <input name="need_play_typeC" type="radio" value="1" checked/>大广告
                                                 <input name="need_play_typeC" type="radio" value="2"/>角标播放
                                             </td>
                                         </tr>
##   D

                                         <tr class="info">
                                             <td>【D】</td>
                                             <td><input type="checkbox" name="groupInfoD"></td>
##                                              <td><input type="text" id="need_nameD" style="width: 200px;"></td>
                                             <td>
                                                 <input name="need_play_typeD" type="radio" value="1" checked/>大广告
                                                 <input name="need_play_typeD" type="radio" value="2"/>角标播放
                                             </td>
                                         </tr>
                                     </table>
                                  </div>
                            </div>
                                </div>
                                    <div class="" style="float:right;">
                                           <a href="javascript:void (0);" onclick="createneedinfo();" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="glyphicon glyphicon-ok"></i> 创建</a>
                                    </div>
			</form>
    </div>
</div>
</div>
</div>


<script type="text/javascript">
  $(document).ready(function () {
     init()
    });
</script>









