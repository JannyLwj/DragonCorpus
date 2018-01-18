# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
from management.Forms import New_Project_Form
from management.models import rrt_project, rrt_project_test_case


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
    rrt_project_count=models.rrt_project.objects.all().count()
    rrt_utterance_count=models.rrt_utterance.objects.all().count()
    rrt_domain_count=models.rrt_domain.objects.all().count()
    rrt_intent_count=models.rrt_intent.objects.all().count()
    rrt_audio_count=models.rrt_audio.objects.all().count()
    rrt_testsuit_count=models.rrt_testsuit.objects.all().count()
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    context={'rrt_project_count': rrt_project_count, 'rrt_utterance_count': rrt_utterance_count,'rrt_domain_count':rrt_domain_count,
                   'rrt_intent_count':rrt_intent_count,'rrt_audio_count':rrt_audio_count,'rrt_testsuit_count':rrt_testsuit_count,
                   'project_list': project_list}

    return render(request, 'management/index.html',context)


def project_overview_detail(request,project_id):
    """
        Show all test case
        Show status of testcase       """
    project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
    project_test_case_list=rrt_project_test_case.objects.filter(project_id_id=project_id)
    context = {'project_test_case_list': project_test_case_list,'project_list': project_list}
    return render(request, 'management/project_overview_detail.html', context)

def new_project(request):
    form = None
    if request.method == 'GET':
        """
            Show all test case
            Show status of testcase
           """
        project_list = models.rrt_project.objects.all().order_by('-modify_time')[0:5]
        context = {'project_list': project_list}
        return render(request, 'management/new_project.html',context)

    elif request.method == 'POST':
        form = New_Project_Form(request.POST)
        if form.is_valid():
            new_project_information = form.cleaned_data
            project_name=new_project_information['project_name']
            project_description=new_project_information['project_description']
            project_list = rrt_project.objects.filter(project_name=project_name)
            if len(project_list) < 1:
                project = rrt_project(project_name=project_name, project_description=project_description)
                project.save()
                return HttpResponseRedirect(reverse('management:project_overview'))
            else:
                return HttpResponseRedirect(reverse('management:project_overview'))

        else:
            #弹出alert窗口
            #弹出alert窗口
            print "error"