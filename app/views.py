from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse


from app.models import MainWheel, MainNav, MainMustBuy, \
    MainShop, MainShow, FoodType, Goods


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

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'chlid_list': chlid_list,
            'cid':cid,
        }
        return render(request, 'market/market.html', data)


