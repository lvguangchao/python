function grouptype() {
    $.get("/groupneedinfo/all", function (ret) {
        var SArr = [];
        var AArr = [];
        var BArr = [];
        var CArr = [];
        var DArr = [];
        var Arr = [];
        SArr.push("<option value=''>请选择</option>");
        AArr.push("<option value=''>请选择</option>");
        BArr.push("<option value=''>请选择</option>");
        CArr.push("<option value=''>请选择</option>");
        DArr.push("<option value=''>请选择</option>");
        $.each(ret, function (k, v) {

            if (v["anchor_level"] == "S") {
                SArr.push("<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>");
            }
            if (v["anchor_level"] == "A") {
                AArr.push("<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>");
            }
            if (v["anchor_level"] == "B") {
                BArr.push("<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>");
            }
            if (v["anchor_level"] == "C") {
                CArr.push("<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>");
            }
            if (v["anchor_level"] == "D") {
                DArr.push("<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>");
            }
        })

        $("#group_nameS").append(SArr.join(""));
        $("#group_nameA").append(AArr.join(""));
        $("#group_nameB").append(BArr.join(""));
        $("#group_nameC").append(CArr.join(""));
        $("#group_nameD").append(DArr.join(""));
        $("#group_name1").append(SArr.join(""));
        $("#group_name2").append(AArr.join(""));
        $("#group_name3").append(BArr.join(""));
        $("#group_name4").append(CArr.join(""));

        $("#group_name5").append(SArr.join(""));
        $("#group_name5").val(250);
        $("#group_name5").trigger("change");

        $("#group_name6").append(AArr.join(""));
        $("#group_name6").val(251);
        $("#group_name6").trigger("change");

        $("#group_name7").append(BArr.join(""));
        $("#group_name7").val(252);
        $("#group_name7").trigger("change");

        $("#group_name8").append(CArr.join(""));
        $("#group_name8").val(253);
        $("#group_name8").trigger("change");

        $("#group_name9").append(DArr.join(""));
        $("#group_name9").val(254);
        $("#group_name9").trigger("change");

    })
}


function show_adsInfo(id) {
    $.get("/needinfo/getadsinfo?id=" + id, function (ret) {

        $('#ads_name').val(ret.ads_name);
        $('#ads_contents').val(ret.ads_contents);
        $('#ads_time').val(ret.ads_time);
        $('#ads_materialurl').val(ret.ads_materialurl);
        var url = 'http://download.xiaohulu.com/obs/adsdownload/' + ret.ads_id + "/" + ret.ads_thumbnailurl
        var movieurl = 'http://download.xiaohulu.com/obs/adsdownload/' + ret.ads_id + "/" + ret.ads_materialurl
        $('#downMovieBt').attr("href", movieurl);
        $('#ads_thumbnailurl').attr("src", url);
        $("#preview").attr("src", "");
        $("#dialog-adsinfo-info").modal()

    })
}

function show_needInfo(id) {
    $.get("/needinfo/selectById?id=" + id, function (ret) {

        if (ret && ret.length > 0) {
            $('#need_name').val(ret[0].need_name);
            $('#package_name').val(ret[0].package_name);
            if (ret[0].need_play_type) {
                var type = ret[0].need_play_type;
                $('#need_play_type').val(type == 1 ? "大广告" : type == 2 ? "角标播放" : "未知");
            }

            $('#description').val(ret[0].description);
            $(":radio[name='enable'][value='" + ret[0].enable + "']").prop("checked", true);
            $("#dialog-needinfo-info").modal()
        } else {
            alert("没有找到对应数据");
        }
    })

}


function selectGroup(that) {
    var next = $(that).next()
    next.empty()
    var group_id = $(that).val()
    if (group_id != "") {
        $.get("/needinfo/selectBygruopId?groupid=" + group_id, function (ret) {
            var html = ''
            $.each(ret, function (k, v) {
                var needhtml = ["<span style='color: green;font-size: 15px;'>ads_id:</span>"]
                if (v["ads_id"]) {
                    var arr = v["ads_id"].split(",");
                    for (var i in arr) {
                        needhtml.push('<a href="javascript:void(0)" onclick="show_adsInfo(' + arr[i] + ')">【' + arr[i] + '】</a>')
                    }
                }
                html += "[<span style='color: red;font-size: 20px;'>" + v["anchor_level"] + "</span> <span style='color: green;font-size: 15px;'>need_id:  <a href=\"javascript:void(0)\" onclick=\"show_needInfo( " + v['need_id'] + ")\">【" + v["need_id"] + "】</span> </a> " + needhtml + "]   </br>"
            })
            next.append(html)
        })
    }
}

function createschedule() {

    var data = [];
    var levelS = $(":checkbox[name='anchor_levelS']").is(":checked");
    var levelA = $(":checkbox[name='anchor_levelA']").is(":checked");
    var levelB = $(":checkbox[name='anchor_levelB']").is(":checked");
    var levelC = $(":checkbox[name='anchor_levelC']").is(":checked");
    var levelD = $(":checkbox[name='anchor_levelD']").is(":checked");
    var level1 = $(":checkbox[name='anchor_level1']").is(":checked");
    var level2 = $(":checkbox[name='anchor_level2']").is(":checked");
    var level3 = $(":checkbox[name='anchor_level3']").is(":checked");
    var level4 = $(":checkbox[name='anchor_level4']").is(":checked");
    var level5 = $(":checkbox[name='anchor_level5']").is(":checked");
    var level6 = $(":checkbox[name='anchor_level6']").is(":checked");
    var level7 = $(":checkbox[name='anchor_level7']").is(":checked");
    var level8 = $(":checkbox[name='anchor_level8']").is(":checked");
    var level9 = $(":checkbox[name='anchor_level9']").is(":checked");


    if (levelS == true) {
        var group_id = $("#group_nameS").val();
        var group_name = $("#group_nameS").find("option:selected").text();
        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择S级分组");
            return;
        }
        var count = $("#countS").val();
        var anchor_if_exp = $("#anchor_if_expS").val();
        var lv_priority = $("#lv_priorityS").val();
        var assign_flag = $(":radio[name='assign_flagS']:checked").val()

        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入S级公式");
            return;
        }
        var create_time = $("#create_timeS").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入S级别时间");
            return;
        }


        var s = {
            assign_flag: assign_flag,
            group_name: group_name+"_"+getYMHS(create_time)+"【S级】",
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time
        };
        data.push(s);
    }
    if (levelA == true) {
        var group_id = $("#group_nameA").val();
        var group_name = $("#group_nameA").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flagA']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择A级分组");
            return;
        }
        var count = $("#countA").val();
        var anchor_if_exp = $("#anchor_if_expA").val();
        var lv_priority = $("#lv_priorityA").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入级公式");
            return;
        }
        var create_time = $("#create_timeA").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入A级别时间");
            return;
        }

        var a = {
            assign_flag: assign_flag,
            group_id: group_id,
            group_name: group_name+"_"+getYMHS(create_time)+"【A级】",
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,

        };
        data.push(a);
    }
    if (levelB == true) {
        var group_id = $("#group_nameB").val();
        var group_name = $("#group_nameB").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flagB']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择B级分组");
            return
        }
        var count = $("#countB").val();
        var anchor_if_exp = $("#anchor_if_expB").val();
        var lv_priority = $("#lv_priorityB").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入B级公式");
            return
        }
        var create_time = $("#create_timeB").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入B级别时间");
            return;
        }
        var b = {
            assign_flag: assign_flag,
            group_name: group_name+"_"+getYMHS(create_time)+"【B级】",
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time
        };
        data.push(b)
    }
    if (levelC == true) {
        var group_id = $("#group_nameC").val();
        var group_name = $("#group_nameC").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flagC']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择C级分组");
            return
        }
        var count = $("#countC").val();
        var anchor_if_exp = $("#anchor_if_expC").val();
        var lv_priority = $("#lv_priorityC").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入C级公式");
            return
        }
        var create_time = $("#create_timeC").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入C级别时间");
            return;
        }
        var c = {
            assign_flag: assign_flag,
            group_name: group_name+"_"+getYMHS(create_time)+"【C级】",
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time
        };
        data.push(c);
    }
    if (levelD == true) {
        var group_id = $("#group_nameD").val();
        var group_name = $("#group_nameD").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flagD']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择D级分组");
            return;
        }
        var count = $("#countD").val();
        var anchor_if_exp = $("#anchor_if_expD").val();
        var lv_priority = $("#lv_priorityD").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入D级公式");
            return
        }
        var create_time = $("#create_timeD").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入D级别时间");
            return;
        }
        var d = {
            assign_flag: assign_flag,
            group_name: group_name+"_"+getYMHS(create_time)+"【D级】",
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time

        };
        data.push(d)
    }
    if (level1 == true) {
        var group_id = $("#group_name1").val();
        var group_name = $("#group_name1").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flag1']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【定制S】分组");
            return;
        }
        var count = $("#count1").val();
        var anchor_if_exp = $("#anchor_if_exp1").val();
        var lv_priority = $("#lv_priority1").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【定制S】公式");
            return
        }
        var create_time = $("#create_time1").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【定制S】时间");
            return;
        }
        var d = {
            group_name: group_name +"_"+getYMHS(create_time)+ "【定制S】",
            assign_flag: assign_flag,
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time

        };
        data.push(d)
    }
    if (level2 == true) {
        var group_id = $("#group_name2").val();
        var group_name = $("#group_name2").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flag2']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【定制A】分组");
            return;
        }
        var count = $("#count2").val();
        var anchor_if_exp = $("#anchor_if_exp2").val();
        var lv_priority = $("#lv_priority2").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【定制A】公式");
            return
        }
        var create_time = $("#create_time2").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【定制A】时间");
            return;
        }
        var d = {
            group_name: group_name +"_"+getYMHS(create_time)+ "【定制A】",
            assign_flag: assign_flag,
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time

        };
        data.push(d)
    }

    if (level3 == true) {
        var group_id = $("#group_name3").val();
        var group_name = $("#group_name3").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flag3']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【定制B】分组");
            return;
        }
        var count = $("#count3").val();
        var anchor_if_exp = $("#anchor_if_exp3").val();
        var lv_priority = $("#lv_priority3").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【定制B】公式");
            return
        }
        var create_time = $("#create_time3").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【定制B】时间");
            return;
        }
        var d = {
            group_name: group_name +"_"+getYMHS(create_time)+ "【定制B】",
            assign_flag: assign_flag,
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time

        };
        data.push(d)
    }

    if (level4 == true) {
        var group_id = $("#group_name4").val();
        var group_name = $("#group_name4").find("option:selected").text();
        var assign_flag = $(":radio[name='assign_flag4']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【定制C】分组");
            return;
        }
        var count = $("#count4").val();
        var anchor_if_exp = $("#anchor_if_exp4").val();
        var lv_priority = $("#lv_priority4").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【定制C】公式");
            return
        }
        var create_time = $("#create_time4").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【定制C】时间");
            return;
        }
        var d = {
            group_name: group_name +"_"+getYMHS(create_time)+ "【定制C】",
            assign_flag: assign_flag,
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time

        };
        data.push(d)
    }  if (level5 == true) {
        var group_id = $("#group_name5").val();
        var group_name = $("#group_name5").find("option:selected").text();
        var delidays = $("#delidays5").val();
        // var assign_flag = $(":radio[name='assign_flag5']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【新手任务S】分组");
            return;
        }
        var count = $("#count5").val();
        var anchor_if_exp = $("#anchor_if_exp5").val();
        var lv_priority = $("#lv_priority5").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【新手任务S】公式");
            return
        }
        var create_time = $("#create_time5").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【新手任务S】时间");
            return;
        } if (!delidays || delidays == "" || delidays == undefined) {
            alert("请输入【新手任务S】连续投放天数");
            return;
        }
        var d = {
            group_name: group_name +"_",
            assign_flag: '0',
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,
            delidays: delidays,
            msg: 'S'

        };
        data.push(d)
    } if (level6 == true) {
        var group_id = $("#group_name6").val();
        var group_name = $("#group_name6").find("option:selected").text();
        var delidays = $("#delidays6").val();
        // var assign_flag = $(":radio[name='assign_flag5']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【新手任务A】分组");
            return;
        }
        var count = $("#count5").val();
        var anchor_if_exp = $("#anchor_if_exp6").val();
        var lv_priority = $("#lv_priority6").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【新手任务A】公式");
            return
        }
        var create_time = $("#create_time6").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【新手任务A】时间");
            return;
        } if (!delidays || delidays == "" || delidays == undefined) {
            alert("请输入【新手任务A】连续投放天数");
            return;
        }
        var d = {
            group_name: group_name +"_",
            assign_flag: '0',
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,
            delidays: delidays,
            msg: 'A'

        };
        data.push(d)
    } if (level7 == true) {
        var group_id = $("#group_name7").val();
        var group_name = $("#group_name7").find("option:selected").text();
        var delidays = $("#delidays7").val();
        // var assign_flag = $(":radio[name='assign_flag5']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【新手任务B】分组");
            return;
        }
        var count = $("#count7").val();
        var anchor_if_exp = $("#anchor_if_exp7").val();
        var lv_priority = $("#lv_priority7").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【新手任务B】公式");
            return
        }
        var create_time = $("#create_time7").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【新手任务B】时间");
            return;
        } if (!delidays || delidays == "" || delidays == undefined) {
            alert("请输入【新手任务B】连续投放天数");
            return;
        }
        var d = {
            group_name: group_name +"_",
            assign_flag: '0',
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,
            delidays: delidays,
            msg: 'B'

        };
        data.push(d)
    } if (level8 == true) {
        var group_id = $("#group_name8").val();
        var group_name = $("#group_name8").find("option:selected").text();
        var delidays = $("#delidays8").val();
        // var assign_flag = $(":radio[name='assign_flag5']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【新手任务C】分组");
            return;
        }
        var count = $("#count8").val();
        var anchor_if_exp = $("#anchor_if_exp8").val();
        var lv_priority = $("#lv_priority8").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【新手任务C】公式");
            return
        }
        var create_time = $("#create_time8").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【新手任务C】时间");
            return;
        } if (!delidays || delidays == "" || delidays == undefined) {
            alert("请输入【新手任务C】连续投放天数");
            return;
        }
        var d = {
            group_name: group_name +"_",
            assign_flag: '0',
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,
            delidays: delidays,
            msg: 'C'

        };
        data.push(d)
    } if (level9 == true) {
        var group_id = $("#group_name9").val();
        var group_name = $("#group_name9").find("option:selected").text();
        var delidays = $("#delidays9").val();
        // var assign_flag = $(":radio[name='assign_flag5']:checked").val()

        if (!group_id || group_id == "" || group_id == undefined) {
            alert("请选择【新手任务D】分组");
            return;
        }
        var count = $("#count9").val();
        var anchor_if_exp = $("#anchor_if_exp9").val();
        var lv_priority = $("#lv_priority9").val();
        if (!anchor_if_exp || anchor_if_exp == "" || anchor_if_exp == undefined) {
            alert("请输入【新手任务D】公式");
            return
        }
        var create_time = $("#create_time9").val();
        if (!create_time || create_time == "" || create_time == undefined) {
            alert("请输入【新手任务D】时间");
            return;
        } if (!delidays || delidays == "" || delidays == undefined) {
            alert("请输入【新手任务D】连续投放天数");
            return;
        }
        var d = {
            group_name: group_name +"_",
            assign_flag: '0',
            group_id: group_id,
            count: count,
            anchor_if_exp: anchor_if_exp,
            lv_priority: lv_priority,
            create_time: create_time,
            delidays: delidays,
            msg: 'D'

        };
        data.push(d)
    }

    if (data.length > 0) {

        $.ajax({
            type: "POST",
            url: "/needschedule/add",
            data: {"param": JSON.stringify(data)},
            success: function (msg) {
                if (msg.code == 0) {
                    alert("广告投放成功");
                    // window.open("","_self").close();

                } else {
                    alert("广告投放失败," + msg.message);
                }
            },
            error: function () {
                alert("网络故障，广告投放失败");
            }

        });

    } else {
        alert("还没有选择任何等级复选框");
        return;
    }
}

function setEarlymorning(type) {

    var oDate = new Date(); //实例一个时间对象；
    oDate.setDate(oDate.getDate() + 1)

    var year = ("0" + (oDate.getFullYear())).slice(-4);
	var month = ("0" + (oDate.getMonth() + 1)).slice(-2);
	var day = ("0" + (oDate.getDate())).slice(-2);

    var value = ''
    if (type == "moring") {
        value = year + "-" + month + "-" + day + " 00:01:00"
    } else if (type == "noon") {
        value = year + "-" + month + "-" + day + " 12:01:00"
    }
    $("#create_timeS").val(value)
    $("#create_timeA").val(value)
    $("#create_timeB").val(value)
    $("#create_timeC").val(value)
    $("#create_timeD").val(value)
    $("#create_time1").val(value)
    $("#create_time2").val(value)
    $("#create_time3").val(value)
    $("#create_time4").val(value)
    $("#create_time5").val(value)
    $("#create_time6").val(value)
    $("#create_time7").val(value)
    $("#create_time8").val(value)
    $("#create_time9").val(value)

}

function setCreateTimeDate(type) {
    $("[id^='create_time']").each(function () {
        var date = new Date($(this).val())
        if (type == "add") {
            date.setDate(date.getDate() + 1)
        }else if(type="less"){
            date.setDate(date.getDate() - 1)
        }

        var year = ("0" + (date.getFullYear())).slice(-4);
        var month = ("0" + (date.getMonth() + 1)).slice(-2);
        var day = ("0" + (date.getDate())).slice(-2);
        var hour = ("0" + (date.getHours())).slice(-2);
        var minute = ("0" + (date.getMinutes())).slice(-2);
        var second = ("0" + (date.getSeconds())).slice(-2);
        var value=(year + '-' + month + '-' + day + ' ' + hour+':' + minute + ':' + second)
        $(this).val(value)
    })
}



function setDisabled() {
    $(":checkbox[name^='anchor_level']").each(function () {
        $(this).click(function () {
            var selector=$(this).attr("name")
            var repx=selector.substr(selector.length-1);
        if ($(this).is(':checked') == true) {
             var rexp=$(this).select()
            $("#group_name" + repx).removeAttr("disabled");
            $("#count" + repx).removeAttr("disabled");
            $("#anchor_if_exp" + repx).removeAttr("disabled");
            $("#lv_priority" + repx).removeAttr("disabled");

             $("#group_name" + repx).addClass("disabledClass");
            $("#count" + repx).addClass("disabledClass");
            $("#anchor_if_exp" + repx).addClass("disabledClass");
            $("#lv_priority" + repx).addClass("disabledClass");
            $("#create_time" + repx).addClass("disabledClass");


        } else {
            $("#group_name" + repx).attr("disabled", "disabled");
            $("#count" + repx).attr("disabled", "disabled");
            $("#anchor_if_exp" + repx).attr("disabled", "disabled");
            $("#lv_priority" + repx).attr("disabled", "disabled");
            $("#group_name" + repx).removeClass("disabledClass");
            $("#count" + repx).removeClass("disabledClass");
            $("#anchor_if_exp" + repx).removeClass("disabledClass");
            $("#lv_priority" + repx).removeClass("disabledClass");
            $("#create_time" + repx).removeClass("disabledClass");

        }
    });
    })
}