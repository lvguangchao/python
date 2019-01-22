<%!
    page_title_ = '任务接受情况统计图'
    page_menu_ = ['plan', 'taskcount']
    page_id_ = 'taskcount'
%>
<%inherit file="../../page_base.mako"/>

<%block name="extend_js">
    <link href="${ static_url('css/style.css') }" rel="stylesheet">
    <script type="text/javascript" src="${ static_url('plugins/laydate/laydate.js') }"></script>
    <script type="text/javascript" src="${ static_url('plugins/echarts/echarts.js') }"></script>
    <script type="text/javascript"
            src="${ static_url('js/ads_manager/taskReceptCount/taskReceptCount.js') }"></script>

##
</%block>

<body>
<div style="margin-top: 17px;margin-left: 38px;">
    <strong>日期：</strong></label>
    <input id="date"/>
    <button type="button" class="btn btn-sm btn-primary" data-dismiss="modal" onclick="makecharts(1)">
        <i class="glyphicon glyphicon-search"></i>查询

        <button type="button" class="btn btn-sm btn-primary" data-dismiss="modal" onclick="makecharts(2)">
        <i class="glyphicon glyphicon-refresh"></i>刷新报表
    </button>

</div>


<div style="display: flex;flex-wrap: wrap;align-content: space-between; margin-top: 70px;">
<div id="main0" style="width: 600px; height: 400px;"></div>
<div id="main1" style="width: 600px; height: 400px;"></div>
<div id="main2" style="width: 600px; height: 400px;"></div>
<div id="main3" style="width: 600px; height: 400px;"></div>
<div id="main4" style="width: 600px; height: 400px;"></div>
<div id="main5" style="width: 600px; height: 400px;"></div>
<div id="main6" style="width: 600px; height: 400px;"></div>
<div id="main7" style="width: 600px; height: 400px;"></div>
<div id="main8" style="width: 600px; height: 400px;"></div>
<div id="main9" style="width: 600px; height: 400px;"></div>
    </div>
<script type="text/javascript">

    $(document).ready(function () {

        laydate.render({
            elem: '#date',
            done: function (value, date, endDate) {
                $("#date").val(value);

            }
        });
          $("#date").val(getDate());
          makecharts(1)  //加载一次统计图

    });


</script>
</body>

