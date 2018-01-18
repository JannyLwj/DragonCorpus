from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    #url(r'^project_overview/$',views.project_overview,name='project_overview'),
    url(r'^(?P<project_id>\w+)/project_overview_detail/$',views.project_overview_detail,name='project_overview_detail'),
    url(r'^new_project/$',views.new_project,name='new_project'),
]