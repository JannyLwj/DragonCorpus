from django.conf.urls import url
import views

urlpatterns = [
    #url(r'^list/$', views.RuningTestcase_list, name='RuningTestcase_list'),
    #url(r'^log/$',  views.RuningTestcase_post, name='RuningTestcase_post'),
    url(r'^index/$',views.index,name='index'),
    #url(r'^(?P<domain>\w+)/index_domain/$', views.index_domain, name='index_domain'),
    #url(r'^result/$',views.result,name='result'),
    #url(r'^result_suit/$',views.result_suit,name='result_suit'),
    #url(r'^(?P<domain>\w+)/result_domain/$', views.result_domain, name='result_domain'),
    #url(r'^(?P<testsuit_id>[0-9]+)/result_suit/$', views.result_suit, name='result_suit'),
    #url(r'^runcase/$',views.runingtestcase,name='runingtestcase'),
    #url(r'^not_start_runingtestcase/$', views.not_start_runingtestcase, name='not_start_runingtestcase'),
    #url(r'^fail/$',views.failedresult,name='failedresult'),
    #url(r'^runalltestcase/$',views.runalltestcase,name='runalltestcase'),
    #url(r'^runsanitytestcase/$',views.runsanitytestcase,name='runsanitytestcase'),
    #url(r'^rerunfailedtestcase/$',views.Rerunfailedtestcase,name='Rerunfailedtestcase'),
    #url(r'^reruntestcase/$',views.reruntestcase,name='reruntestcase'),
]