# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import hashlib
import os
import zipfile

import rarfile
import shutil
from django.db import connection
from audioop import reverse

import time

import MySQLdb
from django.http import Http404
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
    rrt_intent, rrt_utterance,rrt_testsuit_testcase


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

    user = request.user
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    testsuit_list_all= models.rrt_testsuit.objects.all().order_by('-create_time')
    project = rrt_project.objects.get(id=project_id)
    project_name = project.project_name

    domain_result_lilst = list()
    test_cast_mid=models.rrt_project_test_case.objects.filter(project_id=project_id)
    test_cast = test_cast_mid.select_related("domain_id")
    if len(test_cast)>1:
        for obj in test_cast:
            domain_dict = dict()
            domain_dict['id'] = obj.domain_id.id
            domain_dict['domain_name'] =obj.domain_id.domain_name
            if domain_dict not in domain_result_lilst:
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
               'domain_list':domain_result_lilst,
               'testsuit_list_all':testsuit_list_all,
               'user':user
              }

    return render(request, 'management/project_overview_detail.html', context)


def project_overview_detail_table(request,ids=[]):
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

    project_test_case_list = project_test_case_list_mid.select_related("utterance_id", "domain_id","intent_id","slot_id", "audio_id")

    project_test_output = list()
    for project_test in project_test_case_list:
        project_test_item = dict()
        project_test_item["id"] = project_test.id
        project_test_item["utterance"] = project_test.utterance_id.utterance
        project_test_item["audio"] = project_test.audio_id.audio_path
        project_test_item["domain"] = project_test.domain_id.domain_name
        project_test_item["intent"] = project_test.intent_id.intent_name
        project_test_item["slotnames"] = project_test.slot_id.slot_names
        project_test_item["slotvalues"] = project_test.slot_id.slot_values
        if str(project_test.id) in ids:
            project_test_item["state"] = True
        else:
            project_test_item["state"] = False
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
    user = request.user
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('create_time')[0:5]
    testsuit = rrt_testsuit.objects.get(id=testsuit_id)
    testsuit_test_case_list = models.rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit)
    testsuit_name = testsuit.testsuit_name

    domain_list = list()
    test_cast_mid = models.rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit)
    test_cast = test_cast_mid.select_related("testcase_id")
    if len(test_cast) > 1:
        for obj in test_cast:
            domain_dict = dict()
            domain_dict['id'] = obj.testcase_id.domain_id.id
            domain_dict['domain_name'] = obj.testcase_id.domain_id.domain_name
            if domain_dict not in domain_list:
                domain_list.append(domain_dict)

    context = {'testsuit_name': testsuit_name, 'testsuit_test_case_list': testsuit_test_case_list,
               'project_list': project_list, 'testsuit_list': testsuit_list,'domain_list':domain_list,'user':user}
    return render(request, 'management/testsuit_overview_detail.html', context)


def testsuit_overview_detail_table(request):
    """
        Show all test case
        Show status of testcase       """
    testsuit_name=request.GET.get('testsuit_name')
    testsuit_id=rrt_testsuit.objects.get(testsuit_name=testsuit_name)
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

    # project_id =rrt_project.objects.get(project_name=project_name)
    startTimer = time.time()

    if domain_string and intent_string:
        testsuit_test_case_list_mid = rrt_testsuit_testcase.objects.filter(project_id=project_id,domain_id__in=domain_string,intent_id__in=intent_string)
    elif domain_string and len(intent_string)<1:
        testsuit_test_case_list_mid = rrt_testsuit_testcase.objects.filter(project_id=project_id,domain_id__in=domain_string)
    else:
        testsuit_test_case_list_mid = rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit_id)

    testsuit_test_case_list = testsuit_test_case_list_mid.select_related("testcase_id")

    testsuit_test_output = list()
    for testsuit_test in testsuit_test_case_list:
        testsuit_test_item = dict()
        testsuit_test_item["id"] = testsuit_test.testcase_id.id
        testsuit_test_item["utterance"] = testsuit_test.testcase_id.utterance_id.utterance
        testsuit_test_item["audio"] = testsuit_test.testcase_id.audio_id.audio_path
        testsuit_test_item["domain"] = testsuit_test.testcase_id.domain_id.domain_name
        testsuit_test_item["intent"] = testsuit_test.testcase_id.intent_id.intent_name
        testsuit_test_item["slotnames"] = testsuit_test.testcase_id.slot_id.slot_names
        testsuit_test_item["slotvalues"] = testsuit_test.testcase_id.slot_id.slot_values
        testsuit_test_output.append(testsuit_test_item)

    print 'Elapsed time (sec) = ', time.time() - startTimer
    # json_result_list["total"] = len(project_test_output)
    # json_result_list["rows"] = project_test_output
    result = json.dumps(testsuit_test_output)
    return HttpResponse(result)


def new_project(request):
    form = None
    if request.method == 'GET':
        """
            Show all test case
            Show status of testcase
           """
        user = request.user
        project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
        testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
        context = {'project_list': project_list, 'testsuit_list': testsuit_list,'user':user}
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
                project_id = rrt_project.objects.get(project_name=project_name)
                return HttpResponseRedirect(reverse('management:project_overview_detail', args=(project_id.id,)))
            else:
                project_id = rrt_project.objects.get(project_name=project_name)
                return HttpResponseRedirect(reverse('management:project_overview_detail', args=(project_id.id,)))

        else:
            # 弹出alert窗口
            # 弹出alert窗口
            return render(request, 'management/error.html', {
                'error_message': "You didn't input valid project name.",
            })


def new_testsuit(request):
    form = None
    if request.method == 'GET':
        """
            Show all test case
            Show status of testcase
           """
        user = request.user
        project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
        testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
        context = {'project_list': project_list, 'testsuit_list': testsuit_list,'user':user}
        return render(request, 'management/new_testsuit.html', context)

    elif request.method == 'POST':
        testsuit_name = request.POST.get('testsuit_name')
        testcase_id_listtemp=request.POST.get('testcase_id_list')
        project_name=request.POST.get('project_name')
        exist_testsuit_name=request.POST.get('exist_testsuit_name')
        if testcase_id_listtemp=="":
            return render(request, 'management/error.html', {
                'error_message': "You didn't select test case",
            })
        if testsuit_name=="" and exist_testsuit_name=="":
            return render(request, 'management/error.html', {
                    'error_message': "You didn't input valid testsuit name",
                })
        elif testsuit_name=="":
            testsuit_name=exist_testsuit_name
        else:
            testsuit_name=project_name+"_"+ testsuit_name
        testcase_id_list=list()
        testcase_id_split=testcase_id_listtemp[:-1].strip().split(",")
        for id in testcase_id_split:
            testcase_id_list.append(id)

        testsuit_list = rrt_testsuit.objects.filter(testsuit_name=testsuit_name)
        if len(testsuit_list) < 1:
            testsuit = rrt_testsuit(testsuit_name=testsuit_name)
            testsuit.save()
            testsuit_id=rrt_testsuit.objects.get(testsuit_name=testsuit_name)
            for id in testcase_id_list:
                testcase_id=rrt_project_test_case.objects.get(id=id)
                testsuit_testcase_exist=rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit_id,testcase_id=testcase_id)
                if len(testsuit_testcase_exist)<1:
                    testsuit_testcase=rrt_testsuit_testcase(testsuit_id=testsuit_id,testcase_id=testcase_id)
                    testsuit_testcase.save()
                else:
                    continue
            return HttpResponseRedirect(reverse('management:testsuit_overview_detail', args=(testsuit_id.id,)))
        else:
            testsuit_id = rrt_testsuit.objects.get(testsuit_name=testsuit_name)
            for id in testcase_id_list:
                testcase_id = rrt_project_test_case.objects.get(id=id)
                testsuit_testcase_exist = rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit_id, testcase_id=testcase_id)
                if len(testsuit_testcase_exist) < 1:
                    testsuit_testcase = rrt_testsuit_testcase(testsuit_id=testsuit_id, testcase_id=testcase_id)
                    testsuit_testcase.save()
                else:
                    continue
            return HttpResponseRedirect(reverse('management:testsuit_overview_detail', args=(testsuit_id.id,)))


def utterance(request):
    """
        Show all test case
        Show status of testcase
       """
    user = request.user
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    utterance_list = models.rrt_utterance.objects.all()

    filter_project_list = models.rrt_project.objects.all()

    filter_list = list()
    for utterance in utterance_list:
        utterance_dict = dict()
        utterance_dict['source'] = utterance.source
        utterance_dict['dialog'] =utterance.dialog
        if utterance_dict not in filter_list:
            filter_list.append(utterance_dict)

    context = {'utterance_list': utterance_list, 'project_list': project_list, 'testsuit_list': testsuit_list,'filter_list':filter_list,'filter_project_list':filter_project_list,'user':user}

    return render(request, 'management/utterance.html', context)

def utterance_table(request):
    """
        Show all test case
        Show status of testcase       """
    project_id_list=request.GET.get('project_id_list')[:-1].strip()
    dialog_list = request.GET.get('dialog_list')[:-1].strip()
    source_list = request.GET.get('source_list')[:-1].strip()

    project_item = project_id_list.split(',')
    project_string=""
    for item in project_item:
        if item:
            project_string+=item+","
    project_string=project_string[:-1]

    dialog_item = dialog_list.split(',')
    dialog_string_list = list()
    for item in dialog_item:
        if item:
            dialog_string_list.append(item.strip())
    dialog_string=",".join(dialog_string_list)

    source_item = source_list.split(',')
    source_string_list = list()
    for item in source_item:
        if item:
            source_string_list.append(item.strip())
    source_string = ",".join(source_string_list)
    cursor = connection.cursor()
    where_sql = "where %s ;"
    sub_query = list()
    if project_string:
        sub_query.append( "p.id in (%s) " % project_string)
    if dialog_string:
        sub_query.append( "ut.dialog in ('%s') " % dialog_string)
    if source_string:
        sub_query.append("ut.source in ('%s') " % source_string)

    if not project_string and not dialog_string and not source_string:
        sql=""
    else:
        sql = where_sql % "and ".join(sub_query)

    sql_string="select distinct p.project_name, ut.utterance, ut.dialog, ut.source, ut.gloable_priority " \
               "from management_rrt_project_test_case as tc " \
               "join management_rrt_project as p on tc.project_id_id=p.id " \
               "join management_rrt_utterance as ut on tc.utterance_id_id = ut.id "+ sql

    cursor.execute(sql_string)

    utterance_list = cursor.fetchall()
    utterance_test_output = list()
    utterance_test_item = dict()
    utterance_test_output.append(utterance_test_item)
    for utterance_test in utterance_list:
        utterance_test_item = dict()
        utterance_test_item["utterance"] = utterance_test[1]
        utterance_test_item["dialog"] = utterance_test[2]
        utterance_test_item["source"] = utterance_test[3]
        utterance_test_item["priority"] = utterance_test[4]
        utterance_test_item["project"] = utterance_test[0]
        utterance_test_output.append(utterance_test_item)

    reduce_result = reduce(reduce_function, utterance_test_output)

    reduce_utterance_test_output = list()
    for key in reduce_result:
        reduce_utterance_test_item = dict()
        reduce_utterance_test_item["utterance"] = key[0]
        reduce_utterance_test_item["dialog"] = key[1]
        reduce_utterance_test_item["source"] = key[2]
        reduce_utterance_test_item["priority"] = key[3]
        reduce_utterance_test_item["project"] = reduce_result[key]
        reduce_utterance_test_output.append(reduce_utterance_test_item)

    result = json.dumps(reduce_utterance_test_output)
    return HttpResponse(result)

def reduce_function(x,y):
    key_list=(y["utterance"],y["dialog"],y["source"],y["priority"] )
    if key_list in x:
        x[key_list]+=","+y["project"]
    else:
        x[key_list]=y["project"]
    return x


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
        project_id=rrt_project.objects.get(project_name=project_name)

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

def get_testsuit_all_intent(request):
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
        testsuit_name=request.GET.get('testsuit_name')
        #找到domain_id
        testsuit_id=rrt_testsuit.objects.get(testsuit_name=testsuit_name)

        project_test_case_list_mid = rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit_id)
        project_test_case_list = project_test_case_list_mid.select_related( "testcase_id")

        project_test_output = list()
        for project_test in project_test_case_list:
            project_test_item = dict()
            project_test_item["id"] = project_test.testcase_id.intent_id.id
            project_test_item["intent_name"] = project_test.testcase_id.intent_id.intent_name
            if project_test_item not in project_test_output:
                project_test_output.append(project_test_item)
        result = json.dumps(project_test_output)
    else:
        result=""
    return HttpResponse(result)

def project_and_testsuit_overview_detail(request):
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    testsuit_list = models.rrt_testsuit.objects.all().order_by('-create_time')[0:5]
    project_list_all = models.rrt_project.objects.all().order_by('-modify_time')[:]
    testsuit_list_all = models.rrt_testsuit.objects.all().order_by('-create_time')[:]
    context = { 'project_list': project_list, 'testsuit_list': testsuit_list,
                'project_list_all': project_list_all, 'testsuit_list_all': testsuit_list_all }
    return render(request,'management/project_and_testsuit_overview_detail.html',context)

@csrf_exempt
def upload_hrl(request):
    try:
        upload_folder = r"./upload"
        try:
            shutil.rmtree(upload_folder)
        except:
            print "Delete upload folder failed"
        upload_file=request.FILES.get('file')
        project_name=request.POST.get('project_name')
        project_id=rrt_project.objects.get(project_name=project_name)
        print upload_file.name
        if upload_file.name[-4:]==".rar":
            azip = rarfile.RarFile(upload_file)
        elif upload_file.name[-4:]==".zip":
            azip=zipfile.ZipFile(upload_file)
        else:
            return "error"
        print (azip.namelist())
        azip.extractall("upload")

        audio_folder=r"./Audiofile"
        hrl_folder=r"./Hrlfile"

        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)
        if not os.path.exists(hrl_folder):
            os.makedirs(hrl_folder)

        put_hrl_into_database(audio_folder,hrl_folder,project_name)
        return HttpResponseRedirect(reverse('management:project_overview_detail', args=(project_id.id,)))
    except:
        shutil.rmtree(upload_folder)
        HttpResponse("error")

def error_page(request):
    return render(request, 'management/error.html')

def delete_testsuit(request):
    try:
        testsuit_name=request.GET.get("testsuit_name")
        testsuit_id=rrt_testsuit.objects.get(testsuit_name=testsuit_name)
        rrt_testsuit_testcase.objects.filter(testsuit_id=testsuit_id).delete()
        rrt_testsuit.objects.get(testsuit_name=testsuit_name).delete()
        return HttpResponse('success')
    except:
        return HttpResponse('failed')


def put_hrl_into_database(audio_folder,hrl_folder,project_name):
    upload_folder =r"./upload"
    for root, dirs, filenames in os.walk(upload_folder):
        for file in filenames:
            if os.path.splitext(file)[1] == '.hrl':
                hrl_file = os.path.join(root, file)
            else:
                continue
            #copy hrl to server
            domain=root.split("\\")[1].strip()

            server_hrl_folder=hrl_folder+"\\"+project_name
            if not os.path.exists(server_hrl_folder):
                os.makedirs(server_hrl_folder)

            hrl_target_file=hrl_file.replace(upload_folder,server_hrl_folder)
            domain_folder=os.path.dirname(hrl_target_file)
            if not os.path.exists(domain_folder):
                os.mkdir(domain_folder)
            shutil.copy(hrl_file,hrl_target_file)
            #analyze hrl file
            with open(hrl_file, 'r') as hrl_file_process:
                for line in hrl_file_process:
                    if ".pcm" in line or ".wav" in line:
                        line_string = line.strip().split("#")
                        audio_temp = line_string[1]
                        audio=audio_temp.replace('/','\\')

                        audio_target_path=os.path.join(audio_folder,audio)
                        upload_audio_path=os.path.join(root,audio)
                        audio_target_path_updated=process_audio_file(upload_audio_path, audio_target_path,domain, project_name)

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

                        utterance_list = models.rrt_utterance.objects.filter(utterance=utterance)
                        if len(utterance_list) < 1:
                                utterance_item = rrt_utterance(utterance=utterance)
                                utterance_item.save()

                        utterance_id = rrt_utterance.objects.get(utterance=utterance)
                        audio_list = models.rrt_audio.objects.filter(audio_path=audio_target_path_updated)
                        if len(audio_list) < 1:
                            audio_item = rrt_audio(audio_path=audio_target_path_updated, utterance_id=utterance_id,speaker=speaker, gender=gender,audio_hrl_path=audio_temp)
                            audio_item.save()

                        audio_id = rrt_audio.objects.get(audio_path=audio_target_path_updated)
                        domain_id = models.rrt_domain.objects.get(domain_name=domain)
                        intent_id = rrt_intent.objects.get(intent_name=intent)
                        utterance_id = rrt_utterance.objects.get(utterance=utterance)
                        slot_id = rrt_slot.objects.get(slot_names=slot_names, slot_values=slot_values)
                        project_id = rrt_project.objects.get(project_name=project_name)

                        case_list = models.rrt_project_test_case.objects.filter(project_id=project_id, domain_id=domain_id,
                                                                                utterance_id=utterance_id,
                                                                                intent_id=intent_id, slot_id=slot_id, audio_id=audio_id)
                        if len(case_list) < 1:
                            case_item = rrt_project_test_case(project_id=project_id, domain_id=domain_id,
                                                              utterance_id=utterance_id, intent_id=intent_id,
                                                              slot_id=slot_id, audio_id=audio_id)
                            case_item.save()
                    else:
                        continue
    try:
        shutil.rmtree(upload_folder)
    except:
        print "Delete upload file failed"


def process_audio_file(upload_audio_path, audio_target_path, domain,project_name):
    if os.path.exists(audio_target_path):
        if(md5(upload_audio_path) != md5(audio_target_path)):
           radom_string=random.randint(1,10000000)
           (filepath, tempfilename) = os.path.split(audio_target_path)
           (shotname, extension) = os.path.splitext(tempfilename)
           audio_name=project_name+"_"+domain+"_"+str(radom_string)+"_"+extension
           audio_target_path=os.path.join(filepath,audio_name)
           shutil.copy(upload_audio_path,audio_target_path)
           return audio_target_path
        else:
           return audio_target_path
    else:
        dir_path=os.path.dirname(audio_target_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if os.path.exists(upload_audio_path):
            shutil.copy(upload_audio_path, audio_target_path)
        else:
            audio_target_path=""
        return audio_target_path

def md5(file):
    md5_value = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(2048)
            if not data:
                break;
            md5_value.update(data)
    return md5_value.hexdigest()
#添加TestSuit
def add_testsuit(request):
    print request
    domain = list(request.GET.get('domain_list').split(','))
    intent = list(request.GET.get('intent_list').split(','))
    intent_ids=list()
    domain_ids=list()
    for item in domain:
        if item:
            domain_ids.append(int(item.encode('ascii')))
    for item in intent:
        if item:
            intent_ids.append(int(item.encode('ascii')))
    project_name = request.GET.get('project_name')
    randoms = bool(int(request.GET.get('random')))
    project_id = rrt_project.objects.get(project_name=project_name).id
    if domain_ids:
        if intent_ids:
            project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id, \
                                                                              domain_id__in=domain_ids, \
                                                                              intent_id__in= intent_ids)
        else:
            project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id,\
                                                                      domain_id__in=domain_ids,)
    else:
        project_test_case_list_mid = rrt_project_test_case.objects.filter(project_id=project_id,)
    project_test_case_list = project_test_case_list_mid.select_related("intent_id")
    project_test_output = list()#字典集合("intent_id:intent_id","id:case_id")
    for project_test in project_test_case_list:
        project_test_item = dict()
        project_test_item["id"] = project_test.id
        project_test_item["intent_id"] = project_test.intent_id.id
        if project_test_item not in project_test_output:
            project_test_output.append(project_test_item)
    project_test_output.sort(key=lambda k: (k.get('intent_id',0)))
    get_list_id=""
    get_intent_id=""
    before_list = list()#字典集合转化为字符串集合["intent_id case_id1 caseid2...","intent_id case_id1 case_id2...",...]
    for index,test in enumerate(project_test_output):
        if get_intent_id!=test.get('intent_id'):
            if get_list_id:
                before_list.append(get_list_id)
                get_list_id=""
            get_intent_id = test.get('intent_id')
            get_list_id+=str(get_intent_id)
        elif index==len(project_test_output)-1:
            get_list_id += " %s" % str(test.get("id"))
            before_list.append(get_list_id)
        get_list_id += " %s" % str(test.get("id"))
    after_list = list()
    if randoms:
        for caseid_intentid in before_list:
            caseid_intentid_arry = caseid_intentid.split(' ')
            intent_id = caseid_intentid_arry[0]
            random_times = rrt_intent.objects.get(id=intent_id).default_select_utterance
            case_ids = caseid_intentid_arry[1:]
            if len(case_ids)<= random_times:
                after_list.append(" ".join(case_ids))
            else:
                after_list.append(" ".join(random.sample(case_ids, random_times)))
    else:
        pass
    after_case_id = ""
    for array in after_list:
            after_case_id+=array
    return project_overview_detail_table(request,after_case_id.split(" "))


def delete_testsuit_item(request):
    print request
    testcase_ids = list(request.GET.get('testcase_id').split(','))
    testcase_id_list = list()
    for item in testcase_ids:
        if item:
            testcase_id_list.append(int(item.encode('ascii')))
    testsuit_name = request.GET.get('testsuit_name')
    testsuit_id = rrt_testsuit.objects.get(testsuit_name=testsuit_name).id
    cursor = connection.cursor()
    for testcase_id in testcase_id_list:
        sql_string = "DELETE FROM management_rrt_testsuit_testcase WHERE testcase_id_id = '%d' and testsuit_id_id='%d'" % (testcase_id,testsuit_id)
        cursor.execute(sql_string)
    return testsuit_overview_detail_table(request)

def download_testsuit(request):
    testsuit_name = request.GET.get('testsuit_name')
    testsuit_id = rrt_testsuit.objects.get(testsuit_name=testsuit_name).id
    testcase_id_list = rrt_testsuit_testcase.objects.filter(testsuit_id = testsuit_id).select_related("testcase_id")
    testcase_list = list()
    for testcase_id in testcase_id_list:
        testcase_list.append (rrt_project_test_case.objects.get(id=testcase_id.testcase_id_id))
    audio_path_list = list()
    #组装HRL文件并写入
    work_dir = os.getcwd()
    work_dir_last = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    os.makedirs(work_dir+"/download/%s"%work_dir_last)
    hrl_file_dir = work_dir +"/download/%s"%work_dir_last +"/"+"autohrl"+work_dir_last+'.hrl'
    hrl_file = open(hrl_file_dir,'w')
    hrl_file.write("#head;hrl;2.0;utf-8\n\
                   #ref#speechfile#speaker#gender#reference word sequence#topic#;slot names#;slot values\n\
                   head\n")
    for testcase in testcase_list:
        head_str = "ref#"
        audio_path_str = (testcase.audio_id.audio_path +"#").split('\\')[-1]
        audio_speaker_str = testcase.audio_id.speaker +"#"
        audio_gender_str = testcase.audio_id.gender +"#"
        atterance_name_str = testcase.utterance_id.utterance+"#"
        intent_str = testcase.intent_id.intent_name+"#"
        slot_name_str = testcase.slot_id.slot_names+"#"
        slot_value_str = testcase.slot_id.slot_values+"\n"
        writeline = head_str+audio_path_str+audio_speaker_str+audio_gender_str+atterance_name_str+intent_str+slot_name_str+slot_value_str
        hrl_file.write(writeline.encode('utf-8'))
        audio_path_list.append(audio_path_str[0:-1])
    hrl_file.close()
    #复制audio文件到打包的路径
    for audio_path in audio_path_list:
        pass
        #shutil.copy(work_dir+"/upload/Audiofile/"+audio_path,hrl_file_dir)
    #打包并传回文件路径
    zipfile_path = work_dir+"/download/"+work_dir_last
    zipfile_dir = list()
    for root, dirs, files in os.walk(zipfile_path):
        zipfile_dir.append(files)
    zipfile_my = zipfile.ZipFile(zipfile_path+"/"+work_dir_last+".rar",'w',zipfile.ZIP_DEFLATED)
    for file in files:
       # f.write(os.path.join(work_dir+"/download/"+work_dir_last+"/"+str(file)))
       zipfile_my.write(work_dir+"/download/"+work_dir_last+"/"+str(file),file)
    zipfile_my.close()
    #return HttpResponse(json.dumps(f.filename.replace('\\','/')))
    from django.http import FileResponse
    file = open(zipfile_my.filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="example.tar"'
    response['data']="{ }"
    global zip_data_file
    zip_data_file = zipfile_my.filename
    return HttpResponse(json.dumps(zipfile_my.filename.replace('\\','/')))
zip_data_file=""
def zip_download(request):
    from django.http import FileResponse
    file = open(zip_data_file,"rb")
    data = file.read()
    file.close()
    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="hrl_audiao.zip"'

    return response






