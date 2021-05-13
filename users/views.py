from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import re
import datetime

# Create your views here.


from HIS.models import User, Patient


def index(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    elif request.session['is_login']:  # 如果已经登录，则直接跳转到登陆后首页
        return render(request, 'users/home.html')


def login(request):
    if not request.session.get('is_login', None):
        if request.method == 'GET':
            return render(request, 'users/login.html')
        if request.method == "POST":
            if request.session.get('is_login', None):  # 不允许重复登录
                return redirect("/users/home/")
            else:
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
                        # 设置session内部的字典内容
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        request.session['user_attr'] = user.attr
                        return render(request, 'users/home.html')
                else:
                    message = "请确保用户名和密码不为空"
                    return render(request, 'users/login.html', locals())
    elif request.session['is_login']:  # 如果已经登录，则直接跳转到登陆后首页
        return render(request, 'users/home.html')


def register(request):
    if not request.session.get('is_login', None):
        if request.method == 'GET':
            message = 'pat%06d' % (Patient.objects.all().count() + 1)
            return render(request, 'users/register.html', locals())
        elif request.method == 'POST':
            x = 1
            message = User.objects.all().count() + 1
            name = request.POST['name']
            gender = request.POST['gender']
            id_number = request.POST['id_number']
            phone = request.POST['phone']
            emergency_contact = request.POST['emergency_contact']
            address = request.POST['address']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            p1 = r"^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
            if not re.match(p1, id_number):  # 判断身份证号格式是否正确
                x = 0
                message1 = '请输入正确的身份证号！'
            p2 = r"^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$"
            if not re.match(p2, phone):  # 判断手机号格式是否正确
                x = 0
                message2 = '请输入正确的手机号！'
            if not re.match(p2, emergency_contact):  # 判断手机号格式是否正确
                x = 0
                message3 = '请输入正确的手机号！'
            if not username:  # 判断是否输入用户名
                x = 0
                message4 = '请输入用户名！'
            if password1 != password2:  # 判断两次密码是否相同
                x = 0
                message5 = "两次输入的密码不同！"
            try:  # 判断是否有相同用户名
                same_name_user = User.objects.get(username=username)
            except Exception:
                if x == 1:
                    id = 'pat%06d' % (Patient.objects.all().count() + 1)
                    User.objects.create(id=id, username=username, password=password1, attr=0)
                    age = datetime.datetime.today().year - int(id_number[6:10])
                    Patient.objects.create(
                        id=id,
                        name=name,
                        gender=gender,
                        age=age,
                        id_number=id_number,
                        phone=phone,
                        emergency_contact=emergency_contact,
                        address=address
                    )
                    message = '恭喜你注册成功！'
                    return render(request, 'users/register.html', locals())
                else:
                    return render(request, 'users/register.html', locals())
            else:
                message4 = '该用户名已存在！'
                return render(request, 'users/register.html', locals())
    elif request.session['is_login']:  # 如果已经登录，则直接跳转到登陆后首页
        return render(request, 'users/home.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来未登录，也就没有登出
        raise Http404('未登录')
    request.session.flush()
    # flush会一次性清空session中所有内容，可以使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('http://127.0.0.1:8000/')


def home(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
        # return HttpResponse('未登录')
    elif request.session['is_login']:
        return render(request, 'users/home.html')
