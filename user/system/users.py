from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib import auth
from user import models
import akshare as ak
import numpy as np


# Create your system here.


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == "GET":
        info = request.session.get('info')
        if info:
            # 如果用户已经登录，直接跳转到首页
            if info['is_login'] == 1:
                return redirect('/home/')
            # 用户未登录，请用户登录
            else:
                username = request.session.get('info')['username']
                username_checked = 'checked'
        else:
            username = ''
            username_checked = ''
        # GET请求，返回登陆页面
        return render(request, 'login.html', {'username': username, 'username_checked': username_checked})
    else:
        # POST请求，收到用户填写的登录信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_username = request.POST.get('remember_username')
        # 检验用户名与密码是否均输入
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': "用户名与密码不能为空"})
        # 检验密码是否正确
        user = models.UserInfo.objects.filter(username=username).first()
        if user is None:
            return render(request, 'login.html', {'errmsg': "该用户尚未注册，请先注册"})
        else:
            if user.password != password:
                return render(request, 'login.html', {'username': username, 'errmsg': "密码错误，请重新输入"})
        # if remember_username == 'on':
        #     # 记住用户名
        #     request.session["info"] = {'username': username,
        #                                'is_login': 1}
        # else:
        #     request.session.clear()
        request.session["info"] = {'username': username,
                                   'is_login': 1}
        return redirect('/home/')


def register(request):
    """
    新用户注册
    :param request:
    :return:
    """

    if request.method == "GET":
        # 返回注册页面
        return render(request, 'register.html')
    else:
        # 进行新用户注册
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")

        if password != password_again:
            return render(request, 'register.html', {'errmsg': "两次密码输入不同，请重新输入"})
        user = models.UserInfo.objects.filter(username=username).first()
        if user is not None:
            return render(request, 'register.html', {'errmsg': "用户名已存在，请更换用户名"})
        # 进行用户注册,将数据写入数据库
        info = models.UserInfo(username=username, password=password)
        info.save()
        return redirect('/login/')


def home(request):
    """
    打开系统主页
    :param request:
    :return:
    """
    info = request.session.get('info')
    if info['is_login'] == 1:
        return render(request, 'home.html', {'date': ak.option_sse_list_sina()})
    else:
        return redirect('/login/')


def change_code(request):
    """
    修改密码
    :param request:
    :return:
    """
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    new_password_again = request.POST.get('new_password_again')
    # 如果是GET请求，返回修改密码界面
    if request.method == "GET":
        return render(request, 'change_code.html')

    user = models.UserInfo.objects.filter(username=request.session.get("info")['username']).first()
    if user.password != old_password:
        # 原密码错误
        return render(request, 'change_code.html', {'errmsg': "原密码错误，请检查后重新输入"})
    if user.password == new_password:
        # 原密码与新密码相同
        return render(request, 'change_code.html', {'errmsg': "新密码不可与旧密码相同入"})
    if new_password != new_password_again:
        # 两次密码不同
        return render(request, 'change_code.html', {'errmsg': '两次输入密码不同，请检查后重新输入'})
    # 将旧密码改为新密码
    user.password = new_password
    user.save()
    request.session.clear()
    return redirect('/login/')


def account_info(request):
    """
    查看账户信息
    :param request:
    :return:
    """
    username = request.session.get('info')['username']
    info = models.FundAccount.objects.filter(username=username).first()
    position_info = models.Position.objects.filter(username=username)
    position_list = []
    for position in position_info:
        position_list.append(
            [position.option_code, position.option_name, position.position_volume, position.holding_cost,
             position.profit_loss, position.profit_loss_ratio, position.position_type])
    return render(request, 'account_info.html',
                  {'username': info.username, 'fund_account': info.fund_account, 'account_name': info.account_name,
                   'asset': info.asset, 'avail_funds': info.avail_funds, 'position_list': position_list})


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/login/')
