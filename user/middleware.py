from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class Md1(MiddlewareMixin):

    def process_request(self, request):
        # 登录页面和注册页面可以直接访问
        if request.path_info == '/login/' or request.path_info == '/register/':
            return
        # 如果有session，继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 如果没有session，返回登陆页面，并让其登录
        #return render(request, 'login.html', {'errmsg': '使用前请先登录'})
        return redirect('/login/')

    # def process_response(self, request, response):
    #     pass
