

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
                count_price()
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
                count_price()
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


function change_order(order_id){

    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url:'/axf/changeOrderStatus/',
        type:'POST',
        data:{'order_id': order_id},
        dataType: 'json',
        headers:{'X-CSRFToken': csrf},
        success: function(msg){
            if(msg.code == '200'){
                location.href = '/axf/mine/'
            }
        },
        error:function(msg){
            alert('订单状态修改失败')
        }

    })
}


function all_select(i){
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/changeCartAllSelect/',
        type:'POST',
        data:{'all_select':i},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function(msg){
            if(msg.code == '200'){
                count_price()
                for(var i=0; i<msg.ids.length; i++){
                    if(msg.flag){
                        s= '<span onclick="cartchangeselect(' + msg.ids[i] + ')">x</span>'
                        $('#changeselect_'+ msg.ids[i]).html(s)

                        $('#all_select_id').attr({'onclick': 'all_select(1)'})
                        $('#select_id').html('√')
                    }else{
                        s= '<span onclick="cartchangeselect(' + msg.ids[i] + ')">√</span>'
                        $('#changeselect_'+ msg.ids[i]).html(s)

                        $('#all_select_id').attr({'onclick': 'all_select(0)'})
                        $('#select_id').html('x')
                    }
                }
            }
        },
        error:function(msg){
            alert('请求失败')
        }
    });
}

function count_price(){

    $.get('/axf/countPrice/', function(msg){
        if(msg.code == '200'){
            $('#count_price').html('总价:' + msg.count_price)
        }
    })
}

$.get('/axf/countPrice/', function(msg){
    if(msg.code == '200'){
        $('#count_price').html('总价:' + msg.count_price)
    }
})

