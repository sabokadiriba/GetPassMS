from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class Usermodel(UserAdmin):
    list_display = ['first_name','user_type' ]


admin.site.register(CustomizedUser,Usermodel)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(GuestRequest)
admin.site.register(Badge)

