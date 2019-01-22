<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<title>小葫芦广告后台</title>
	<link href="${ static_url('css/style.css') }" rel="stylesheet">
    <script type="text/javascript" src="${ static_url('plugins/jquery/jquery.min.js') }"></script>
    <script type="text/javascript" src="${ static_url('js/auth/login.js') }"></script>

</head>

<style>
.rc{
    display: flex;
    justify-content: space-between;
    text-align: center;
}

</style>

<body>
	<div class="login">
		<h2>小葫芦广告后台</h2>
		<p>请联系我们获取查看权限 bd@xiaohulu.com</p>


		<input type="text" placeholder="用户名" id="user_name">
		<input type="password" placeholder="密码" id="user_pwd">
        <div class="rc">
            <input type="text" placeholder="验证码" id="input_code" style="margin-left:97px;width: 179px;">
            <img id="code" src="" onclick="getRandomCodeAction()" style="margin-right: 102px;height: 30px;">
        </div>
		     <a href="javascript:;" onclick="loginAction()" style="margin: 0 auto 0;">登录</a>

    </div>
</body>

<script type="text/javascript">
        $(document).ready(function () {
            getRandomCodeAction()
        });

        $(function () {
            document.onkeydown = function (event) {
                var e = event || window.event || arguments.callee.caller.arguments[0];
                if (e && e.keyCode == 13) {
                    loginAction()
                }
            };
        });

</script>


</html>
