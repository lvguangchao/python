function get_anchor_stock() {
    var date=$("#date").val()
    $("#tomonth").text(date)

    $.post('/anchorstock/list',{date:date},function (ret) {
        var anchor_day=ret['data']['day']
        var anchor_all=ret['data']['all']
        $("#anchor_stock tbody").html("");
        // progress-bar-info
        var dom_html='<div class="progress"><div class="progress-bar progress-bar-success {2}"  role="progressbar" aria-valuenow="60" ' +
            'aria-valuemin="0" aria-valuemax="100" style="width:{0}%; color:#774b00">{1}%</div></div>'
        for(var i=0 in anchor_day){
            var rate_s=((anchor_day[i].order_s/anchor_all.s)*100).toFixed(2)
            var rate_a=((anchor_day[i].order_a/anchor_all.a)*100).toFixed(2)
            var rate_b=((anchor_day[i].order_b/anchor_all.b)*100).toFixed(2)
            var rate_c=((anchor_day[i].order_c/anchor_all.c)*100).toFixed(2)
            var rate_d=((anchor_day[i].order_d/anchor_all.d)*100).toFixed(2)
            var p_s= dom_html.format(rate_s,rate_s);
            var p_a= dom_html.format(rate_a,rate_a);
            var p_b= dom_html.format(rate_b,rate_b);
            var p_c= dom_html.format(rate_c,rate_c);
            var p_d= dom_html.format(rate_d,rate_d);
            if(rate_s>50){
                 p_s= dom_html.format(rate_s,rate_s,'progress-bar-warning');
            } if(rate_a>50){
                 p_a= dom_html.format(rate_a,rate_a,'progress-bar-warning');
            } if(rate_b>50){
                 p_b= dom_html.format(rate_b,rate_b,'progress-bar-warning');
            } if(rate_c>50){
                 p_c= dom_html.format(rate_c,rate_c,'progress-bar-warning');
            } if(rate_d>50){
                 p_d= dom_html.format(rate_d,rate_d,'progress-bar-warning');
            }if(rate_s>80){
                 p_s= dom_html.format(rate_s,rate_s,'progress-bar-danger');
            } if(rate_a>80){
                 p_a= dom_html.format(rate_a,rate_a,'progress-bar-danger');
            } if(rate_b>80){
                 p_b= dom_html.format(rate_b,rate_b,'progress-bar-danger');
            } if(rate_c>80){
                 p_c= dom_html.format(rate_c,rate_c,'progress-bar-danger');
            } if(rate_d>80){
                 p_d= dom_html.format(rate_d,rate_d,'progress-bar-danger');
            }
            var num=Math.floor(Math.random()*5+1);
            var tr_class=class_array[num]
            $("#anchor_stock").append("<tr class="+tr_class+">" +
                "<td >" + anchor_day[i].order_date + "</td>" +
                "<td >" + (anchor_day[i].order_s) + "/<label style='color: red'>" + (anchor_all.s) + "</label>" + p_s + "</td>" +
                "<td >" + (anchor_day[i].order_a) + "/<label style='color: red'>" + (anchor_all.a) + "</label>" + p_a + "</td>" +
                "<td >" + (anchor_day[i].order_b) + "/<label style='color: red'>" + (anchor_all.b) + "</label>" + p_b + "</td>" +
                "<td >" + (anchor_day[i].order_c) + "/<label style='color: red'>" + (anchor_all.c) + "</label>" + p_c + "</td>" +
                "<td >" + (anchor_day[i].order_d) + "/<label style='color: red'>" + (anchor_all.d) + "</label>" + p_d + "</td>" +
                "<tr>");
        }

        $("#anchor_all tbody").html("");
         $("#anchor_all").append("<tr>" +
                "<td>" + "主播人数 " + "</td>" +
                "<td>" + anchor_all.s + "</td>" +
                "<td>" + anchor_all.a + "</td>" +
                "<td>" + anchor_all.b + "</td>" +
                "<td>" + anchor_all.c + "</td>" +
                "<td>" + anchor_all.d + "</td>" +
                "<tr>");

    })
}