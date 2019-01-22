/**
 * Created by minanqiang on 2017/8/10.
 */

var RANK = {
    getQueryString :function () {
        var str = location.search.length > 0 ? location.search.substring(1) : "";
        var items = str.length ? str.split("&") : [];

        var args = {}, item = null, name = null, value = null;

        for (var i = 0, len = items.length; i < len; i++) {
          item = items[i].split("=");
          name = decodeURIComponent(item[0]);
          value = decodeURIComponent(item[1]);
          if (name.length) {
              args[name] = value;
          }
        };

      return args;

    },
	create: function () {
		var self = {};
		// 页面主入口函数，每个页面加载完成后，调用此函数来传递页面参数
		self.init = function () {

		    $("#static_content").text("统计周期：08月11日-9月10日");
		    $("#intro_info").text("小葫芦广告后台");

		    var query_string = RANK.getQueryString();
            if (typeof query_string.key !== "undefined"){
               $("a.anchor_level") .removeClass("active");
            }
            else if (typeof query_string.key === "undefined" && typeof query_string.level === "undefined"){
               $("a.anchor_level") .removeClass("active");
               $("#ad_level_all").addClass("active");
            } else if(typeof query_string.level !== "undefined"){
                if(query_string.level === 'S'){
                    $("#ad_level_s").siblings().removeClass("active");
                    $("#ad_level_s").addClass("active");
                }else if(query_string.level === 'S_PLUS'){
                    $("#ad_level_s_plus").siblings().removeClass("active");
                    $("#ad_level_s_plus").addClass("active");
                }else if(query_string.level === 'A'){
                    $("#ad_level_a").siblings().removeClass("active");
                    $("#ad_level_a").addClass("active");
                }else if(query_string.level === 'B'){
                    $("#ad_level_b").siblings().removeClass("active");
                    $("#ad_level_b").addClass("active");
                }else if(query_string.level === 'C'){
                    $("#ad_level_c").siblings().removeClass("active");
                    $("#ad_level_c").addClass("active");
                }
            }

            $("#ad_level_all").click(function (){
		        window.location.href = '/index';
            });

            $("#ad_level_s_plus").click(function (){
		        window.location.href = '/index?level=S_PLUS';

            });
		    $("#ad_level_s").click(function (){
		        window.location.href = '/index?level=S';

            });
		    $("#ad_level_a").click(function (){

		        window.location.href = '/index?level=A';
		        // $(this).addClass("active").siblings().removeClass("active");
            });
            $("#ad_level_b").click(function (){
		        window.location.href = '/index?level=B';
		        // $(this).addClass("active").siblings().removeClass("active");
            });
            $("#ad_level_c").click(function (){
		        window.location.href = '/index?level=C';
		        // $(this).addClass("active").siblings().removeClass("active");
            })
            $("#anchor_search").click(function () {
                var key = $("#anchor_name").val();
                window.location.href = '/rank/getanchorbyname?key='+key;

            });
		};



		return self;
	}

};
var rank = RANK.create();