

function addCart(goods_id){
//    $.get('/axf/addCart/?goods_id=' + goods_id, function(msg){
//        if(msg.code == 200){
//            $('#num_'+ goods_id).text(msg.c_num)
//        }else{
//            alert(msg.msg)
//        }
//    });
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/axf/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers:{'X-CSRFToken': csrf},
        success: function(msg){
            if(msg.code == 200){
                $('#num_'+ goods_id).text(msg.c_num)
            }else{
                alert(msg.msg)
            }
        },
        error: function(msg){
            alert('请求失败')
        }
    });
}


function subCart(goods_id){

    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url:'/axf/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function(data){
            if(data.code == '200'){
                $('#num_' + goods_id).html(data.c_num)
            }else{
                alert(data.msg)
            }
        },
        error: function(data){
            alert('请求失败')
        }
    });
}

function changeSelectStatus(cart_id){

//    $.post('/axf/changeSelectStatus/', function(data){
//        alert(data)
//        alert(data.is_select)
//    });
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url: '/axf/changeSelectStatus/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers:{'X-CSRFToken': csrf},
        success:function(data){
            if(data.code == '200'){
                if(data.is_select){
                    $('#cart_id_' + cart_id).html('√')
                }else{
                    $('#cart_id_' + cart_id).html('x')
                }
            }
        },
        error: function(data){
            alert('请求失败')
        }
    });
}