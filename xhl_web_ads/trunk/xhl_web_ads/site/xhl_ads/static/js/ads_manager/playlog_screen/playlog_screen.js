$("#btn-batch-edit-host").click(function () {
    $("#screen-batch-action")[0].reset();
    $("#dialog-screenbatch-info").modal();
});

$("#dialog-screenbatch-info #btn-save").click(function () {
     var screen_type=$(":radio[name='screen_type']:checked").val();
     if(!screen_type){
         alert('请选择需要替换内容');
         return
     }
     var play_ids=$("#dialog-screenbatch-info #play_ids").val();
     if(!play_ids){
         alert('请输入需要修改的play_id');
         return
     }
     play_ids=play_ids.replace(/，/g,",");

     var play_ids_arrary=play_ids.split(',');
     for(p in play_ids_arrary){
        if(!isRealNum(play_ids_arrary[p])){
            alert('play_id 内容不合法');
            return
        }
     }
    var data={screen_type:screen_type,play_ids:play_ids,edit_type:1};
     $.post('/playlog/screen/edit',data,function (ret) {
        if(ret.code==0){
            alert('批量替换成功');
            $("#dialog-screenbatch-info").modal('hide');
        }else {
            alert('批量替换失败');
        }
     });


});


$("#btn-edit-host").click(function () {
    $("#screen-action")[0].reset();
       $("#dialog-screen-info").modal();

});

$("#dialog-screen-info #btn-save").click(function () {

    var play_ids=$("#dialog-screen-info #play_ids").val();
    var screen_path=$("#dialog-screen-info #screen_path").val();
    var record_path=$("#dialog-screen-info #record_path").val();
    if(!play_ids){
          alert('请输入play_id');
           return
      }
    function _fn_sure() {
        var data = {screen_path: screen_path, play_ids: play_ids, edit_type: 2, record_path: record_path};
        $.post('/playlog/screen/edit', data, function (ret) {
            if (ret.code == 0) {
                alert('监播数据修改成功');
                $("#dialog-screen-info").modal('hide');
            } else {
                alert('监播数据修改失败');
            }
        });
    }
    if(!screen_path || !record_path){
         var cb_stack = CALLBACK_STACK.create();

        ywl.dlg_confirm(cb_stack, {
            msg: '<p>监播【视频】或【截图】为空，您确定要修改吗?！！</p>',
            fn_yes: _fn_sure
        });
    }else{
        _fn_sure();
    }




});

$("#dialog-screen-info #play_log_search").click(function () {
      var play_id=$("#dialog-screen-info #play_ids").val();
      if(!play_id){
          alert('请输入play_id');
           return
      }
       $.post('/playlog/find_by_id',{play_id:play_id},function (ret) {
        if(ret.code==0){
            $("#dialog-screen-info #screen_path").val(ret.data.screen_shot_path);
            $("#dialog-screen-info #record_path").val(ret.data.record_path);
        }else {
            alert('查询失败');
        }
     });

});
