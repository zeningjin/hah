
import os,django

from django.db.models import Max

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdangwang2.settings")
django.setup()
import json
from dataapp.models import TShoppingCardCon, TShoppingCart, TUser, TBook, TOrder, TOrderDetail, TUserAddress

from businessapp.car import Car


# # 得到id=2的用户
# user = TUser.objects.filter(id=2)
# print(user)
# # 得到id=2的用户的购物车
# cart = TShoppingCart.objects.filter(user_id=user[0].id)
# print(cart)
# # 得到id=2的用户的购物车中的物品
# cart_con = TShoppingCardCon.objects.filter(shoppingh_id=cart[0].id)
# print(cart_con)
# print(len(cart_con))
# print(cart_con[0])
# for i in cart_con:
#     print(i)
# 添加物品
# TShoppingCardCon.objects.create(shoppingh_id=2, book_id=3, book_count=2)
# TShoppingCart.objects.create(id=3, user_id_id=3)

# 测试函数
# 数据库中购物车数据更新
# def alter_data_item(cart_id, book_id, book_count):
#     '''
#     :param cart_id: 购物车id
#     :param book_id: 书id
#     :param book_count: 书数量
#     :return:
#     '''
#     item = TShoppingCardCon.objects.filter(shopping_id=cart_id, book_id=book_id)
#     # 如果这本书存在，则更新对应的数量
#     if item:
#         this_item = item[0]
#         this_item.book_count += book_count
#         print(this_item.book_count)
#         print(this_item)
#         this_item.save()
#     else:
#         TShoppingCardCon.objects.create(shopping_id_id=cart_id, book_id_id=book_id, book_count=book_count)

# alter_data_item(1,1,1)
# # 修改数量
# a = TShoppingCardCon.objects.filter(shopping_id=1, book_id=1)[0]
# print(a)
# a.book_count = 2
# a.save()

# 添加一组数据
# TShoppingCardCon.objects.create(shopping_id_id=1, book_id_id=4, book_count=4)

# 删除一组数据
# TShoppingCardCon.objects.filter(shopping_id_id=2, book_id_id=4)[0].delete()

# 主从过滤查询
# cart_item = TShoppingCardCon.objects.filter(shopping_id_id=1)[0]
# cart = TShoppingCart.objects.filter(user_id=2)
# cart_items = TShoppingCardCon.objects.filter(shopping_id__id=cart[0].id)
# print(cart_item.book_id)
# print(cart)
# print(cart_items)


# 测试clear_items的容错性
# mycar = Car()
# mycar.add_car(1, 2)
# print(mycar.car_items, mycar.total_price, mycar.save_price)
# mycar.claer_items()
# print(mycar.car_items, mycar.total_price, mycar.save_price)


# 测试从查主的属性查看区别
# t_cart_items = TShoppingCardCon.objects.filter(shopping_id__id=1)
# for i in t_cart_items:
#     print(i.book_id,i.book_count)
#     print(i.book_id.id,i.book_count)

# TShoppingCardCon.objects.create(shopping_id=TShoppingCart.objects.get(id=6), book_id_id=1, book_count=4)


# 测试json.loads None 是否报错  --- 会报错 必须是str类型
# a = '[1,2,3,4]'
# c = '["a","b"]'
# d = '{"a":1,"b":2}'
# b = json.loads(d)
# print(b, type(b))

# max_cart = TOrder.objects.aggregate(id=Max("pk"))
# print(max_cart)

# # 测试QuerySet为空集是 not QuerySer<[]> 是否为真
# address = TUserAddress.objects.filter(id=1, phone=15035213142)
# if not address:
#     print(2)
# print(address)
# if address:
#     print(1)
# print(not address)

from datetime import datetime
import random
from random import sample


# def get_date():
#     # 订单前缀
#     order_number_pre = datetime.now().strftime('%Y%m%d')
#     print(order_number_pre)
#
# get_date()
#
#
# str1 = '1234567890abcbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# import math
# index = math.floor(random.random()*len(str1))
# print(index)
# print(str1[index])
#
# order_number_list = random.sample(str1, 8)
# order_number_end = ''
# for i in order_number_list:
#     order_number_end += i
# print(order_number_end)

import hashlib


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


random_str = random_seq8()
str2 = '20190102TYJy4Zgj'
random_str = '521314.gueicai' + 'wWDp9Rdo'
print(random_str)
h1 = hashlib.sha256(random_str.encode())
print('1------',hashlib.sha256(random_str.encode()).hexdigest())
print(type(h1.hexdigest()))
#
# print(len('4a675f1c697226a00949897120508a6cd06f018b88b88415c06e16287bc188c0'))



# max_order = TOrder.objects.aggregate(id=Max("pk"))
# print(max_order)
# print(max_order.get("id", 1000))