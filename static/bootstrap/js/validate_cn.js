/**
 * 验证
 */
jQuery.extend(jQuery.validator.messages, {
    required: "必填字段",
    remote: "请修正该字段",
    email: "请输入正确格式的电子邮件",
    url: "请输入合法的网址",
    date: "请输入合法的日期",
    dateISO: "请输入合法的日期 (ISO).",
    number: "请输入合法的数字",
    digits: "只能输入非负整数",  //正整数+0
    creditcard: "请输入合法的信用卡号",
    equalTo: "请再次输入相同的值",
    accept: "请输入拥有合法后缀名的字符串",  //输入拥有合法后缀名的字符串（上传文件的后缀）
    maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串"),
    minlength: $.validator.format("请输入一个长度最少是 {0} 的字符串"),
    rangelength: jQuery.validator.format("请输入一个长度介于 {0} 和 {1} 之间的字符串"),  //汉字算一个字符
    range: jQuery.validator.format("请输入一个介于 {0} 和 {1} 之间的值"),
    max: jQuery.validator.format("请输入一个最大为 {0} 的值"),
    min: jQuery.validator.format("请输入一个最小为 {0} 的值")
});

/**
 * 只能包含英文字母、数字、_和-
 */
jQuery.validator.addMethod("valid_letter_num", function (value, element) {
    var reg = /^[\d\a-zA-Z\_\-]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字、_和-");


/**
 * 通用名称验证规则：
 * 只能包含中文字符、英文字母、数字、_、-、.、（和）,且只能以字母或_或中文开头;其中括号可以为中英文的都可以
 */
jQuery.validator.addMethod("uecCommonNameCNwithPoint", function (value, element) {
    var reg = /^[\a-zA-Z\_\u4e00-\u9fa5]+[\d\a-zA-Z\u4e00-\u9fa5\_\-\(\)\（\）\.]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含中文字符、英文字母、数字、_、-、（和）,且只能以汉子字母或_开头");

/**
 * 通用名称验证规则：
 * 只能包含中文字符、英文字母、数字、_、-、（和）,且只能以字母或_或中文开头;其中括号可以为中英文的都可以
 */
jQuery.validator.addMethod("uecCommonNameCN", function (value, element) {
    var reg = /^[\a-zA-Z\_\u4e00-\u9fa5]+[\d\a-zA-Z\u4e00-\u9fa5\_\-\(\)\（\）]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含中文字符、英文字母、数字、_、-、（和）,且只能以汉子字母或_开头");

/**
 * 地域名称验证规则
 * 只能包含英文字母、数字、_和-,且只能以字母或_开头
 */
jQuery.validator.addMethod("uecCommonName", function (value, element) {
    var reg = /^[\a-zA-Z\_]+[\d\a-zA-Z\_\-]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字、_和-,且只能以字母或_开头");

/**
 * 云平台字符串基本验证规则
 * 只能包含英文字母、数字、_和-
 */
jQuery.validator.addMethod("uecCommonString", function (value, element) {
    var reg = /^[\d\a-zA-Z\_\-]*$/;
    return this.optional(element) || reg.test(value);
}, "只能包含英文字母、数字、_和-");

/**
 * 正整数
 */
jQuery.validator.addMethod("uecPositiveInteger", function (value, element) {
    var reg = /^[1-9]+[0-9]*$/;  //正整数
    return this.optional(element) || reg.test(value);
}, "只能是正整数");


//jQuery.validator.addMethod("uecName", function(value, element, params) { 
//	var length = value.length;
//	if(length < params[0] || length > params[1]){
//		return false;
//	}
//	var reg = /^[\d\a-zA-Z\u4e00-\u9fa5\_\-]*$/;    
//	return this.optional(element) || reg.test(value);
//}, jQuery.validator.format("名称只能为{0}到{1}长度的字符，并且只能为中文字符、数字、字母_和-"));  

/**
 * 邮政编码规则
 */
jQuery.validator.addMethod("uecZipCode", function (value, element) {
    var tel = /^[0-9]{6}$/;
    return this.optional(element) || (tel.test(value));
}, "请正确填写您的邮政编码");

/**
 * 手机号码验证
 */
jQuery.validator.addMethod("phone", function (value, element) {
    var reg = "/^1[3|4|5|8] \d{9}$/";
    return this.optional(element) || (reg.test(value));
}, "请正确输入您的手机号码");

//this one requires the text "buga", we define a default message, too
$.validator.addMethod("buga", function (value) {
    return value == "buga";
}, 'Please enter "buga"!');


// this one requires the value to be the same as the first parameter
$.validator.methods.equal = function (value, element, param) {
    return value == param;
};

//$.validator.addMethod("math", function(value, element, params) {
//  return this.optional(element) || value == params[0] + params[1];
//}, $.validator.format("Please enter the correct value for {0} + {1}"));

/*$(function(){
 $('.submit').click(function(){
 alert(123);
 $('label.error').append('<i class="fa fa-fw fa-exclamation-circle"></i>').css({
 'border':'1px solid #f00',
 });
 });
 });*/


//IP地址验证   
jQuery.validator.addMethod("ip", function (value, element) {
    return this.optional(element) || /^(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.)(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.){2}([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))$/.test(value);
}, "请填写正确的IP地址。");

