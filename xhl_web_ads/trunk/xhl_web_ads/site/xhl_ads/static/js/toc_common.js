/*! ywl v1.0.1, (c)2016 eomsoft.net */
"use strict";

var LOG_LEVEL_DEBUG = 1;
var LOG_LEVEL_VERBOSE = 10;
var LOG_LEVEL_INFO = 20;
var LOG_LEVEL_WARN = 30;
var LOG_LEVEL_ERROR = 40;

var WITH_LOG_LEVEL = LOG_LEVEL_VERBOSE;
var WITH_LOG_TRACE = false;

var log = {};
if (window.console && LOG_LEVEL_ERROR >= WITH_LOG_LEVEL) {
	log.e = function () {
		console.error.apply(console, arguments);
		if(WITH_LOG_TRACE)
			console.trace();
	};
} else {
	log.e = function () {
	};
}
if (window.console && LOG_LEVEL_WARN >= WITH_LOG_LEVEL) {
	log.w = function () {
		console.warn.apply(console, arguments);
		if(WITH_LOG_TRACE)
			console.trace();
	};
} else {
	log.w = function () {
	}
}
if (window.console && LOG_LEVEL_INFO >= WITH_LOG_LEVEL) {
	log.i = function () {
		console.info.apply(console, arguments);
		if(WITH_LOG_TRACE)
			console.trace();
	};
} else {
	log.i = function () {
	}
}
if (window.console && LOG_LEVEL_VERBOSE >= WITH_LOG_LEVEL) {
	log.v = function () {
		console.log.apply(console, arguments);
		//if(WITH_LOG_TRACE)
		//	console.trace();
	};
} else {
	log.v = function () {
	}
}
if (window.console && LOG_LEVEL_DEBUG >= WITH_LOG_LEVEL) {
	log.d = function () {
		console.log.apply(console, arguments);
		//if(WITH_LOG_TRACE)
		//	console.trace();
	};
} else {
	log.d = function () {
	}
}
String.prototype.format=function()
{
  if(arguments.length==0) return this;
  for(var s=this, i=0; i<arguments.length; i++)
    s=s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);
  return s;
};

// 构造一个回调函数栈，遵循先进后出的原则进行调用。
var CALLBACK_STACK = {
	create: function () {
		var self = {};

		self.cb_stack = [];

		self.add = function (cb_func, cb_args) {
			if (!_.isFunction(cb_func)) {
				log.e('need callable function.');
			}
			cb_args = cb_args || {};
			self.cb_stack.push({func: cb_func, args: cb_args});
			return self;
		};

		self.exec = function (ex_args) {
			if (self.cb_stack.length > 0) {
				var cb = self.cb_stack.pop();
				var ex_ = ex_args || [];
				cb.func(self, cb.args, ex_);
			}
		};

		self.pop = function () {
			if (self.cb_stack.length == 0) {
				return null;
			} else {
				return self.cb_stack.pop();
			}
		};

		return self;
	}
};

if (!String.prototype.startsWith) {
	String.prototype.startsWith = function (searchString, position) {
		position = position || 0;
		return this.indexOf(searchString, position) === position;
	};
}

if (!String.prototype.realLength) {
	String.prototype.realLength = function () {
		var _len = 0;
		for (var i = 0; i < this.length; i++) {
			if (this.charCodeAt(i) > 255) _len += 2; else _len += 1;
		}
		return _len;
	};
}


function digital_precision(num, keep) {
	return Math.round(num * Math.pow(10, keep)) / Math.pow(10, keep);
}

function prefixInteger(num, length) {
    return (num / Math.pow(10, length)).toFixed(length).substr(2);
}

function size2str(size, precision) {
	precision = precision || 0;
	var s = 0;
	var k = '';
	if (size < KB) {
		s = size;
		k = 'B';
	}
	else if (size < MB) {
		s = digital_precision(size / KB, precision);
		k = 'KB'
	}
	else if (size < GB) {
		s = digital_precision(size / MB, precision);
		k = 'MB'
	}
	else if (size < TB) {
		s = digital_precision(size / GB, precision);
		k = 'GB'
	}
	else if (size < PB) {
		s = digital_precision(size / TB, precision);
		k = 'TB'
	}
	else {
		s = digital_precision(size / PB, precision);
		k = 'PB'
	}

	return '' + s + ' ' + k;
}

function second2str(sec) {
	var _ret = '';
	if (sec >= SECONDS_PER_DAY) {
		var _d = Math.floor(sec / SECONDS_PER_DAY);
		_ret = '' + _d + '天';
		sec = sec % SECONDS_PER_DAY;
	}

	if (sec >= SECONDS_PER_HOUR) {
		var _h = Math.floor(sec / SECONDS_PER_HOUR);
		_ret += '' + _h + '小时';
		sec = sec % SECONDS_PER_HOUR;
	} else if (_ret.length > 0) {
		_ret += '0小时';
	}

	if (sec >= SECONDS_PER_MINUTE) {
		var _m = Math.floor(sec / SECONDS_PER_MINUTE);
		_ret += '' + _m + '分';
		sec = sec % SECONDS_PER_MINUTE;
	} else if (_ret.length > 0) {
		_ret += '0分';
	}

	_ret += '' + sec + '秒';
	return _ret;
}

function get_cookie(name) {
	var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return r ? r[1] : undefined;
}

function utc_to_local(timestamp) {
	//console.log('utc_to_local:', timestamp);
	var d = new Date(timestamp * 1000);
	var _local = d.getTime() - (d.getTimezoneOffset() * 60000);
	return Math.round(_local / 1000);
}

function local_to_utc(timestamp) {
	var d = new Date(timestamp * 1000);
	var _utc = d.getTime() + (d.getTimezoneOffset() * 60000);
	return Math.round(_utc / 1000);
}
function format_datetime(timestamp) {
	var d = new Date(timestamp * 1000);
	//return '' + d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate() + ' ' + d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();

	var fmt = 'yyyy-MM-dd HH:mm:ss';
	var o = {
		"M+": d.getMonth() + 1, //月份
		"d+": d.getDate(), //日
		"H+": d.getHours(), //小时
		"m+": d.getMinutes(), //分
		"s+": d.getSeconds() //秒
		//"q+": Math.floor((this.getMonth() + 3) / 3), //季度
		//"S": d.getMilliseconds() //毫秒
	};

	if (/(y+)/.test(fmt)) {
		fmt = fmt.replace(RegExp.$1, (d.getFullYear() + "").substr(4 - RegExp.$1.length));
	}
	for (var k in o) {
		if (new RegExp("(" + k + ")").test(fmt)) {
			if(o.hasOwnProperty(k))
				fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
		}
	}
	return fmt;
}

var base64KeyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
function base64_encode(input) {
	var output = "";
	var chr1, chr2, chr3 = "";
	var enc1, enc2, enc3, enc4 = "";
	var i = 0;
	do {
		chr1 = input.charCodeAt(i++);
		chr2 = input.charCodeAt(i++);
		chr3 = input.charCodeAt(i++);
		enc1 = chr1 >> 2;
		enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
		enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
		enc4 = chr3 & 63;
		if (isNaN(chr2)) {
			enc3 = enc4 = 64;
		} else if (isNaN(chr3)) {
			enc4 = 64;
		}
		output = output + base64KeyStr.charAt(enc1) + base64KeyStr.charAt(enc2) + base64KeyStr.charAt(enc3) + base64KeyStr.charAt(enc4);
		chr1 = chr2 = chr3 = "";
		enc1 = enc2 = enc3 = enc4 = "";
	} while (i < input.length);
	return output;
}

function get_file_name(path) {
	var reg = /(\\+)/g;
	path = path.replace(reg, "/");
	var _path = path.split('/');
	return _path[_path.length - 1]
}

var g_unique_id = (new Date()).valueOf();
function generate_id() {
	return g_unique_id++;
}


function htmlEncode(_s) {
	if (_s.length == 0) return "";
	var s = _s.replace(/&/g, "&amp;");
	s = s.replace(/</g, "&lt;");
	s = s.replace(/>/g, "&gt;");
	//s = s.replace(/ /g, "&nbsp;");
	s = s.replace(/\'/g, "&#39;");
	s = s.replace(/\"/g, "&quot;");
	return s;
}
//
///*2.用正则表达式实现html解码*/
//function htmlDecode(_s) {
//	if (_s.length == 0) return "";
//	var s = str.replace(/&amp;/g, "&");
//	s = s.replace(/&lt;/g, "<");
//	s = s.replace(/&gt;/g, ">");
//	s = s.replace(/&nbsp;/g, " ");
//	s = s.replace(/&#39;/g, "\'");
//	s = s.replace(/&quot;/g, "\"");
//	return s;
//}
//时间戳序列
function get_fileName() {
    var myDate = new Date();
    var myYear = myDate.getYear();
    var myMonth = myDate.getMonth();
    var myHour = myDate.getHours();
    var myMinute = myDate.getMinutes();
    var mySecond = myDate.getSeconds();
	var fileName ="_"+myYear + myMonth + myHour + myMinute + mySecond
	return fileName
}

//生成uuid
function guid() {
    function S4() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+S4()+S4()+S4()+S4()+S4()+S4());
}

function getYearMonday() {
	var d = new Date();
	var formatedYear = ("0" + (d.getFullYear())).slice(-4);
	var formatedMonth = ("0" + (d.getMonth() + 1)).slice(-2);
	var formatedDay = ("0" + (d.getDate())).slice(-2);
	var str = ""+formatedYear+formatedMonth+formatedDay;
	return str

}
function getDate(num) {

	var d = new Date();
	if(num){
		    d.setDate(d.getDate() + num);//获取AddDayCount天后的日期
	}
	var formatedYear = ("0" + (d.getFullYear())).slice(-4);
	var formatedMonth = ("0" + (d.getMonth() + 1)).slice(-2);
	var formatedDay = ("0" + (d.getDate())).slice(-2);
	var str = ""+formatedYear+ "-"+formatedMonth+"-"+formatedDay;
	return str

}

function  getYearMonth(num) {
	var d = new Date();
	if(num){
		    d.setDate(d.getDate() + num);//获取AddDayCount天后的日期
	}
	var formatedYear = ("0" + (d.getFullYear())).slice(-4);
	var formatedMonth = ("0" + (d.getMonth() + 1)).slice(-2);
	var str = ""+formatedYear+ "-"+formatedMonth
	return str
}

function GetDateStr(AddDayCount) {
    var dd = new Date();
    dd.setDate(dd.getDate() + AddDayCount);//获取AddDayCount天后的日期
    var y = dd.getFullYear();
    var m = dd.getMonth() + 1;//获取当前月份的日期
    var d = dd.getDate();
    return y + "-" + m + "-" + d;
}

//判断数组是否重复包含
function isRepeat(arr) {
    var hash = {};
    for (var i in arr) {
        if (hash[arr[i]])
            return true;
        hash[arr[i]] = true;
    }
    return false;
}
function  getYMHS(str) {
    var d = new Date(str);
    var formatedMonth = ("0" + (d.getMonth() + 1)).slice(-2);
    var formatedDay = ("0" + (d.getDate())).slice(-2);
    var formatedHour = ("0" + (d.getHours())).slice(-2);
    var formatedSecond = ("0" + (d.getMinutes())).slice(-2);
    var str = "" + formatedMonth  + formatedDay  + formatedHour+formatedSecond;
    return str
}
function  getFormatDate(str) {
    var d = new Date(str);
    var formatedYear = ("0" + (d.getFullYear())).slice(-4);
    var formatedMonth = ("0" + (d.getMonth() + 1)).slice(-2);
    var formatedDay = ("0" + (d.getDate())).slice(-2);

	var str = ""+formatedYear+ "-"+formatedMonth+"-"+formatedDay;
    return str
}
//图片预览
function previewFile(that) {
    var file = that.files[0] // 获取input上传的图片数据;
    if (file) {
        var img = new Image();
        var url = window.URL.createObjectURL(file);
        $("#preview").attr("src", url);
    }
}


function isToday(str){
    var d = new Date(str);
    if(d == new Date()){
        return true;
    } else {
        return false;
    }
}


function flushschedule() {
    $.ajax({
        url: "/schedule/flush",
        type: 'get',
        success: function (data) {
           if(data.code==TPE_OK){
               alert('刷新成功');
           }else {
               alert("刷新失败"+data.message);
           }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert('网络故障，刷新失败');
        }
    });
}

function getRoominfo(that) {
	var source_link=$(that).attr("value");
	if(source_link=="null"||source_link==''){
	    alert("暂时无法获取直播间地址");
	    return;
    }
    window.open(source_link);
}

var process = (function () {
    var xhl = {}
    xhl.block_process = function (option) {
        var url_create = option.url_create;
        var url_select = option.url_select;
        var dom = option.dom_id
        var url = option.url
        var params = option.params
        var msg = option.msg
        var that = option.that;
        var t = null  //定时对象
        var playnum = null  //task编号
        $.get(url_create, function (ret) {
                $(dom).modal()
                playnum = ret.data
				params.playnum=playnum
                //step-2  定时获取文件上传进
                t = setInterval(function () {
                    $.get(url_select, {playnum: playnum}, function (ret) {
                            if (ret.code === TPE_OK) {
                                $(dom+' #process_data1').attr({value: ret.data["now"], max: ret.data["max"]}); //更新数据到进度条
                                $(dom+' #progress1').html(ret.data["now"] + "/" + ret.data["max"] + "     ");

                            } else {
                                ywl.notify_error('获取进度信息失败：' + ret.message);
                            }
                        }
                    );
                }, 200);
                that.attr("disbaled", 'disabled');
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: params,
                    dataType: "json",
                    success: function (ret) {

                            clearInterval(t);    //删除定时请求
                            if (ret.code === TPE_OK) {
                            	alert(msg + "成功");
                                host_table.reload();
                            }
                            else {
                                ywl.notify_error(msg + '失败：' + ret.message);
                            }
                            $(dom).modal('hide')
                            $(dom + ' #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                            $(dom + ' #progress1').html("0 bytes");

                            option.callback&&option.callback(ret)



                    },
                    error: function (xhr, errorText, errorStatus) {
                        clearInterval(t);    //删除定时请求
                        alert(msg + "失败");
                        $(dom).modal('hide')
                        $(dom+' #process_data1').attr({value: 0, max: 0}); //更新数据到进度条
                        $(dom+' #progress1').html("0 bytes");
                        ywl.notify_error('网络故障，' + msg + '未完成！');
                    }
                })
            }
        );
    }
    return xhl
})();

 function show_adsInfo(id) {
     $.get("/needinfo/getadsinfo?id="+id,function (ret) {

         $('#dialog-adsinfo-info #ads_name').val(ret.ads_name);
         $('#dialog-adsinfo-info #ads_contents').val(ret.ads_contents);
         $('#dialog-adsinfo-info #ads_time').val(ret.ads_time);
         $('#dialog-adsinfo-info #ads_materialurl').val(ret.ads_materialurl);
         var url = 'http://download.xiaohulu.com/obs/adsdownload/' + ret.ads_id + "/" + ret.ads_thumbnailurl
         var movieurl = 'http://download.xiaohulu.com/obs/adsdownload/' + ret.ads_id + "/" + ret.ads_materialurl
         $('#dialog-adsinfo-info #downMovieBt').attr("url", movieurl);
         $('#dialog-adsinfo-info #ads_thumbnailurl').attr("src", url);
         $("#dialog-adsinfo-info #preview").attr("src", "");
         $("#dialog-adsinfo-info").modal()

     })
    }
function isRealNum(val){
    // isNaN()函数 把空串 空格 以及NUll 按照0来处理 所以先去除
    if(val === "" || val ==null){
        return false;
    }
    if(!isNaN(val)){
        return true;
    }else{
        return false;
    }
}
