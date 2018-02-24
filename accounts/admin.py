# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserInfo
from .forms import UserAdmin
# Register your models here.


# class PermissionList_Admin(admin.ModelAdmin):
#     list_display = ('id','name','url')
#
# class RoleList_Admin(admin.ModelAdmin):
#     list_display = ('id','name')
#
# class UserInfo_Admin(admin.ModelAdmin):
#     list_display = ('id','password',"username",'email','is_active','is_superuser','role_id')
admin.site.register(UserInfo, UserAdmin)

# admin.site.register(PermissionList, PermissionList_Admin)
# admin.site.register(RoleList, RoleList_Admin)
# admin.site.register(UserInfo, UserInfo_Admin)
