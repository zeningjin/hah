
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class TBook(models.Model):
    id = models.BigIntegerField(primary_key=True)
    book_name = models.CharField(max_length=30, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    publishing_house = models.CharField(max_length=30, blank=True, null=True)
    publishing_time = models.DateField(blank=True, null=True)
    edition = models.CharField(max_length=30, blank=True, null=True)
    print_time = models.DateField(blank=True, null=True)
    print_count = models.BigIntegerField(blank=True, null=True)
    comment_count = models.BigIntegerField(blank=True, null=True)
    sale_count = models.BigIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=30, blank=True, null=True)
    char_count = models.BigIntegerField(blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)
    format_size = models.IntegerField(blank=True, null=True)
    paper_type = models.CharField(max_length=30, blank=True, null=True)
    book_class = models.ForeignKey('TBookClass', models.DO_NOTHING, db_column='book_class', blank=True, null=True)
    wrap = models.CharField(max_length=30, blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    d_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    editor_commend = models.TextField(blank=True, null=True)
    content_intro = models.TextField(blank=True, null=True)
    book_intro = models.TextField(blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    cataloh = models.TextField(blank=True, null=True)
    media_comment = models.TextField(blank=True, null=True)
    book_pic = models.CharField(max_length=200, blank=True, null=True)
    content_all = models.TextField(blank=True, null=True)
    book_cover = models.CharField(max_length=200, blank=True, null=True)





class TBookClass(models.Model):
    id = models.BigIntegerField(primary_key=True)
    type_name = models.CharField(max_length=30, blank=True, null=True)
    parent_id = models.BigIntegerField(blank=True, null=True)




# 订单
class TOrder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.ForeignKey('TUser', models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    order_number = models.CharField(max_length=20, blank=True, null=True)




# 订单中间表
class TOrderDetail(models.Model):
    id = models.BigIntegerField(primary_key=True)
    order_id = models.ForeignKey(TOrder, models.DO_NOTHING, db_column='order_id')
    book_id = models.ForeignKey(TBook, models.DO_NOTHING, db_column='book_id')
    book_count = models.BigIntegerField(blank=True, null=True)




# 购物车中间表
class TShoppingCardCon(models.Model):
    id = models.BigIntegerField(primary_key=True)
    shopping_id = models.ForeignKey('TShoppingCart', models.DO_NOTHING, db_column='shopping_id')
    book_id = models.ForeignKey(TBook, models.DO_NOTHING, db_column='book_id')
    book_count = models.BigIntegerField(blank=True, null=True)




# 用户购物车
class TShoppingCart(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.ForeignKey('TUser', models.DO_NOTHING, db_column='user_id', blank=True, null=True)



# 用户
class TUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    token = models.CharField(max_length=30, blank=True, null=True)



# 用户收货地址
class TUserAddress(models.Model):
    id = models.BigIntegerField(primary_key=True)
    detail_address = models.CharField(max_length=300, blank=True, null=True)
    user_id = models.ForeignKey(TUser, models.DO_NOTHING, blank=True, null=True, db_column='user_id')
    name = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    to_user = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    static_phone = models.CharField(max_length=11, blank=True, null=True)

