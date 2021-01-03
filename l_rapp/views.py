from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from dataapp.models import TUser, TShoppingCart
import random, string
from l_rapp.captcha.image import ImageCaptcha
import hashlib
# Create your views here.


# 注册页面
def register(request):
    # 判断是否来自购物车的请求
    login_from_car = request.GET.get('login_from')
    if login_from_car:
        request.session['login_from_car'] = login_from_car
    return render(request, 'register.html')


# 注册成功页面
def register_ok(request):
    email_or_phone = request.GET.get('email_or_phone')
    # 明确变量，作用域泄露问题
    phone = None
    email = None
    if email_or_phone.isnumeric():
        phone = email_or_phone
    else:
        email = email_or_phone
    return render(request, 'register ok.html', {'phone': phone, 'email': email})


# 登录页面
def login(request):
    # 判断是否来自购物车的请求
    login_from_car = request.GET.get('login_from')
    if login_from_car:
        request.session['login_from_car'] = login_from_car
    return render(request, 'login.html')


# 注册逻辑
def register_logic(request):
    # 从前端获取到的手机或者邮箱
    email_or_phone = request.POST.get('email_or_phone')
    # 手机号
    phone = None
    # 邮箱
    email = None
    # 判断，如果是纯数字则是手机号
    if email_or_phone.isnumeric():
        phone = email_or_phone
    else:
        email = email_or_phone
    # 用户输入的密码
    password = request.POST.get('password')
    # 得到一个随机八位令牌
    token = random_seq8()
    # 拼接新密码
    re_joint = password + token
    # 生成唯一密码 ---- 系统加密后的密码
    re_password = hashlib.sha256(re_joint.encode()).hexdigest()
    # 从数据库中查找id最大的id
    max_user = TUser.objects.aggregate(id=Max("pk"))
    # 如果存在，是得到id，如果不存在默认从1000开始添加  字典的get方法 1000为默认值
    max_id = (max_user.get("id") + 1 if max_user.get("id") else 1000)
    # 向数据库中添加数据
    user = TUser.objects.create(id=max_id, phone=phone, email=email, password=re_password, token=token, user_password=password)
    # 添加登录状态
    request.session['login'] = 'ok'
    # session保存用户账户
    request.session['email_or_phone'] = email_or_phone

    # 创建用户的同时，创建其唯一的购物车
    # 从数据库中查找id最大的id
    max_cart = TShoppingCart.objects.aggregate(id=Max("pk"))
    # 如果存在，是得到id，如果不存在默认从1000开始添加  字典的get方法 1000为默认值
    max_cart_id = (max_cart.get("id") + 1 if max_cart.get("id") else 100)
    # 创建购物车
    t_cart = TShoppingCart.objects.create(id=max_cart_id, user_id=user)
    # 将购物车id存入session中,用于数据同步
    request.session['cart_id'] = t_cart.id
    return JsonResponse({'register': 'ok'})


# 登录逻辑判断
def logon_logic(request):
    email_or_phone = request.POST.get('email_or_phone')
    password = request.POST.get('password')
    autologin = request.POST.get('autologin')
    re_password = None
    # print(email_or_phone, password, autologin)
    if email_or_phone.isnumeric():
        token = TUser.objects.get(phone=email_or_phone).token
        re_joint = password + token
        re_password = hashlib.sha256(re_joint.encode()).hexdigest()
        user = TUser.objects.filter(phone=email_or_phone, password=re_password)
    else:
        token = TUser.objects.get(email=email_or_phone).token
        re_joint = password + token
        re_password = hashlib.sha256(re_joint.encode()).hexdigest()
        user = TUser.objects.filter(email=email_or_phone, password=re_password)
    print(email_or_phone, password, re_password)
    if user:
        request.session['login'] = 'ok'
        rst = JsonResponse({'login': 'ok'})
        request.session['email_or_phone'] = email_or_phone
        if autologin == 'true':
            rst.set_cookie('email_or_phone', email_or_phone, max_age=60*60*12*7)
            rst.set_cookie('password', re_password, max_age=60*60*12*7)
        return rst
    else:
        return JsonResponse({'login': 'fail'})


# 邮箱或手机号验证
def email_phone_check(request):
    email_or_phone = request.POST.get('email_or_phone')
    if email_or_phone.isnumeric():
        user = TUser.objects.filter(phone=email_or_phone)
    else:
        user = TUser.objects.filter(email=email_or_phone)

    if user:
        return JsonResponse({'email_or_phone': 'ok'})
    else:
        return JsonResponse({'email_or_phone': 'fail'})


# 验证码获取
def get_captcha(request):
    # 生成验证码captcha
    img = ImageCaptcha()
    # 生成码 随机码
    rst = random.sample(string.ascii_letters + string.digits, 5)
    print(rst)  # ['X', 's', '1', 'q', 'V']
    code = ''.join(rst)
    print(code)  # Xs1qV
    # 将当前验证码存入session中
    request.session['cur_captcha'] = code
    image = img.generate(code)  # 生成图片

    # 'image/png' 标识data的数据类型
    return HttpResponse(image, 'image/png')


# 验证码正确性检测
def check_captcha(request):
    # 得到系统生成的验证码
    cur_captcha = request.session.get('cur_captcha')
    # 得到用户输入的验证码
    input_captcha = request.GET.get('input_captcha')
    if cur_captcha.upper() == input_captcha.upper():
        return JsonResponse({'check_captcha': 'ok'})
    else:
        return JsonResponse({'check_captcha': 'fail'})


# 退出登录
def out_login(request):
    # 设置登录状态为未登录
    request.session['login'] = 'fail'
    # 将用户名置为None
    request.session['email_or_phone'] = None
    request.session['cart_id'] = None
    request.session['login_from_car'] = None
    request.session['login_from'] = None
    rst = JsonResponse({'submit': 'ok'})
    # rst = redirect('dataapp:index')
    rst.delete_cookie('email_or_phone')
    rst.delete_cookie('password')
    print('asdasdas')
    # 如果存在session购物车，将其清空，使即使退出也可使用购物车
    mycar = request.session.get('mycar')
    if mycar:
        mycar.clear_items()
        request.session['mycar'] = mycar
    # 中间件场景3的重构标志
    request.session['reload_data'] = 0
    # 返回到首页
    return rst



# 得到一个随机八位序列
def random_seq8():
    str1 = '1234567890abcbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 参数8位随机列表
    random_list = random.sample(str1, 8)
    # 拼接字符串
    random_str = ''
    for i in random_list:
        random_str += i
    return random_str