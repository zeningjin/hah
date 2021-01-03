from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import json

from businessapp.car import Car
from businessapp.order import Order
from dataapp.models import TUser, TBook, TShoppingCardCon, TOrder, TOrderDetail, TUserAddress, TShoppingCart
from datetime import datetime
import hashlib
from random import sample


# Create your views here.


# 购物车页面
def mycar(request):
    # # 模拟数据，模拟购物车
    # mycar = Car()
    # mycar.add_car(book_id=1, num=2)
    # mycar.add_car(book_id=2, num=1)
    # mycar.add_car(book_id=3, num=2)
    mycar = request.session.get('mycar')
    # request.session['mycar'] = mycar
    # items = mycar.get_items()
    # # 遍历得到每一本书的model及其数量
    # for per_item in items:
    #     print(per_item.book)
    #     print(per_item.book.book_name)
    #     print(per_item.num)
    return render(request, 'car.html', {'mycar': mycar})


# 添加商品数量
def add_item(request):
    # 获取session中的购物车
    mycar = request.session.get('mycar')
    # 获取登录态下的数据库中的购物车id
    cart_id = request.session.get('cart_id')
    print('购物车id为', cart_id)
    # 以下部分已在中间件中实现
    # 如果购物车不存在，则创建一个
    # if not mycar:
    #     mycar = Car()
    book_id = request.POST.get('book_id')
    book_num = request.POST.get('book_num')
    if book_num:
        try:
            # 传入的类型不能转化为整形时，则证明黑客攻击
            book_num = int(book_num)
            # 如果是负数，则改为1
            if book_num <= 0:
                raise ValueError
        except:
            book_num = 1
    print('mycar------', mycar)
    print('book_num----', book_num)
    # 如果没有传入数量，则默认为1
    if not book_num:
        book_num = 1
    # 向session购物车添加数据
    mycar.add_car(book_id=int(book_id), num=int(book_num))
    # 如果已登录（数据库有购物车表）
    if cart_id:
        # 修改数据库中数据
        alter_data_item(cart_id=cart_id, book_id=int(book_id), book_count=int(book_num))
    request.session['mycar'] = mycar
    return JsonResponse({'total_price': mycar.total_price, 'save_price': mycar.save_price, 'state': 'ok'})


# 减少商品数量
def reduce_item(request):
    # 获取session中的数据库
    mycar = request.session.get('mycar')
    # 获取登录态下的数据库中的购物车id
    cart_id = request.session.get('cart_id')
    # 获取书籍id
    book_id = request.POST.get('book_id')
    # 获取书籍数量
    book_num = request.POST.get('book_num')
    # 如果没有传入数量，则默认为1
    if not book_num:
        book_num = -1
    # 修改session数据库中数据
    mycar.add_car(book_id=int(book_id), num=int(book_num))
    # 如果已登录（数据库有购物车表）
    if cart_id:
        # 修改数据库中数据
        alter_data_item(cart_id=cart_id, book_id=book_id, book_count=book_num)
    # 更新session数据库数据
    request.session['mycar'] = mycar
    return JsonResponse({'total_price': mycar.total_price, 'save_price': mycar.save_price})


# 输入框中修改商品数量
def input_alter_item(request):
    # 获取session中的数据库
    mycar = request.session.get('mycar')
    # 获取登录态下的数据库中的购物车id
    cart_id = request.session.get('cart_id')
    # 获取书籍id
    book_id = request.POST.get('book_id')
    # 获取书籍数量
    book_num = request.POST.get('book_num')
    try:
        book_num = int(book_num)
        if book_num <= 0:
            raise ValueError
    except:
        # 防止非法输入
        book_num = 1
    # 修改session数据库的数量
    mycar.change_num(book_id=int(book_id), num=int(book_num))
    # 如果已登录（数据库有购物车表）
    if cart_id:
        # 修改数据库中数据
        alter_data_item(cart_id=cart_id, book_id=book_id, alter_type=False, book_count=book_num)
    # 更新session数据库数据
    request.session['mycar'] = mycar
    return JsonResponse({'total_price': mycar.total_price, 'save_price': mycar.save_price})


# 删除商品
def delete_item(request):
    # 得到购物车
    mycar = request.session.get('mycar')
    # 获取登录态下的数据库中的购物车id
    cart_id = request.session.get('cart_id')
    # 获取要删除的书的id
    book_id = request.GET.get('book_id')
    mycar.del_item(book_id=int(book_id))
    # 如果已登录
    if cart_id:
        car_item = TShoppingCardCon.objects.filter(shopping_id_id=int(cart_id), book_id_id=int(book_id))
        if car_item[0]:
            car_item[0].delete()
    # print(mycar.total_price, mycar.save_price)
    # 更新购物车
    request.session['mycar'] = mycar
    # for i in mycar.car_items:
    #     print(i.num)
    #     print(i.book.d_price)
    return JsonResponse({'total_price': mycar.total_price, 'save_price': mycar.save_price})


# 购物车中商品数量的修改
def alter_data_item(cart_id, book_id, book_count=1, alter_type=True):
    '''
    :param cart_id: 购物车id
    :param book_id: 书id
    :param alter_type: 修改类型： True ---> 使用相加类型, False ---> 使用直接替换数量类型
    :param book_count: 书数量 默认为1
    :return:
    '''
    item = TShoppingCardCon.objects.filter(shopping_id=cart_id, book_id=book_id)
    # 如果这本书存在，则更新对应的数量
    if item:
        this_item = item[0]
        if alter_type:
            this_item.book_count += book_count
        else:
            this_item.book_count = book_count
        # print(this_item.book_count)
        # print(this_item)
        this_item.save()
    # 如果不存在则添加该数据到数据库
    else:
        TShoppingCardCon.objects.create(shopping_id_id=cart_id, book_id_id=book_id, book_count=book_count)


# 检查提交订单视图
def indent_check(request):
    # 获取用户，查看是否登录
    email_or_phone = request.session.get('email_or_phone')
    # is语句的作用域泄露问题
    user = None
    if email_or_phone:
        if email_or_phone.isnumeric():
            user = TUser.objects.filter(phone=email_or_phone)
        else:
            user = TUser.objects.filter(email=email_or_phone)
    # ajax使用json序列化数组传入python为对应的列表传入的数据
    book_ids = request.POST.get('book_ids')
    print('book_ids=', book_ids)
    # 相当于检测来源的作用：1.能得到则是第一次提交；2.得不到则是由未登录转到登录态
    # 项目需求：由未登录转到登录态，当来源是订单时，登录后必须返回到订单页面
    if book_ids:
        # 防止用户从购物车-->点击提交--->未登录转到登录态--->那么此时book_ids是从Post得不到的
        # 将book_ids存入到session中，等由未登录转到登录态成功后
        book_ids = json.loads(book_ids)
        request.session['book_ids'] = book_ids
        print('第一次访问时的book_ids', book_ids)
    else:
        # 转到登录后从session中获取到book_ids
        book_ids = request.session.get('book_ids')
        print('从未登录状态转换过来的book_ids', book_ids)
    # 创建二次进入（从未登录转到登录）标志
    flag_enter = request.session.get('flag_enter')
    # 如果已登录
    if user:
        # 创建订单对象（与购物车类似，也可存到购物车中，因为可以是多个订单这里不存入）
        user_order = Order()
        # 订单的主键id并不是自增的需要手动添加
        # 从数据库中查找id最大的id, aggregate()得到的是字典，因为可以加多个参数a=Count("pk")等
        max_order = TOrder.objects.aggregate(id=Max("pk"))
        # 如果存在，是得到id，如果不存在默认从1000开始添加  字典的get方法 1000为默认值
        max_order_id = (max_order.get("id")+1 if max_order.get("id") else 1000)
        # 得到一个随机订单号
        order_number = get_date() + random_seq8()
        # 为了提交订单成功显示的订单号
        request.session['order_number'] = order_number
        # 创建数据库中的订单
        data_order = TOrder.objects.create(id=max_order_id, user_id=user[0], order_number=order_number)
        # 将选中的书添加到 订单对象中 并同步到数据库中
        for book_id in book_ids:
            # 得到对应的书
            book = TBook.objects.get(id=int(book_id))
            # 得到用户的购物车
            data_cart = TShoppingCart.objects.get(user_id=user[0])

            # 根据这本书查到对应购物车中的信息
            cart_con = TShoppingCardCon.objects.get(shopping_id=data_cart, book_id=book)
            # 根据购物车信息得到该本书的数量
            book_count = cart_con.book_count
            # 将这本书添加到订单中
            user_order.add_item(book_id=book_id, num=book_count)
            # 将这本书添加到数据库中的订单中  (从表的创建，外键要写主键order_id = model对象，或者使用order_id__id = 主键id)
            TOrderDetail.objects.create(order_id=data_order, book_id=book, book_count=book_count)
        # 将该订单对象存到session中
        request.session['user_order'] = user_order
        # 第一次提交订单
        if flag_enter == 1:
            # 只添加一次订单，防止用户重复刷新提交同一个订单，将标志改为2，注意控制数量
            flag_enter = 2
            # 将标志更新到session中
            request.session['flag_enter'] = flag_enter
            # 重定向到订单页面
            return redirect('businessapp:indent')
        # # 多次提交订单
        # elif flag_enter == 2:
        #     return redirect('businessapp:indent')
        else:
            return JsonResponse({'login': 'ok'})
    # 未登录
    else:
        request.session['flag_enter'] = 1
        request.session['login_from'] = 'order'
        return JsonResponse({'login': 'fail'})


# 订单页
def indent(request):
    # 得到订单对象
    user_order = request.session.get('user_order')
    # 得到用户地址
    # 获取用户，查看是否登录
    email_or_phone = request.session.get('email_or_phone')
    # is语句的作用域泄露问题
    user = None
    # 得到用户对象
    if email_or_phone:
        if email_or_phone.isnumeric():
            user = TUser.objects.filter(phone=email_or_phone)
        else:
            user = TUser.objects.filter(email=email_or_phone)
    address = TUserAddress.objects.filter(user_id=user[0])
    # 该用户常用地址id列表
    addressid_list = [i for i in address]
    return render(request, 'indent.html', {'user_order': user_order, 'addressid_list': addressid_list})


# 订单提交保存地址页
def save_address(request):
    # 获取当前订单号
    order_number = request.session.get('order_number')
    # 获取当前订单号提交次数
    get_order_number_count = request.session.get(order_number)
    # 若未提交
    if not get_order_number_count:
        # 设置当前订单号提交次数
        request.session[order_number] = 1
    else:
        # 已提交则不可重复提交
        return JsonResponse({'submit': 'fail'})
    # 寄给谁
    to_user = request.POST.get('to_user')
    # 详细地址
    detail_address = request.POST.get('detail_address')
    # 邮政编码
    post_code = request.POST.get('post_code')
    # 手机号
    phone = request.POST.get('phone')
    # 固定电话
    static_phone = request.POST.get('static_phone')
    # print(to_user, detail_address, post_code, phone, static_phone)
    # 获取用户，查看是否登录
    email_or_phone = request.session.get('email_or_phone')
    # is语句的作用域泄露问题
    user = None
    # 得到用户对象
    if email_or_phone:
        if email_or_phone.isnumeric():
            user = TUser.objects.filter(phone=email_or_phone)
        else:
            user = TUser.objects.filter(email=email_or_phone)
    # 数据库中添加该用户地址
    try:
        # 控制事务
        with transaction.atomic():
            # 先从数据库查找是否有该地址
            address = TUserAddress.objects.filter(detail_address=detail_address, user_id=user[0], zipcode=post_code, to_user=to_user, phone=phone, static_phone=static_phone)
            # print(address)
            # 如果没有则加入到数据库
            if not address:
                # 得到最大id的地址
                max_address = TUserAddress.objects.aggregate(id=Max("pk"))
                # 得到其id
                max_address_id = (max_address.get("id") + 1 if max_address.get("id") else 1000)
                # 向数据库中添加这个地址
                TUserAddress.objects.create(id=max_address_id, detail_address=detail_address, user_id=user[0], to_user=to_user, zipcode=post_code, phone=phone, static_phone=static_phone)
            return JsonResponse({'submit': 'ok'})
    except Exception as e:
        print(e)
        return JsonResponse({'submit': 'fail'})


# 订单提交成功页
def indent_ok(request):
    # session中的购物车
    mycar = request.session.get('mycar')
    # 订单书籍id列表
    book_ids = request.session.get('book_ids')
    # 清空session数据
    mycar = Car()
    # 获取用户，查看是否登录
    email_or_phone = request.session.get('email_or_phone')
    # is语句的作用域泄露问题
    user = None
    # 得到用户对象
    if email_or_phone:
        if email_or_phone.isnumeric():
            user = TUser.objects.filter(phone=email_or_phone)
        else:
            user = TUser.objects.filter(email=email_or_phone)
    # 获取购物车
    cart_data = TShoppingCart.objects.filter(user_id=user[0])
    # 获取购物车id
    cart_id = cart_data[0].id
    # 删除数据库中的订单提交成功后的书籍
    for book_id in book_ids:
        card_con = TShoppingCardCon.objects.filter(shopping_id_id=cart_id, book_id_id=book_id)
        if card_con:
            card_con[0].delete()
    # 将数据库中的数据反向重构session中的数据
    t_cart_items = TShoppingCardCon.objects.filter(shopping_id_id=cart_id)
    for per_data in t_cart_items:
        mycar.add_car(book_id=per_data.book_id.id, num=per_data.book_count)
    # 更新session
    request.session['mycar'] = mycar
    # 订单序号
    order_number = request.session.get('order_number')
    # 收件人
    to_user = request.GET.get('to_user')
    # 总价
    total_price = request.GET.get('total_price')
    return render(request, 'indent ok.html', {'order_number': order_number, 'to_user': to_user, 'total_price': total_price })


# 得到当前日期
def get_date():
    # 订单前缀
    order_number_pre = datetime.now().strftime('%Y%m%d')
    return order_number_pre


# 得到一个随机八位序列
def random_seq8():
    str1 = '1234567890abcbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 参数8位随机列表
    random_list = sample(str1, 8)
    # 拼接字符串
    random_str = ''
    for i in random_list:
        random_str += i
    return random_str