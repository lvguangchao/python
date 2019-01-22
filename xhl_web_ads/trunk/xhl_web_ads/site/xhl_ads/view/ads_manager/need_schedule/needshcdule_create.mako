<%!
    page_title_ = 'schedule添加'
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
    <script type="text/javascript" src="${ static_url('js/ads_manager/need_schedule/need_schedule_add.js') }"></script>
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
                <a href="javascript:void (0);" onclick="setCreateTimeDate('less')" class="btn btn-sm btn-default"><i class="glyphicon glyphicon-minus"></i> </a>
                <a href="javascript:void (0);" onclick="setEarlymorning('moring')" class="btn btn-sm btn-default"><i class="glyphicon glyphicon-time"></i> 凌晨</a>
                <a href="javascript:void (0);" onclick="setEarlymorning('noon');" class="btn btn-sm btn-default"><i class="glyphicon glyphicon-certificate"></i> 中午</a>
                <a href="javascript:void (0);" onclick="setCreateTimeDate('add');" class="btn btn-sm btn-default"><i class="glyphicon glyphicon-plus"></i> </a>
                <a href="javascript:void (0);" onclick="flushschedule();" class="btn btn-sm btn-primary" ywl-filter="flush"><i class="glyphicon glyphicon-refresh"></i> 刷新广告</a>

            </div>
            <div>

            </div>
        </div>
        <div class="modal-body">
                    <form enctype="multipart/form-data" id="needschedule-list-action">
                        <input type="hidden" id="vtype_list_id">
                        <div class="form-horizontal">
                              <div class="form-group form-group-sm">
                                  <div class="col-sm-12">

                                     <table class="table table-bordered">
                                         <tr>
                                             <th>#</th>
                                             <th>请勾选</th>
                                             <th>组名</th>
                                             <th>投放量</th>
                                             <th>公式</th>
                                             <th>优先级</th>
                                             <th>投放时间</th>
                                             <th>分配</th>
                                         </tr>
                                         <tr class="success">
                                             <td>【S】</td>
                                             <td><input type="checkbox" name="anchor_levelS"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_nameS" style="width: 300px" disabled>
                                             </select>
                                                 <div style="text-align: left;">
                                                 </div>
                                                 </div>
                                             </td>
                                             <td><input type="number" id="countS" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_expS" value="level>=5" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priorityS" value="15" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_timeS" value="" style=" border:1px solid #9bdf70;background:#f0fbeb"></td>
                                             <td>
                                                 <input type="radio" name="assign_flagS" value="0" checked>按条件分配</input>
                                             </td>
                                         </tr> <tr   class="active">
                                             <td>【A】</td>
                                            <td><input type="checkbox" name="anchor_levelA"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_nameA" style="width: 300px" disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="countA" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_expA" value="level>=4" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priorityA" value="14" min="0" style="width: 50px" disabled></td>
                                            <td><input type="text" id="create_timeA"></td>
                                             <td>
                                                 <input type="radio" name="assign_flagA" value="0" checked>按条件分配</input>
                                             </td>

                                         </tr> <tr class="warning">
                                             <td>【B】</td>
                                            <td><input type="checkbox" name="anchor_levelB"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_nameB" style="width: 300px" disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="countB" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_expB" value="level>=3" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priorityB" value="13" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_timeB"></td>
                                         <td>
                                             <input type="radio" name="assign_flagB" value="0" checked>按条件分配</input>
                                         </td>

                                         </tr> <tr class="active">
                                             <td>【C】</td>
                                            <td><input type="checkbox" name="anchor_levelC"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_nameC" style="width: 300px" disabled>
                                             </select>
                                                 <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="countC" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_expC" value="level>=2" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priorityC" value="12" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_timeC"></td>
                                          <td>
                                             <input type="radio" name="assign_flagC" value="0" checked>按条件分配</input>
                                         </td>

                                         </tr> <tr class="danger">
                                             <td>【D】</td>
                                            <td><input type="checkbox" name="anchor_levelD"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_nameD" style="width: 300px" disabled>
                                             </select>
                                                 <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="countD" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_expD" value="level>=1" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priorityD" value="11" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_timeD"></td>
                                          <td>
                                             <input type="radio" name="assign_flagD" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>
                                         <tr class="active">
                                             <td>【定制S】</td>
                                            <td><input type="checkbox" name="anchor_level1"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name1" style="width: 300px" disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count1" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp1" value="level>=100" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority1" value="26" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time1"></td>
                                              <td>
                                             <input type="radio" name="assign_flag1" value="1" checked>白名单分配</input>
                                         </td>
                                         </tr>
                                         <tr class="success">
                                             <td>【定制A】</td>
                                            <td><input type="checkbox" name="anchor_level2"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name2" style="width: 300px" disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count2" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp2" value="level>=100" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority2" value="25" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time2"></td>
                                              <td>
                                             <input type="radio" name="assign_flag2" value="1" checked>白名单分配</input>
                                         </td>
                                         </tr>
                                         <tr class="active">
                                             <td>【定制B】</td>
                                            <td><input type="checkbox" name="anchor_level3"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name3" style="width: 300px" disabled>
                                             </select>
                                                 <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count3" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp3" value="level>=100" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority3" value="24" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time3"></td>
                                              <td>
                                             <input type="radio" name="assign_flag3" value="1" checked>白名单分配</input>
                                         </td>
                                         </tr>
                                         <tr class="danger">
                                             <td>【定制C】</td>
                                            <td><input type="checkbox" name="anchor_level4"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name4" style="width: 300px" disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count4" value="10" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp4" value="level>=100" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority4" value="23" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time4"></td>
                                              <td>
                                             <input type="radio" name="assign_flag4" value="1" checked>白名单分配</input>
                                         </td>
                                         </tr>
                                         <tr class="active">
                                             <td>【新手S】</td>
                                            <td><input type="checkbox" name="anchor_level5"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name5" style="width: 300px"  disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count5" value="600" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp5" value="level>=5 and new_user=True" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority5" value="5" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time5"></td>
                                              <td>
                                                  <label>投放天数</label>
                                                  <input type="number" id="delidays5" value="1" min="0" max="10" style="width: 50px">
##                                              <input type="radio" name="assign_flag5" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>     <tr class="info">
                                             <td>【新手A】</td>
                                            <td><input type="checkbox" name="anchor_level6"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name6" style="width: 300px"  disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count6" value="600" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp6" value="level>=4 and new_user=True" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority6" value="4" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time6"></td>
                                              <td>
                                                  <label>投放天数</label>
                                                  <input type="number" id="delidays6" value="1" min="0" max="10" style="width: 50px">
##                                              <input type="radio" name="assign_flag5" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>     <tr class="warning">
                                             <td>【新手B】</td>
                                            <td><input type="checkbox" name="anchor_level7"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name7" style="width: 300px"  disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count7" value="600" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp7" value="level>=3 and new_user=True" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority7" value="3" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time7"></td>
                                              <td>
                                                  <label>投放天数</label>
                                                  <input type="number" id="delidays7" value="1" min="0" max="10" style="width: 50px">
##                                              <input type="radio" name="assign_flag5" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>     <tr class="success">
                                             <td>【新手C】</td>
                                            <td><input type="checkbox" name="anchor_level8"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name8" style="width: 300px"  disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count8" value="600" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp8" value="level>=2 and new_user=True" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority8" value="2" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time8"></td>
                                              <td>
                                                  <label>投放天数</label>
                                                  <input type="number" id="delidays8" value="1" min="0" max="10" style="width: 50px">
##                                              <input type="radio" name="assign_flag5" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>     <tr class="danger">
                                             <td>【新手D】</td>
                                            <td><input type="checkbox" name="anchor_level9"></td>
                                             <td><div style=" display: flex;flex-direction: column;justify-content: space-between;align-items: center;">
                                                 <select onchange="selectGroup(this)" id="group_name9" style="width: 300px"  disabled>
                                             </select>
                                                  <div style="text-align: left;">
                                                 </div>
                                             </div>
                                             </td>
                                             <td><input type="number" id="count9" value="600" min="0" style="width: 100px" disabled></td>
                                             <td><input type="text" id="anchor_if_exp9" value="level>=1 and new_user=True" style="width: 350px" disabled></td>
                                             <td><input type="number" id="lv_priority9" value="1" min="0" style="width: 50px" disabled></td>
                                             <td><input type="text" id="create_time9"></td>
                                              <td>
                                                  <label>投放天数</label>
                                                  <input type="number" id="delidays9" value="1" min="0" max="10" style="width: 50px">
##                                              <input type="radio" name="assign_flag5" value="0" checked>按条件分配</input>
                                         </td>
                                         </tr>
                                     </table>
                                  </div>
                            </div>
                                </div>
                                    <div class="" style="float:right;">
                                           <a href="javascript:void (0);" onclick="createschedule();" class="btn btn-sm btn-primary" ywl-filter="reload"><i class="glyphicon glyphicon-ok"></i> 创建</a>
                                    </div>
                    </form>
				</div>
    </div>
</div>

<%block name="extend_content">
	<div class="modal fade" id="dialog-needinfo-info" tabindex="-1" role="dialog">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">need_info信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="needschedule-list-action">
                        <input type="hidden" id="vtype_list_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="group_name" class="col-sm-3 control-label"><strong>需求名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="need_name" type="text" class="form-control" readonly url="sss"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="package_id" class="col-sm-3 control-label"><strong>套餐名称：</strong></label>
                                <div class="col-sm-6">
                                <input id="package_name" type="text" class="form-control" readonly/>
                                </div>
                            </div>
                            <div class="form-group form-group-sm">
                                <label for="anchor_alloc_type" class="col-sm-3 control-label"><strong>播放类型：</strong></label>
                                <div class="col-sm-6">
                                    <input id="need_play_type" class="form-control" value="1" readonly/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="enable" class="col-sm-3 control-label"><strong>是否启用：</strong></label>
                                <div class="col-sm-6">
                                    <input name="enable" type="radio" value="1" disabled/>Yes
                                    <input name="enable" type="radio" value="0" disabled/>No
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="comment" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="comment" style="height: 100px;width: 290px" type="text"
                                              maxlength="200" class="form-control" readonly></textarea>
                                </div>
                            </div>
                            <div id="dlg-notice">
##                                 <div class="form-group form-group-sm">
##                                     <div class="col-sm-3"></div>
##                                     <div class="col-sm-6">
##                                         注意，广告位复选框需勾选中 <span class="mono h4">下拉选择才有效</span> ！
##                                     </div>
##                                 </div>
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

<div class="modal fade" id="dialog-adsinfo-info" tabindex="-1" role="dialog" data-backdrop="static" data-keyboard="false">
		<div class="modal-dialog" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<h3 class="modal-title">广告素材信息</h3>
				</div>
                <div class="modal-body">
                    <form enctype="multipart/form-data" id="version-list-action">
                        <input type="hidden" id="ptype_id">
                        <div class="form-horizontal">
                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_name" class="col-sm-3 control-label"><strong>素材名称：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_name" type="text" maxlength="20" class="form-control" readonly/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm" id="vtype-div">
                                <label for="ads_time" class="col-sm-3 control-label"><strong>广告视频时长：</strong></label>
                                <div class="col-sm-6">
                                    <input id="ads_time" type="number" type="number" readonly class="form-control"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_materialurl" class="col-sm-3 control-label"><strong>视频：</strong></label>
                                <div class="col-sm-6">
                                    <div class="input-group">
                                        <input  id="ads_materialurl" type="text" readonly class="form-control">
                                        <span class="input-group-btn"><a class="btn btn-default" href="" id="downMovieBt"
                                         target="_blank">下载</a></span>
                                    </div><!-- /input-group -->
                                </div><!-- /.col-lg-6onClick="downloadMovie(this)" -->

                            </div>
                            <div class="form-group form-group-sm">
                                <label for="ads_thumbnailurl" class="col-sm-3 control-label"><strong>图片：</strong></label>
                                <div class="col-sm-6">
                                    <img id="ads_thumbnailurl" style="width: 50%;height: 25%;" class="form-control"/>
                                </div>
                            </div>

                            <div class="form-group form-group-sm">
                                <label for="ads_contents" class="col-sm-3 control-label"><strong>描述：</strong></label>
                                <div class="col-sm-6">
                                    <textarea id="ads_contents" style="height: 100px;width: 290px" type="text" readonly class="form-control"></textarea>
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
					<button type="button" class="btn btn-sm btn-default" data-dismiss="modal"><i class="fa fa-close fa-fw"></i> 取消</button>
				</div>
			</div>
		</div>
	</div>
<script type="text/javascript">
  $(document).ready(function () {
        var date = getDate(1) + " 00:01:00"
        $("#create_timeS").val(date);
        $("#create_timeA").val(date);
        $("#create_timeB").val(date);
        $("#create_timeC").val(date);
        $("#create_timeD").val(date);
        $("#create_time1").val(date);
        $("#create_time2").val(date);
        $("#create_time3").val(date);
        $("#create_time4").val(date);
        var date2 = getDate(1) + " 11:01:00"
        $("#create_time5").val(date2);
        $("#create_time6").val(date2);
        $("#create_time7").val(date2);
        $("#create_time8").val(date2);
        $("#create_time9").val(date2);
        grouptype();
         laydate.render({
          elem: '#create_timeS',
          type:'datetime'
          , done: function (value, date, endDate) {
                 $("#create_timeS").val(value);
                 $("#create_timeA").val(value);
                 $("#create_timeB").val(value);
                 $("#create_timeC").val(value);
                 $("#create_timeD").val(value);
                 $("#create_time1").val(value);
                 $("#create_time2").val(value);
                 $("#create_time3").val(value);
                 $("#create_time4").val(value);
                 $("#create_time5").val(value);
                 $("#create_time6").val(value);
                 $("#create_time7").val(value);
                 $("#create_time9").val(value);
                 $("#create_time8").val(value);
##                  $("#create_time5").val(value);

          }
      });

         setDisabled()



    });





</script>









