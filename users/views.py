from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.


from HIS.models import User, Patient


def index(request):
    return render(request, 'users/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect("/users/index/")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            password = password.strip()
            try:  # 查询是否有该用户
                user = User.objects.get(username=username)
            except Exception:
                message = "该用户不存在!"
                return render(request, 'users/login.html', locals())
            if user.password != password:
                message = "密码不正确！"
                return render(request, 'users/login.html', locals())
            else:
                html = '''
                登录成功 点击<a href='/users/index/'>进入首页</a>
                '''
                # 设置session内部的字典内容
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session['user_attr'] = user.attr
                return HttpResponse(html)
        else:
            msssage = "请确保用户名和密码不为空"
            return render(request, 'users/login.html', locals())
    return render(request, 'users/login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        if not username:
            username_error = '请输入正确的用户名！'
            return render(request, 'users/register.html', locals())
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        attr = request.POST['attr']
        if password1 != password2:  # 判断两次密码是否相同
            password_error = "两次输入的密码不同！"
            return render(request, 'users/register.html', locals())
        try:  # 判断是否有相同用户名
            same_name_user = User.objects.get(username=username)
        except Exception:
            User.objects.create(username=username, password=password1, attr=attr)
            id = User.objects.get(username=username).id
            if int(attr) == 0:
                Patient.objects.create(id=id)
            return render(request, 'users/register_success.html')
        else:
            username_error = '该用户名已存在！'
            return render(request, 'users/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来未登录，也就没有登出
        return redirect("/index/")
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/users/index/')
