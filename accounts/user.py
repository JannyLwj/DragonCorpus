#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import LoginUserForm, ChangePasswordForm
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

# Create your views here.
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'Get' and request.GET.has_key('next'):
        next_page = request.GET['next']
    else:
        next_page = '/'
    if next_page == '/accounts/logout/':
        next_page = '/'
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)
    kwargs = {
        'request': request,
        'form': form,
        'next': next_page,
    }

    return render(request, 'accounts/login.html', kwargs)

@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
# @permission_verify()
def user_list(request):
    temp_name = "accounts/accounts-header.html"
    all_user = get_user_model().objects.all()
    kwargs = {
        'temp_name': temp_name,
        'all_user':  all_user,
    }
    return render(request, 'accounts/user_list.html', kwargs)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:logout'))
    else:
        form = ChangePasswordForm(user=request.user)
    kwargs = {
        'form': form,
        'request': request,
    }
    return render(request, 'accounts/change_password.html', kwargs)