#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from models import UserInfo, RoleList, PermissionList
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class LoginUserForm(forms.Form):
    email = forms.CharField(label='Email', error_messages={'required': 'email should not be empty'},
                            widget=forms.TextInput(attrs={'class': 'string email optional', 'size': 35}))
    password = forms.CharField(label='Password', error_messages={'required': 'password should not be empty'},
                               widget=forms.PasswordInput(attrs={'class': 'password optional', 'size': 35}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = auth.authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('email and password not matched !!!')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('this account has been forbit')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('password not correct')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserInfo
        fields = ('email', 'username', 'password')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('last_login',)}),
        ('Permissions', {'fields': ('is_superuser','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'last_login', 'password1', 'password2', 'is_superuser', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email', 'username')
    filter_horizontal = ()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Current Password',
                                   error_messages={'required': 'please input Current password'},
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', error_messages={'required': 'please input the new password'},
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='New Password Confirm',
                                    error_messages={'required': 'please input the new password again'},
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'current password incorrect')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError('New Password should be bit than 6 bit')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('password is not same with before')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordResetForm(PasswordResetForm):
    def end_email(slef, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        super.send_email(subject_template_name, email_template_name, context, from_email, to_email,
                         html_email_template_name)
