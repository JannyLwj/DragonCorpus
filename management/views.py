# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import zipfile

import rarfile
from django.db import connection
from audioop import reverse

import time

import MySQLdb
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
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
    project = rrt_project.objects.get(id=project_id)
    project_name = project.project_name

    cursor = connection.cursor()
    cursor.execute("select distinct d.id,d.domain_name from  "
                   "management_rrt_project_test_case as tc "
                   "join management_rrt_domain as d "
                   "where project_id_id=%s" %project_id)
    domain_list = cursor.fetchall()
    domain_result_lilst = list()
    for domain in domain_list:
        domain_dict = dict()
        domain_dict['id'] = domain[0]
        domain_dict['domain_name'] = domain[1]
        domain_result_lilst.append(domain_dict)

    domain_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('domain_id').distinct().count()
    intent_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('intent_id').distinct().count()
    utterance_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('utterance_id').distinct().count()
    slot_list_count = rrt_project_test_case.objects.filter(project_id=project_id).values('slot_id').distinct().count()

    context = {'project_name': project_name,
               'project_list': project_list,
               'testsuit_list':testsuit_list,
               'domain_list_count':domain_list_count,
               'intent_list_count':intent_list_count,
               'utterance_list_count':utterance_list_count,
               'slot_list_count':slot_list_count,
               'domain_list':domain_result_lilst
              }

    return render(request, 'management/project_overview_detail.html', context)


def project_overview_detail_table(request):
    """
        Show all test case
        Show status of testcase       """
    project_name=request.GET.get('project_name')
    filter_domain=request.GET.get('domain_list')[:-1].strip()
    filter_intent=request.GET.get('intent_list')[:-1].strip()

    domain_item = filter_domain.split(',')
    domain_string = list()
    for item in domain_item:
        if item:
            domain_string.append(int(item.encode('ascii')))

    intent_item = filter_intent.split(',')
    intent_string = list()
    for item in intent_item:
        if item:
            intent_string.append(int(item.encode('ascii')))

    project_id =rrt_project.objects.get(project_name=project_name).id
    startTimer = time.time()

    if domain_string and intent_string:
        project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id,domain_id__in=domain_string,intent_id__in=intent_string)
    elif domain_string and len(intent_string)<1:
        project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id,domain_id__in=domain_string)
    else:
        project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id_id=project_id)


    project_test_case_list = project_test_case_list_mid.select_related("utterance_id", "domain_id","intent_id","slot_id", "utterance_id__audio_id")

    project_test_output = list()
    for project_test in project_test_case_list:
        project_test_item = dict()
        project_test_item["utterance"] = project_test.utterance_id.utterance
        project_test_item["audio"] = project_test.utterance_id.audio_id.audio_path
        project_test_item["domain"] = project_test.domain_id.domain_name
        project_test_item["intent"] = project_test.intent_id.intent_name
        project_test_item["slotnames"] = project_test.slot_id.slot_names
        project_test_item["slotvalues"] = project_test.slot_id.slot_values
        project_test_output.append(project_test_item)

    print 'Elapsed time (sec) = ', time.time() - startTimer
    # json_result_list["total"] = len(project_test_output)
    # json_result_list["rows"] = project_test_output
    result = json.dumps(project_test_output)
    return HttpResponse(result)

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
            return HttpResponseRedirect(reverse('management:project_overview_detail', args=(1,)))


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

def utterance_table(request):
    """
        Show all test case
        Show status of testcase       """
    cursor = connection.cursor()
    cursor.execute("select p.project_name, ut.utterance, ut.dialog, ut.source, ut.gloable_priority "
                   "from management_rrt_project_test_case as tc "
                   "join management_rrt_project as p on tc.project_id_id=p.id "
                   "join management_rrt_utterance as ut on tc.utterance_id_id = ut.id;" )
    utterance_list = cursor.fetchall()
    utterance_test_output = list()
    for utterance_test in utterance_list:
        utterance_test_item = dict()
        utterance_test_item["utterance"] = utterance_test[1]
        utterance_test_item["dialog"] = utterance_test[2]
        utterance_test_item["source"] = utterance_test[3]
        utterance_test_item["priority"] = utterance_test[4]
        utterance_test_item["project"] = utterance_test[0]
        utterance_test_output.append(utterance_test_item)
    result = json.dumps(utterance_test_output)
    return HttpResponse(result)

def get_all_intent(request):
    """
    this is for Report feature
    get all Language info, so admin can filter the work_set
    :param request:
    :return:
    """
    filter_domain = request.GET.get('domain_id')

    domain_item = filter_domain.split(',')
    domain_string = list()
    for item in domain_item:
        if item:
            domain_string.append(int(item.encode('ascii')))

    if domain_string:
        project_name = request.GET.get('project_name')
        #找到domain_id
        project_id=rrt_project.objects.get(project_name=project_name).id

        project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id,domain_id__in=domain_string)
        project_test_case_list = project_test_case_list_mid.select_related( "intent_id")

        project_test_output = list()
        for project_test in project_test_case_list:
            project_test_item = dict()
            project_test_item["id"] = project_test.intent_id.id
            project_test_item["intent_name"] = project_test.intent_id.intent_name
            if project_test_item not in project_test_output:
                project_test_output.append(project_test_item)
        result = json.dumps(project_test_output)
    else:
        result=""
    return HttpResponse(result)

@csrf_exempt
def upload_hrl(request):
    try:
        upload_file=request.FILES.get('file')
        print upload_file.name
        if upload_file.name[-4:]==".rar":
            azip = rarfile.RarFile(upload_file)
        elif upload_file.name[-4:]==".zip":
            azip=zipfile.ZipFile(upload_file)
        else:
            return
        print (azip.namelist())
        azip.extractall("upload")



        # res_list=list()
        # return_dict=dict()
        # return_dict["result"]="success"
        # return_dict["test"] = "test"
        # res_list.append(return_dict)
        # result = json.dumps(res_list)
        HttpResponse("success")
    except:
        HttpResponse("error")

def put_hrl_into_database():
    hrl_path_folder = r"D:\database\FullTest1"
    for file in os.listdir(hrl_path_folder):
        hrl_file = os.path.join(hrl_path_folder, file)
        domain = file.split(".")[0]
        hrl_file_process = open(hrl_file, 'r')
        for line in hrl_file_process:
            if ".pcm" in line:
                line_string = line.strip().split("#")
                audio = line_string[1]
                speaker = line_string[2]
                gender = line_string[3]
                utterance = line_string[4]
                intent = line_string[5]
                try:
                    if len(line_string) > 6:
                        slot_names = line_string[6]
                        slot_values = line_string[7]
                    else:
                        slot_names = ""
                        slot_values = ""
                except:
                    slot_names = ""
                    slot_values = ""

                domain_list = models.rrt_domain.objects.filter(domain_name=domain)
                if len(domain_list) < 1:
                    domain_item = rrt_domain(domain_name=domain)
                    domain_item.save()

                intent_list = models.rrt_intent.objects.filter(intent_name=intent)
                if len(intent_list) < 1:
                    intent_item = rrt_intent(intent_name=intent)
                    intent_item.save()

                slot_list = models.rrt_slot.objects.filter(slot_names=slot_names, slot_values=slot_values)
                if len(slot_list) < 1:
                    slot_item = rrt_slot(slot_names=slot_names, slot_values=slot_values)
                    slot_item.save()

                audio_list = models.rrt_audio.objects.filter(audio_path=audio)
                if len(audio_list) < 1:
                    audio_item = rrt_audio(audio_path=audio, speaker=speaker, gender=gender)
                    audio_item.save()

                audio_id = rrt_audio.objects.get(audio_path=audio)

                utterance_list = models.rrt_utterance.objects.filter(utterance=utterance)
                if len(utterance_list) < 1:
                    utterance_item = rrt_utterance(utterance=utterance, audio_id=audio_id)
                    utterance_item.save()

                domain_id = models.rrt_domain.objects.get(domain_name=domain)
                intent_id = rrt_intent.objects.get(intent_name=intent)
                utterance_id = rrt_utterance.objects.get(utterance=utterance)
                slot_id = rrt_slot.objects.get(slot_names=slot_names, slot_values=slot_values)
                project_id = rrt_project.objects.get(project_name="EcarX")

                case_list = models.rrt_project_test_case.objects.filter(project_id=project_id, domain_id=domain_id,
                                                                        utterance_id=utterance_id,
                                                                        intent_id=intent_id, slot_id=slot_id)
                if len(case_list) < 1:
                    case_item = rrt_project_test_case(project_id=project_id, domain_id=domain_id,
                                                      utterance_id=utterance_id, intent_id=intent_id,
                                                      slot_id=slot_id)
                    case_item.save()