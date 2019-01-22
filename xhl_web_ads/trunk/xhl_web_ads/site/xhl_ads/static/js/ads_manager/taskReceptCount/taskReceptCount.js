var chartsArr = []

function makecharts(type) {

    var date = $("#date").val()
    if (!date || date == "" || date == undefined) {
        alert("请选择日期")
        return
    }
    for (var i in chartsArr) {
        chartsArr[i].clear()
    }

    chartsArr.splice(0, chartsArr.length) //清空数据

    var option = {
        title: {
            x: "center",
            text: ''
        },

        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            orient: 'vertical',
            right: 'right',
            data: ['总投放', '总接受（含放弃）', '完成', '放弃', '正在进行中','未开始']
        },
        grid: {
            left: '15%',
            right: '20%',
            bottom: '20%',
            top: '10%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: []
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: []
    };
    $.post('/task/count', {"date": date,"type":type}, function (ret) {
        if (ret.code == 0) {
            if (ret.data.length <= 0) {
                alert("该天暂无数据");
                return
            }

            var head = ["S", "A", "B", "C", "D"]
            for (var r in ret.data) {
                var temp = ret.data[r]
                var total = []
                var recept = []
                var finish = []
                var forgo = []
                var ison = []
                var other = []
                total.push(temp['s'])
                total.push(temp['a'])
                total.push(temp['b'])
                total.push(temp['c'])
                total.push(temp['d'])

                recept.push(temp['s0'])
                recept.push(temp['a0'])
                recept.push(temp['b0'])
                recept.push(temp['c0'])
                recept.push(temp['d0'])

                finish.push(temp['s1'])
                finish.push(temp['a1'])
                finish.push(temp['b1'])
                finish.push(temp['c1'])
                finish.push(temp['d1'])

                forgo.push(temp['s2'])
                forgo.push(temp['a2'])
                forgo.push(temp['b2'])
                forgo.push(temp['c2'])
                forgo.push(temp['d2'])

                ison.push(temp['s3'])
                ison.push(temp['a3'])
                ison.push(temp['b3'])
                ison.push(temp['c3'])
                ison.push(temp['d3'])

                other.push(temp['s4'])
                other.push(temp['a4'])
                other.push(temp['b4'])
                other.push(temp['c4'])
                other.push(temp['d4'])

                option.series.push({name: "总投放", type: "bar", data: total})
                option.series.push({name: "总接受（含放弃）", type: "bar", data: recept})
                option.series.push({name: "完成", type: "bar", data: finish})
                option.series.push({name: "放弃", type: "bar", data: forgo})
                option.series.push({name: "正在进行中", type: "bar", data: ison})
                option.series.push({name: "未开始", type: "bar", data: other})

                option.xAxis[0].data = head
                option.title.text = temp["package_name"] ? "【套餐】:"+temp["package_name"] : "";
                var myChart = echarts.init(document.getElementById('main' + r));
                myChart.setOption(option);
                chartsArr.push(myChart);
                option.series.splice(0, option.series.length)


            }

        } else {
            alert("生成报表失败,请重试")
        }
    })
}