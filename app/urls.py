
from django.conf.urls import url

from app import views

urlpatterns = [
    # 首页
    url(r'^home/', views.home, name='home'),
    # 个人中心
    url(r'^mine/', views.mine, name='mine'),
    # 闪购超市
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.user_market, name='market_params'),

    # 添加购物车
    url(r'^addCart/', views.add_cart, name='addCart'),
    url(r'^subCart/', views.sub_cart, name='subCart'),

    # 购物车页面
    url(r'^cart/', views.cart, name='cart'),

    # 修改购物车中商品的选择情况
    url(r'^changeSelectStatus/', views.change_select_status, name='change_select_status'),

    # 下单
    url(r'^generateOrder/', views.generate_order, name='generate_order'),


]