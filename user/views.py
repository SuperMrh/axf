
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from user.models import UserModel, UserTicketModel

from utils.functions import get_ticket


def register(request):
    """
    注册
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')
        # 需要验证参数都不为空
        if not all([username, email, password, icon]):
            # 验证不通过，提示参数不能为空，返回页面错误提示
            msg = '参数不能为空'
            return render(request, 'user/user_register.html', {'msg': msg})
        # 加密password
        password = make_password(password)
        # 创建
        UserModel.objects.create(username=username,
                                 password=password,
                                 email=email,
                                 icon=icon
                                 )
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    """
    登录
    """
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户是否存在
        user = UserModel.objects.filter(username=username).first()
        if user:
            # 验证密码是否正确
            if check_password(password, user.password):
                # 1. 保存ticket在客户端
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('axf:mine'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 2. 保存ticket到服务端的user_ticket表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)

                return response
            else:
                msg = '密码错误'
                return render(request, 'user/user_login.html', {'msg': msg})
        else:
            msg = '用户不存在'
            return render(request, 'user/user_login.html', {'msg': msg})


def logout(request):
    """
    注销
    """
    if request.method == 'GET':
        # 注销，删除当前登录的用户的cookies中的ticket信息
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')

        return response
