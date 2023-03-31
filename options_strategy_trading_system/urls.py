"""options_strategy_trading_system URL Configuration

The `urlpatterns` list routes URLs to system. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function system
    1. Add an import:  from my_app import system
    2. Add a URL to urlpatterns:  path('', system.home, name='home')
Class-based system
    1. Add an import:  from other_app.system import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.system import users, data_process, strategy, upload_info, profit

urlpatterns = [

    # 进入地址，返回主页
    path('', users.home),

    # 登录
    path('login/', users.login),

    # 注册
    path('register/', users.register),

    # 修改密码
    path('change_code/', users.change_code),

    # 查看账户信息
    path('account_info/', users.account_info),

    # 主页
    path('home/', users.home),

    # 登出
    path('logout/', users.logout),

    # 实时行情
    path('quotes/', data_process.quotes),
    path('quotes/<str:month>/', data_process.quotes_month),

    # 实时更新
    path('refresh/', data_process.refresh),


    # 策略生成
    path('strategy/', strategy.show),

    # 数据更新
    path('update/', upload_info.update),

    # 查看策略收益
    path('profit/',profit.show),

    # 确认交易成功
    path('success/', upload_info.update_strategy),

]
