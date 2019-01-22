function setPackSelect() {
    $.get("/packinfo/select", function (ret) {
            var auxArr = [];
            $.each(ret, function (k, v) {
                auxArr[k] = "<option value='" + v["package_id"] + "'>" + v["package_name"] + "</option>";
            });
            $('[id="package_id"]').append(auxArr.join(''));

        }
    );
}

function setAdsSelect() {
    $.get("/adsinfo/select", function (ret) {
            var auxArr = [];
            $.each(ret, function (k, v) {
                auxArr[k] = "<option value='" + v["ads_id"] + "'>" + v["ads_name"] + "</option>";
            });
            $("[id^='ads_id']").append(auxArr.join(''));

        }
    );
}

function setGroupInfoSelect() {
    $.get("/groupinfo/select", function (ret) {
            var auxArr = [];
            $.each(ret, function (k, v) {
                auxArr[k] = "<option value='" + v["ads_need_group_id"] + "'>" + v["group_name"] + "</option>";
            });
            $("[id^='group_id']").append(auxArr.join(''));

        }
    );
}

function init() {
    setPackSelect();
    setAdsSelect();
    setGroupInfoSelect()
}

function createneedinfo() {
    // var description = $('#description').val()
    var need_names = $('#need_name').val()
    var package_id = $('#package_id').val()
    var package_name=$("#package_id").find("option:selected").text()
    var enable = $("input[name='enable']:checked").val();
    var ifrepait=$(":radio[name='ifrepait']:checked").val()

    if (!need_names || need_names == "") {
        alert("需求名称不能为空");
        return;
    }
    if (!package_id || package_id == "") {
        alert("套餐不能为空");
        return;
    }

    if (!enable || enable == "") {
        alert("请选择是否启用");
        return;
    }
    // if (!description || description == "") {
    //     alert("描述不能为空");
    //     return;
    // }
    var parr = []
    $.each($(":checkbox[name='position']:checked"), function () {
        parr.push($(this).val());
    });


    var ads_arr = []
    var interval_arr = []
    var position_arr = []
    var ads_id1 = $("#ads_id1").val()
    var ads_id2 = $("#ads_id2").val()
    var ads_id3 = $("#ads_id3").val()
    var ads_id4 = $("#ads_id4").val()
    var ads_id5 = $("#ads_id5").val()
    var ads_id6 = $("#ads_id6").val()
    var ads_id7 = $("#ads_id7").val()
    var ads_id8 = $("#ads_id8").val()
    var ads_id9 = $("#ads_id9").val()
    var ads_id10 = $("#ads_id10").val()
    var ads_id11 = $("#ads_id11").val()
    var ads_id12 = $("#ads_id12").val()

    if (ads_id1 != "" && $.inArray('1', parr) >= 0) {
        ads_arr.push(ads_id1);
        var p1 = $("#position1").val();
        if (!p1 || p1 == "" || p1 == undefined) {
            alert("广告【1】的位置不能为空");
            return;
        }
        var ia1=$("#ads_interval1").val()
        if (!ia1 || ia1 == "" || ia1 == undefined) {
            alert("广告【1】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia1)
        position_arr.push(p1);
    } else if ($.inArray('1', parr) >= 0) {
        alert("广告【1】素材不能为空");
        return
    }

    if (ads_id2 != "" && $.inArray('2', parr) >= 0) {
        ads_arr.push(ads_id2);
        var p2 = $("#position2").val();
        if (!p2 || p2 == "" || p2 == undefined) {
            alert("广告【2】的位置不能为空");
            return;
        }
         var ia2=$("#ads_interval2").val()
        if (!ia2 || ia2 == "" || ia2 == undefined) {
            alert("广告【2】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia2)
        position_arr.push(p2);
    } else if ($.inArray('2', parr) >= 0) {
        alert("广告【2】素材不能为空");
        return
    }
    if (ads_id3 != "" && $.inArray('3', parr) >= 0) {
        ads_arr.push(ads_id3);
        var p3 = $("#position3").val();
        if (!p3 || p3 == "" || p3 == undefined) {
            alert("广告【3】的位置不能为空");
            return;
        }
          var ia3=$("#ads_interval3").val()
        if (!ia3 || ia3 == "" || ia3 == undefined) {
            alert("广告【3】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia3)
        position_arr.push(p3);
    } else if ($.inArray('3', parr) >= 0) {
        alert("广告【3】素材不能为空");
        return
    }
    if (ads_id4 != "" && $.inArray('4', parr) >= 0) {
        ads_arr.push(ads_id4);
        var p4 = $("#position4").val();
        if (!p4 || p4 == "" || p4 == undefined) {
            alert("广告【4】的位置不能为空");
            return;
        }
          var ia4=$("#ads_interval4").val()
        if (!ia4 || ia4 == "" || ia4 == undefined) {
            alert("广告【4】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia4)
        position_arr.push(p4);
    } else if ($.inArray('4', parr) >= 0) {
        alert("广告【4】素材不能为空");
    }

    if (ads_id5 != "" && $.inArray('5', parr) >= 0) {
        ads_arr.push(ads_id5);
        var p5 = $("#position5").val();
        if (!p5 || p5 == "" || p5 == undefined) {
            alert("广告【5】的位置不能为空");
            return;
        }
          var ia5=$("#ads_interval5").val()
        if (!ia5 || ia5 == "" || ia5 == undefined) {
            alert("广告【5】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia5)
        position_arr.push(p5);
    } else if ($.inArray('5', parr) >= 0) {
        alert("广告【5】素材不能为空");
        return
    }
    if (ads_id6 != "" && $.inArray('6', parr) >= 0) {
        ads_arr.push(ads_id6);
        var p6 = $("#position6").val();
        if (!p6 || p6 == "" || p6 == undefined) {
            alert("广告【6】的位置不能为空");
            return;
        }
          var ia6=$("#ads_interval6").val()
        if (!ia6 || ia6 == "" || ia6 == undefined) {
            alert("广告【6】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia6)
        position_arr.push(p6);
    } else if ($.inArray('6', parr) >= 0) {
        alert("广告【6】素材不能为空");
        return
    }

    if (ads_id7 != "" && $.inArray('7', parr) >= 0) {
        ads_arr.push(ads_id7);
        var p7 = $("#position7").val();
        if (!p7 || p7 == "" || p7 == undefined) {
            alert("广告【7】的位置不能为空");
            return;
        }
          var ia7=$("#ads_interval7").val()
        if (!ia7 || ia7 == "" || ia7 == undefined) {
            alert("广告【7】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia7)
        position_arr.push(p7);
    } else if ($.inArray('7', parr) >= 0) {
        alert("广告【7】素材不能为空");
        return
    }
    if (ads_id8 != "" && $.inArray('8', parr) >= 0) {
        ads_arr.push(ads_id8);
        var p8 = $("#position8").val();
        if (!p8 || p8 == "" || p8 == undefined) {
            alert("广告【8】的位置不能为空");
            return;
        }
          var ia8=$("#ads_interval8").val()
        if (!ia8 || ia8 == "" || ia8 == undefined) {
            alert("广告【8】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia8)
        position_arr.push(p8);
    } else if ($.inArray('8', parr) >= 0) {
        alert("广告【8】素材不能为空");
        return
    }

    if (ads_id9 != "" && $.inArray('9', parr) >= 0) {
        ads_arr.push(ads_id9);
        var p9 = $("#position9").val();
        if (!p9 || p9 == "" || p9 == undefined) {
            alert("广告【9】的位置不能为空");
            return;
        }
          var ia9=$("#ads_interval9").val()
        if (!ia9 || ia9 == "" || ia9 == undefined) {
            alert("广告【9】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia9)
        position_arr.push(p9);
    } else if ($.inArray('9', parr) >= 0) {
        alert("广告【9】素材不能为空");
        return
    }
    if (ads_id10 != "" && $.inArray('10', parr) >= 0) {
        ads_arr.push(ads_id10);
        var p10 = $("#position10").val();
        if (!p10 || p10 == "" || p10 == undefined) {
            alert("广告【10】的位置不能为空");
            return;
        }
          var ia10=$("#ads_interval10").val()
        if (!ia10 || ia10 == "" || ia10 == undefined) {
            alert("广告【10】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia10)
        position_arr.push(p10);
    } else if ($.inArray('10', parr) >= 0) {
        alert("广告【10】素材不能为空");
        return
    }
    if (ads_id11 != "" && $.inArray('11', parr) >= 0) {
        ads_arr.push(ads_id11);
        var p11 = $("#position11").val();
        if (!p11 || p11 == "" || p11 == undefined) {
            alert("广告【11】的位置不能为空");
            return;
        }
          var ia11=$("#ads_interval11").val()
        if (!ia11 || ia11 == "" || ia11 == undefined) {
            alert("广告【11】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia11)
        position_arr.push(p11);
    } else if ($.inArray('11', parr) >= 0) {
        alert("广告【11】素材不能为空");
        return
    }
    if (ads_id12 != "" && $.inArray('12', parr) >= 0) {
        ads_arr.push(ads_id12);
        var p12 = $("#position12").val();
        if (!p12 || p12 == "" || p12 == undefined) {
            alert("广告【12】的位置不能为空");
            return;
        }
          var ia12=$("#ads_interval12").val()
        if (!ia12 || ia12 == "" || ia12 == undefined) {
            alert("广告【12】的间隔值不能为空");
            return;
        }
        interval_arr.push(ia12)
        position_arr.push(p12);
    } else if ($.inArray('12', parr) >= 0) {
        alert("广告【12】素材不能为空");
        return
    }
    var ads_id = ads_arr.join(",");
    var position = position_arr.join(",");
    var ads_interval = interval_arr.join(",");

    if (ads_id == "" || position == "") {
        alert("广告位不能为空");
        return
    }
    if (interval_arr == "" || interval_arr == "") {
        alert("广告间隔不能为空");
        return
    }
    if (isRepeat(position_arr)) {
        alert("广告位重复")
        return;
    }

    var data = [];

    var num = $(":checkbox[name^='groupInfo']:checked")
    if (!num || num.length <= 0) {
        alert("请勾选需求等级复选框");
        return
    }


    var groupInfoA = $(":checkbox[name='groupinfoA']").is(":checked");
     groupInfoA = $("#groupInfoA").is(":checked");
    var groupInfoS = $(":checkbox[name='groupInfoS']").is(":checked");
    var groupInfoB = $(":checkbox[name='groupInfoB']").is(":checked");
    var groupInfoC = $(":checkbox[name='groupInfoC']").is(":checked");
    var groupInfoD = $(":checkbox[name='groupInfoD']").is(":checked");

    if (groupInfoS == true) {
        var need_name = package_name+"-"+need_names+"-S"
        var need_play_type = $(":radio[name='need_play_typeS']:checked").val()
        if (!need_play_type || need_play_type == "" || need_play_type == undefined) {
            alert("S级播放类型不能为空")
        }

        var d = {
            "ads_id": ads_id,
            "position": position,
            "description": package_name+"-"+need_names,
            "package_id": package_id,
            "need_play_type": need_play_type,
            "enable": enable,
            "need_name": need_name,
            "anchor_level": "S",
            "ads_interval": ads_interval
        }
        data.push(d);
    }
    if (groupInfoA == true) {
        var need_name = package_name+"-"+need_names+"-A"
        var need_play_type = $(":radio[name='need_play_typeA']:checked").val()
        if (!need_play_type || need_play_type == "" || need_play_type == undefined) {
            alert("A级播放类型不能为空")
        }

        var d = {
            "ads_id": ads_id,
            "position": position,
            "description": package_name+"-"+need_names,
            "package_id": package_id,
            "need_play_type": need_play_type,
            "enable": enable,
            "need_name": need_name,
            "anchor_level": "A",
            "ads_interval": ads_interval
        }
        data.push(d);
    }
    if (groupInfoB == true) {
        var need_name = package_name+"-"+need_names+"-B"
        var need_play_type = $(":radio[name='need_play_typeB']:checked").val()
        if (!need_play_type || need_play_type == "" || need_play_type == undefined) {
            alert("B级播放类型不能为空")
        }

        var d = {
            "ads_id": ads_id,
            "position": position,
            "description": package_name+"-"+need_names,
            "package_id": package_id,
            "enable": enable,
            "need_name": need_name,
            "need_play_type": need_play_type,
            "anchor_level": "B",
            "ads_interval": ads_interval
        }
        data.push(d);
    }
    if (groupInfoC == true) {
        var need_name = package_name+"-"+need_names+"-C"
        var need_play_type = $(":radio[name='need_play_typeC']:checked").val()
        if (!need_play_type || need_play_type == "" || need_play_type == undefined) {
            alert("C级播放类型不能为空")
        }

        var d = {
            "ads_id": ads_id,
            "position": position,
            "description": package_name+"-"+need_names,
            "package_id": package_id,
            "need_play_type": need_play_type,
            "enable": enable,
            "need_name": need_name,
            "anchor_level": "C",
            "ads_interval": ads_interval
        }
        data.push(d);
    }
    if (groupInfoD == true) {
        var need_name = package_name+"-"+need_names+"-D"
        var need_play_type = $(":radio[name='need_play_typeD']:checked").val()
        if (!need_play_type || need_play_type == "" || need_play_type == undefined) {
            alert("D级播放类型不能为空")
        }

        var d = {
            "ads_id": ads_id,
            "position": position,
            "description": package_name+"-"+need_names,
            "package_id": package_id,
            "need_play_type": need_play_type,
            "enable": enable,
            "need_name": need_name,
            "anchor_level": "D",
            "ads_interval": ads_interval
        }
        data.push(d);
    }

    if (data.length > 0) {
        $.ajax({
            type: "POST",
            url: "/needinfo/toadd",
            data: {"param": JSON.stringify(data),"ifrepait":ifrepait,"package_name":package_name},
            success: function (msg) {
                if (msg.code == 0) {
                    alert("批量创建需求成功");
                } else {
                    alert("批量创建需求失败," + msg.message);
                }
            },
            error: function () {
                alert("网络故障，批量创建需求失败");
            }
        });
    } else {
        alert("还没有选择任何等级复选框");
        return;
    }
}
