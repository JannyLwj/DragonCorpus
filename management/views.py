# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from audioop import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from management import models
from management.Forms import New_Project_Form, New_Testsuit_Form
from management.models import rrt_project, rrt_project_test_case, rrt_testsuit, rrt_slot, rrt_domain, rrt_audio, \
    rrt_intent, rrt_utterance


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def index(request):
    """
        Show all test case
        Show status of testcase
       """
    rrt_project_count = models.rrt_project.objects.all().count()
    rrt_utterance_count = models.rrt_utterance.objects.all().count()
    rrt_domain_count = models.rrt_domain.objects.all().count()
    rrt_intent_count = models.rrt_intent.objects.all().count()
    rrt_audio_count = models.rrt_audio.objects.all().count()
    rrt_testsuit_count = models.rrt_testsuit.objects.all().count()
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    context = {'rrt_project_count': rrt_project_count, 'rrt_utterance_count': rrt_utterance_count,
               'rrt_domain_count': rrt_domain_count,
               'rrt_intent_count': rrt_intent_count, 'rrt_audio_count': rrt_audio_count,
               'rrt_testsuit_count': rrt_testsuit_count,
               'project_list': project_list, 'testsuit_list': testsuit_list}

    return render(request, 'management/index.html', context)


def project_overview_detail(request, project_id):
    """
        Show all test case
        Show status of testcase       """
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    project_test_case_list = rrt_project_test_case.objects.filter(project_id_id=project_id)
    project = rrt_project.objects.get(id=project_id)
    project_name = project.project_name

    # begin
    domain_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('domain_id').distinct().count()
    intent_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('intent_id').distinct().count()
    intent_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('utterance_id').distinct().count()
    # slot_list_count = rrt_slot.objects.filter(project_id=project_id).values('utterance_id').distinct().count()

    context = {'project_name': project_name, 'project_test_case_list': project_test_case_list,
               'project_list': project_list, 'testsuit_list': testsuit_list}
    return render(request, 'management/project_overview_detail.html', context)


def testsuit_overview_detail(request, testsuit_id):
    """
        Show all test case
        Show status of testcase       """
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('create_time')
    testsuit_test_case_list = rrt_project_test_case.objects.filter(testsuit_id=testsuit_id)
    testsuit = rrt_testsuit.objects.get(id=testsuit_id)
    testsuit_name = testsuit.testsuit_name
    context = {'testsuit_name': testsuit_name, 'testsuit_test_case_list': testsuit_test_case_list,
               'project_list': project_list, 'testsuit_list': testsuit_list}
    return render(request, 'management/testsuit_overview_detail.html', context)


def new_project(request):
    form = None
    if request.method == 'GET':
        """
            Show all test case
            Show status of testcase
           """
        project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
        testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
        context = {'project_list': project_list, 'testsuit_list': testsuit_list}
        return render(request, 'management/new_project.html', context)

    elif request.method == 'POST':
        # hrl_path_folder=r"D:\database\FullTest1"
        # for file in os.listdir(hrl_path_folder):
        #     hrl_file=os.path.join(hrl_path_folder,file)
        #     domain=file.split(".")[0]
        #     hrl_file_process=open(hrl_file,'r')
        #     for line in hrl_file_process:
        #         if ".pcm" in line:
        #             line_string=line.strip().split("#")
        #             audio=line_string[1]
        #             speaker=line_string[2]
        #             gender = line_string[3]
        #             utterance= line_string[4]
        #             intent = line_string[5]
        #             if len(line_string)> 6:
        #                 slot_names=line_string[6]
        #                 slot_values = line_string[7]
        #             else:
        #                 slot_names = ""
        #                 slot_values = ""
        #
        #             domain_list=models.rrt_domain.objects.filter(domain_name=domain)
        #             if len(domain_list) < 1:
        #                 domain_item = rrt_domain(domain_name=domain)
        #                 domain_item.save()
        #
        #             intent_list = models.rrt_intent.objects.filter(intent_name=intent)
        #             if len(intent_list) < 1:
        #                 intent_item = rrt_intent(intent_name=intent)
        #                 intent_item.save()
        #
        #             slot_list = models.rrt_slot.objects.filter(slot_names=slot_names,slot_values=slot_values)
        #             if len(slot_list) < 1:
        #                 slot_item = rrt_slot(slot_names=slot_names,slot_values=slot_values)
        #                 slot_item.save()
        #
        #             audio_list = models.rrt_audio.objects.filter(audio_path=audio)
        #             if len(audio_list) < 1:
        #                 audio_item = rrt_audio(audio_path=audio,speaker=speaker,gender=gender)
        #                 audio_item.save()
        #
        #             audio_id = rrt_audio.objects.get(audio_path=audio)
        #
        #             utterance_list = models.rrt_utterance.objects.filter(utterance=utterance)
        #             if len(utterance_list) < 1:
        #                 utterance_item = rrt_utterance(utterance=utterance,audio_id=audio_id)
        #                 utterance_item.save()
        #
        #             domain_id=models.rrt_domain.objects.get(domain_name=domain)
        #             intent_id=rrt_intent.objects.get(intent_name=intent)
        #             utterance_id=rrt_utterance.objects.get(utterance=utterance)
        #             slot_id=rrt_slot.objects.get(slot_names=slot_names,slot_values=slot_values)
        #             project_id=rrt_project.objects.get(project_name="EcarX")
        #             case_item=rrt_project_test_case(project_id=project_id, domain_id = domain_id,utterance_id = utterance_id,intent_id = intent_id,slot_id=slot_id)
        #             case_item.save()



        form = New_Project_Form(request.POST)
        if form.is_valid():
            new_project_information = form.cleaned_data
            project_name = new_project_information['project_name']
            project_description = new_project_information['project_description']
            project_list = rrt_project.objects.filter(project_name=project_name)
            if len(project_list) < 1:
                project = rrt_project(project_name=project_name, project_description=project_description)
                project.save()
                return HttpResponseRedirect(reverse('management:project_overview_detail', args=(1,)))
            else:
                return HttpResponseRedirect(reverse('management:project_overview_detail', args=(1,)))

        else:
            # 弹出alert窗口
            # 弹出alert窗口
            print "error"


def new_testsuit(request):
    form = None
    if request.method == 'GET':
        """
            Show all test case
            Show status of testcase
           """
        project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
        testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
        context = {'project_list': project_list, 'testsuit_list': testsuit_list}
        return render(request, 'management/new_testsuit.html', context)

    elif request.method == 'POST':
        form = New_Testsuit_Form(request.POST)
        if form.is_valid():
            new_testsuit_information = form.cleaned_data
            testsuit_name = new_testsuit_information['testsuit_name']
            testsuit_list = rrt_testsuit.objects.filter(testsuit_name=testsuit_name)
            if len(testsuit_list) < 1:
                testsuit = rrt_testsuit(testsuit_name=testsuit_name)
                testsuit.save()
                return HttpResponseRedirect(reverse('management:testsuit_overview_detail', args=(1,)))
            else:
                return HttpResponseRedirect(reverse('management:testsuit_overview_detail', args=(1,)))

        else:
            # 弹出alert窗口
            # 弹出alert窗口
            print "error"


def utterance(request):
    """
        Show all test case
        Show status of testcase
       """
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    utterance_list = models.rrt_utterance.objects.all()
    context = {'utterance_list': utterance_list, 'project_list': project_list, 'testsuit_list': testsuit_list}

    return render(request, 'management/utterance.html', context)
