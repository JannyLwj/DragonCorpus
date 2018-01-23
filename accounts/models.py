# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone

# Create your models here.
"""
user custom user admin system
"""


class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(PermissionList, blank=True)

    def __unicode__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        create a user
        :param email:
        :param username:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), username=username, last_login=timezone.now())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(RoleList, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        pass

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_lable):
        return True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

