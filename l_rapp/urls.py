from django.urls import path
from l_rapp import views

app_name = 'l_rapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_ok/', views.register_ok, name='register_ok'),
    path('register_logic/', views.register_logic, name='register_logic'),
    path('login/', views.login, name='login'),
    path('login_logic/', views.logon_logic, name='login_logic'),
    path('out_l/', views.out_login, name='out_l'),
    path('email_or_phone/', views.email_phone_check, name='email_phone_check'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
    path('check_captcha/', views.check_captcha, name='check_captcha'),
]
