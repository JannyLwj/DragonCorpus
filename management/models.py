# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class rrt_project(models.Model):
    project_name = models.CharField('project_name', max_length=255)
    project_description = models.TextField('project_description')
    create_time = models.DateTimeField('create_time', default=timezone.now)
    modify_time = models.DateTimeField('modify_time', default=timezone.now)
    creater = models.CharField('creater', max_length=255, default='admin')

    def __str__(self):
        return self.project_name


class rrt_domain(models.Model):
    domain_name = models.CharField('domain_name', max_length=255)

    def __str__(self):
        return self.domain_name


class rrt_utterance(models.Model):
    utterance = models.CharField('utterance', max_length=255)
    source=models.CharField('source', max_length=255,default='QA')
    dialog=models.CharField('dialog', max_length=255,default='default')
    gloable_priority = models.IntegerField('gloable_priority', default=0)

    def __str__(self):
        return self.utterance

class rrt_audio(models.Model):
    audio_path = models.CharField('audio_path', max_length=255)
    audio_hrl_path=models.CharField('audio_hrl_path', max_length=255)
    speaker = models.CharField('speaker', max_length=255)
    gender = models.CharField('gender', max_length=255)
    age=models.IntegerField('age',default=18)
    utterance_id = models.ForeignKey(rrt_utterance)
    format = models.CharField('format', max_length=255,default=16*16)
    language=models.CharField('language', max_length=255,default="CMN")
    create_time = models.DateTimeField('create_time', default=timezone.now)

    def __str__(self):
        return self.audio_path


class rrt_intent(models.Model):
    intent_name = models.CharField('intent_name', max_length=255)
    default_select_utterance = models.IntegerField('max_select_utterance', default=10)
    intent_priority = models.IntegerField('min_select_utterance', default=1)

    def __str__(self):
        return self.intent_name


class rrt_testsuit(models.Model):
    testsuit_name = models.CharField('testsuit_name', max_length=255)
    create_time = models.DateTimeField('create_time', default=timezone.now)

    def __str__(self):
        return self.testsuit_name


class rrt_slot(models.Model):
    slot_names = models.CharField('slot_names', max_length=255)
    slot_values = models.CharField('slot_values', max_length=255)

    def __str__(self):
        return self.slot_names


class rrt_project_test_case(models.Model):
    case_priority = models.IntegerField('case_priority', default=0)
    select_times = models.IntegerField('select_times', default=0)
    select_flag = models.BooleanField('select flag', default=False)
    # ForeignKey
    project_id = models.ForeignKey(rrt_project)
    domain_id = models.ForeignKey(rrt_domain)
    utterance_id = models.ForeignKey(rrt_utterance)
    audio_id = models.ForeignKey(rrt_audio)
    intent_id = models.ForeignKey(rrt_intent)
    slot_id=models.ForeignKey(rrt_slot)


class rrt_testsuit_testcase(models.Model):
    testsuit_id=models.ForeignKey(rrt_testsuit)
    testcase_id = models.ForeignKey(rrt_project_test_case)


class rrt_baseline_test_case(models.Model):
    project_test_case_id = models.ForeignKey(rrt_project_test_case)
    utterance_id = models.ForeignKey(rrt_utterance)
    case_priority = models.IntegerField('baseline_case_priority', default=0)
    select_times = models.IntegerField('baseline_select_times', default=0)
    select_flag = models.BooleanField('baseline_select_flag', default=False)


class rrt_project_running_test_case(models.Model):
    baseline_test_case_id = models.ForeignKey(rrt_baseline_test_case)
    project_id = models.ForeignKey(rrt_project)
    domain_id = models.ForeignKey(rrt_domain)
    utterance_id = models.ForeignKey(rrt_utterance)
    intent_id = models.ForeignKey(rrt_intent)
    log_id = models.UUIDField('log_id')
    create_time = models.DateTimeField('running_testcase_create_time', default=timezone.now)
    testsuit_id = models.ForeignKey(rrt_testsuit)


