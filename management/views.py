# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import JSONRenderer

from management import models
from management.PageInfo import PageInfo

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
    context={'rrt_project_count': rrt_project_count, 'rrt_utterance_count': rrt_utterance_count,'rrt_domain_count':rrt_domain_count,
                   'rrt_intent_count':rrt_intent_count,'rrt_audio_count':rrt_audio_count,'rrt_testsuit_count':rrt_testsuit_count}

    return render(request, 'management/index.html',context)