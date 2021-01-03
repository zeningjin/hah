from django.db.models import Max
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from businessapp.car import Car
from dataapp.models import TUser, TShoppingCart, TShoppingCardCon


# 自定义的中间件
class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("init1")

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        # 判断是否设置7天免登陆，只验证一次
        check_login = request.session.get('check_login')
        if not check_login:
            email_or_phone = request.COOKIES.get('email_or_phone')
            password = request.COOKIES.get('password')
            # 如果已登录
            if email_or_phone:
                # 即使设置了COOKIE也要检测密码的正确性，因为有可能修改密码
                if email_or_phone.isnumeric():
                    user = TUser.objects.filter(phone=email_or_phone, password=password)
                else:
                    user = TUser.objects.filter(email=email_or_phone, password=password)
                if user:
                    request.session['login'] = 'ok'
                    request.session['email_or_phone'] = email_or_phone
                    request.session['check_login'] = 1

        # 登陆页面拦截，已登录状态直接转到index主页
        if 'login' in request.path:
            email_or_phone = request.COOKIES.get('email_or_phone')
            if email_or_phone:
                request.session['login'] = 'ok'
                return redirect('dataapp:index')

        # 购物车的初始化
        if 'mycar' in request.path:
            # 获取session中的购物车
            mycar = request.session.get('mycar')
            # 获取用户，查看是否登录
            email_or_phone = request.session.get('email_or_phone')
            login_state = request.session.get('login')
            print(email_or_phone)
            print(login_state)
            user = None
            if email_or_phone:
                if email_or_phone.isnumeric():
                    user = TUser.objects.filter(phone=email_or_phone)
                else:
                    user = TUser.objects.filter(email=email_or_phone)
            # print(1, '------mycar------', mycar)
            # 如果用户登录了，就把cart_id存入session中，为了添加书籍使用
            if user:
                t_cart = TShoppingCart.objects.filter(user_id=user[0].id)
                request.session['cart_id'] = t_cart[0].id
            # 创建情景三的重构标志
            reload_data = request.session.get('reload_data')
            if not reload_data:
                reload_data = 0

            # 输出mycar 与 user 判断是否存在
            print(mycar, user)
            # 情景一：
            # 条件：第一次使用，用户登录状态，session购物车不存在
            # 操作：# 1.如果购物车不存在时，则创建购物车  ----> 简化到了用户注册中
            # 2.如果购物车存在，则将数据库购物车中数据同步到sessionm购物车
            if not mycar and user:
                print('情景一')
                # 创建session购物车对象
                mycar = Car()
                # 已登录状态
                # print(2, '-------user----', user)
                # 获取用户购物车
                t_cart = TShoppingCart.objects.filter(user_id=user[0].id)
                # print(3, '-----------t_cart---------', t_cart)
                # 如果存在，则将其中数据同步到session购物车中
                if t_cart:
                    # 获取购物车中物品
                    t_cart_items = TShoppingCardCon.objects.filter(shopping_id_id=t_cart[0].id)

                    # print(4, '----t_cart_items----', t_cart_items)
                    # 如果数据库中有数据，则将数据添加到session购物车中
                    if t_cart_items:
                        for per_item in t_cart_items:
                            # print(per_item.book_id_id,per_item.book_count)
                            # per_item.book_id_id = 从查主 ---  外键_主表属性
                            mycar.add_car(book_id=per_item.book_id_id, num=per_item.book_count)
                    # 将购物车id存入session中,用于数据同步
                    request.session['cart_id'] = t_cart[0].id
                    # 设置重构标志为1： 不重构
                    # 原因：一开始就登陆是不需要重构session和数据库数据的
                    request.session['reload_data'] = 1
                    # 若购物车不存在，创建购物车，在register注册过程中实现
                    # else:
                    #     # 从数据库中查找id最大的id
                    #     max_cart = TShoppingCart.objects.aggregate(id=Max("pk"))
                    #     # 如果存在，是得到id，如果不存在默认从1000开始添加  字典的get方法 1000为默认值
                    #     max_cart_id = max_cart.get("id", 1000) + 1
                    #     # 创建购物车
                    #     t_cart = TShoppingCart.objects.create(id=max_cart_id, user_id=user[0])
                    #     # 将购物车id存入session中,用于数据同步
                    #     request.session['cart_id'] = t_cart.id

            # 情景二：
            # 条件：用户未登录状态，session购物车不存在
            # 操作：创建session购物车
            elif not mycar and not user:
                print('情景二')
                # 创建session购物车对象
                mycar = Car()

            # 情景三：
            # 条件：用户先在未登录状态先进行操作，根据情景二创建的session购物车---->从未登录到登录状态
            # 操作：将session购物车中的数据同步到数据库中，并将此时的session购物车通过数据库中的数据重构
            # 注意：只进行重构一次所以写入标志reload_data：0.重构；1.已重构，跳过
            elif mycar and user and reload_data == 0:
                print('情景三')
                # 改变标志
                request.session['reload_data'] = 1
                # 获取用户购物车,及其id
                t_cart = TShoppingCart.objects.filter(user_id=user[0].id)[0]
                t_cart_id = t_cart.id
                # 将session数据库中的数据同步到数据库
                for per_item in mycar.car_items:
                    alter_data_item(cart_id=t_cart_id, book_id=per_item.book.id, book_count=per_item.num)
                    print('session数据库中的数据', per_item.book, per_item.num)
                # 将数据库中的数据反向重构session中的数据
                t_cart_items = TShoppingCardCon.objects.filter(shopping_id__id=t_cart_id)
                # 清空session购物车mycar
                mycar.clear_items()
                for per_data in t_cart_items:
                    mycar.add_car(book_id=per_data.book_id.id, num=per_data.book_count)

            # 同步session，是视图之间共享session中数据
            request.session['mycar'] = mycar
            for i in mycar.car_items:
                print('购物车中的物品', i.book, i.num)

        print("request:", request)

    # 在process_request之后View之前执行
    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print("view:", request, view_func, view_args, view_kwargs)

    # view执行之后，响应之前执行
    # def process_response(self, request, response):
    #     print("response:", request, response)
    #     return response  # 必须返回response

    # 如果View中抛出了异常
    # def process_exception(self, request, ex):  # View中出现异常时执行
    #     print("exception:", request, ex)


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
