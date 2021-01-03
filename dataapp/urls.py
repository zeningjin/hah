from django.urls import path
from dataapp import views

app_name = 'dataapp'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('bookdetail/', views.book_detail, name='bookdetail'),
    path('booklist/', views.book_list, name='booklist'),
    path('iframe_booklist/', views.iframe_booklist, name='iframe_booklist'),
    path('booklist_test/', views.booklist_test, name='booklist_test'),
]
