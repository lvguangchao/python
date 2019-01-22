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
    
    
