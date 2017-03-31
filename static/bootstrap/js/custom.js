/**
 * Created by huozhihui on 16/11/16.
 */
function change_active(obj) {
    $('#ul_tab').children().each(
        function () {
            // $(this).removeClass('active');
            $(this).addClass('activea');
        }
    )
}

function check_all() {
    $("#all").click(function () {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });
    // if ($('#all').prop('checked')) {
    //     $('[id^=client_node_]').each(function () {
    //         $(this).prop('checked', '')
    //     })
    // } else {
    //     $('[id^=client_node_]').each(function () {
    //         $(this).prop('checked', 'checked')
    //     })
    // }
}


// deploy_file/form.html用到

function write_file_code(st) {
    if (st == 'Python') {
        var s = "#!/usr/bin/python\n# -*- coding: utf-8 -*-\n";
    } else {
        var s = "#!/bin/bash\n";
    }
    $('#file_code').val(s)
}

// 弹出框
function show_dialog(url, data) {
    $.ajax({
        url: url,
        method: "get",
        data: data,
        success: function (response) {
            $('#update_div').html(response);
        }
    })
    ;
}

// 删除数据
function delete_date(url, th) {
    $.ajax({
        url: url,
        method: "get",
        success: function (response) {
            $(th).parents('tr').remove()
            $('div[role=alert]').removeClass('hidden');
            $('div[role=alert]').children('strong').text(response.msg);
        }
    });
}

// 验证名称唯一性
function check_uniq(field, url, submit_id) {
    console.log('check ' + field + ' uniq');
    element_id = 'id_' + field;
    element_uniq = $('#' + element_id);
    element_submit = $('#' + submit_id);
    element_uniq.on('input', function () {
        value = $(this).val();
        if (value != '') {
            $.ajax({
                url: url,
                method: "get",
                data: field + "=" + value,
                success: function (response) {
                    element_label_error = $('#' + element_id + '-uniq');
                    if (response.msg == '') {
                        if (element_label_error.length > 0) {
                            element_label_error.remove()
                        }
                        element_submit.prop('disabled', false);
                    } else {
                        if (element_label_error.length == 0) {
                            label = $('<label>', {
                                'id': element_id + '-uniq',
                                'class': 'red',
                                'for': element_id,
                                'text': response.msg,
                            });
                            element_uniq.after(label);
                        }
                        element_submit.prop('disabled', true);
                    }
                }
            })
        }
    })
}