/**
 * Created by huozhihui on 17/1/24.
 */
  // 通过ajax方式提交表单
    function form_ajax() {
        var hosts = new Array()
        $('[id^=client_node_]').each(function () {
            if (this.checked) {
                hosts.push($(this).attr('ip'))
            }
        })
        if (hosts.length == 0) {
            alert("请选择客户端!");
            return;
        } else {
            $('[name=hosts]').val(hosts.join(','));
        }

        var flag = true;
        $('input:required').each(function () {
            input = $(this).val();
            if(input == ""){
                $(this).parent().append('<span class="red">必填项</span>');
                flag = false;
                return false;
            }else{
                span = $(this).parent().children('span').last();
                if(span.html() == "必填项"){
                    span.remove();
                }
            }
        })
        if(!flag){
            return;
        }
        // 隐藏结果显示列表
        $('#update_result').html('');
        // 显示 正在加载数据......
        reload_image();
        $("#mid").ajaxSubmit({
            type: 'post',
            success: function (response) {
                $('#update_result').html(response);
                reload_image()
            }
        })
    }

    // 显示/隐藏 正在加载......
    function reload_image() {
        $('#reload').toggleClass('hide');
    }


     // 显示隐藏字段
    function show_hidden_fields(flag) {
        if (flag) {
            $('#default_params').children('a').text('隐藏默认参数')
            $('#default_params').children('a').attr('onclick', 'show_hidden_fields(false); return false')
            set_fields_hide(false)
        }else{
            $('#default_params').children('a').text('查看默认参数')
            $('#default_params').children('a').attr('onclick', 'show_hidden_fields(true); return false')
            set_fields_hide(true)
        }
    }

    function set_fields_hide(hide) {
        for (var i = 0; i < hide_fields.length; i++) {
            element = 'label[for=' + hide_fields[i] + ']'
            if (hide) {
                $(element).parent().hide();
            } else {
                $(element).parent().show();
            }
        }
    }


      function set_fields(fields, flag) {
        for (var i = 0; i < fields.length; i++) {
            element = 'label[for=' + fields[i] + ']'
            if (flag=='hide') {
                $(element).parent().hide();
            }else{
                $(element).parent().show();
            }
        }
    }