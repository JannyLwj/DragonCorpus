#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from accounts import user
from accounts import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^change_password/$', user.change_password, name='change_password'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
]
