import os, django

from django.db.models import Max

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dangdangwang2.settings")
django.setup()

from dataapp.models import TUser,TShoppingCart

max_id = TUser.objects.filter(user_password__in=['a123456789','123456']).values()
# for id in max_id:
#     print(id)
# max_id = TUser.objects.get(user_password='123456')
print(max_id)
# app_item={}