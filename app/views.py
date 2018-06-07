from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse


from app.models import MainWheel, MainNav, MainMustBuy, \
    MainShop, MainShow, FoodType, Goods, CartModel, \
    OrderModel, OrderGoodsModel

from user.models import UserTicketModel
from utils.functions import get_order_random_id


def home(request):
    '''
    首页视图函数
    '''
    if request.method == 'GET':

        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mainbuys = MainMustBuy.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()

        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainbuys': mainbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,
        }
        return render(request, 'home/home.html', data)


def mine(request):
    """
    个人中心
    """
    if request.method == 'GET':
        return render(request, 'mine/mine.html')


def market(request):
    if request.method == 'GET':

        return HttpResponseRedirect(reverse('axf:market_params', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    """
    :param typeid: 分类id
    :param cid:  子分类id
    :param sid: 排序id
    """
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if user_ticket:
            user = user_ticket.user
        else:
            user = ''

        foodtypes = FoodType.objects.all()
        # 获取某分类下的商品
        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)
        # 重新组装全部分类的参数
        # 组装结果为[['全部分类','0'], ['酒类':13550], ['饮用水':15431]]
        foodtypes_current = foodtypes.filter(typeid=typeid).first()
        if foodtypes_current:
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            chlid_list = []
            for childtypename in childtypenames:
                child_type_info = childtypename.split(':')
                chlid_list.append(child_type_info)

        # 排序
        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productnum')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')

        # 返回购物车信息
        if user:
            user_cart = CartModel.objects.filter(user=user)
        else:
            user_cart = ''

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'chlid_list': chlid_list,
            'cid': cid,
            'user_cart': user_cart
        }
        return render(request, 'market/market.html', data)


def add_cart(request):
    """
    添加购物车
    """
    if request.method == 'POST':

        user = request.user
        goods_id = request.POST.get('goods_id')
        # 判断用户是否是系统自带的anonymouseuser还是登陆的用户
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        if user.id:
            user_carts = CartModel.objects.filter(user=user,
                                                  goods_id=goods_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user=user,
                                         goods_id=goods_id)
                data['c_num'] = 1

            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '当前用户没有登陆，请去登陆'
        return JsonResponse(data)


def sub_cart(request):
    """
    减少购物车用户下单商品的数量
    """
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')

        if user.id:
            # 获取用户下单对应的商品信息
            user_carts = CartModel.objects.filter(user=user,
                                                  goods_id=goods_id).first()
            # 如果购物车中已经存在了商品信息
            if user_carts:
                if user_carts.c_num == 1:
                    # 直接删除购物车中的商品信息
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                return JsonResponse(data)
            data['c_num'] = 0
            return JsonResponse(data)

        data['msg'] = '当前用户没有登陆，请去登陆'
        data['code'] = 403
        return JsonResponse(data)


def cart(request):

    if request.method == 'GET':
        # 获取用户
        user = request.user
        # 查询购物车信息
        user_carts = CartModel.objects.filter(user=user)

        data = {
            'user_carts': user_carts
        }
        return render(request, 'cart/cart.html', data)


def change_select_status(request):
    if request.method == 'POST':

        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_select:
            cart.is_select = False
        else:
            cart.is_select = True
        cart.save()

        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select
        }
        return JsonResponse(data)


def generate_order(request):
    """
    下单
    """
    if request.method == 'GET':

        user = request.user
        # 创建订单
        o_num = get_order_random_id()
        order = OrderModel.objects.create(user=user, o_num=o_num)
        # 选择勾选的商品进行下单
        user_carts = CartModel.objects.filter(user=user, is_select=True)
        for carts in user_carts:
            # 创建商品和订单之间的关系
            OrderGoodsModel.objects.create(goods=carts.goods,
                                           order=order,
                                           goods_num=carts.c_num)
        user_carts.delete()

        return render(request, 'order/order_info.html', {'order': order})
