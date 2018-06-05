
from django.shortcuts import render

from app.models import MainWheel, MainNav, MainMustBuy, \
    MainShop, MainShow


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

    if request.method == 'GET':

        return render(request, 'mine/mine.html')