function loginAction() {
        var name=$("#user_name").val()
        var pwd=$("#user_pwd").val()
        var input_code=$("#input_code").val()
        $.post("/login", {
            "user_name":name,
            "user_pass":pwd,
            "input_code":input_code}
        ,function(result){
          if(result.code==0){
                  window.location = '/index'
          }else if (result.code==-1){
              alert("用户名或者密码错误")
              getRandomCodeAction()
          }else if (result.code==-2){
              alert("验证码错误")
              getRandomCodeAction()
          }
        }
    )
}

function getRandomCodeAction() {

        $.get("/get/RandomCode",
            function(result){
             $("#code").attr("src","data:image/png;base64,"+result)
        }
    )
}

function uploadPwd() {
         var raw_pwd=$("#raw_pwd").val()
         var pwd_first=$("#pwd_first").val()
         var pwd_second=$("#pwd_second").val()
         if(!raw_pwd||raw_pwd==""){
             alert("原始密码不能为空")
             return
         }
          if(!pwd_first||pwd_first==""){
             alert("新密码不能为空")
             return
         }
          if(!pwd_second||pwd_second==""){
             alert("确认密码不能为空")
             return
         }
         if(pwd_first!=pwd_second){
             alert("2次新密码不相同,请重新输入")
             $("#pwd_second").val("")
             $("#pwd_first").val("")
             return
         }

     $.ajax({
        url:'/pwd/update',
        type:'POST',
        data:{"raw_pwd": raw_pwd,
            "pwd_first": pwd_first,
            "pwd_second": pwd_second},
         dataType: 'json',
         success: function (ret) {
            if (ret.code === TPE_OK) {
                ywl.notify_success('密码更新成功！');
                window.location.href='/signout'
            } else {
                ywl.notify_error(ret.message);
            }
         },
         error: function(xhr,status,statusText){
            ywl.notify_error("网络故障");
        }
    });

}
    
    
