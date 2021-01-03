from django.urls import path
from businessapp import views

app_name = 'businessapp'


urlpatterns = [
    path('mycar/', views.mycar, name='mycar'),
    path('mycar/add_item/', views.add_item, name='add_item'),
    path('mycar/reduce_item/', views.reduce_item, name='reduce_item'),
    path('mycar/delete_item/', views.delete_item, name='delete_item'),
    path('mycar/alter_item/', views.input_alter_item, name='alter_item'),
    path('indent/', views.indent, name='indent'),
    path('indent_ok/', views.indent_ok, name='indent_ok'),
    # 加mycar的原因是购物车有中间件判断的效果，为了订单能从购物车中拿到数据
    path('mycar/indent_check/', views.indent_check, name='indent_check'),
    path('save_address', views.save_address, name='save_address'),
]