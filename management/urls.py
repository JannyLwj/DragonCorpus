from django.conf.urls import url
import views

urlpatterns = [
    #login
    url(r'^index/$',views.index,name='index'),
    url(r'^(?P<project_id>\w+)/project_overview_detail/$',views.project_overview_detail,name='project_overview_detail'),
    url(r'^project_overview_detail_table/$',views.project_overview_detail_table,name='project_overview_detail_table'),
    url(r'^testsuit_overview_detail_table/$', views.testsuit_overview_detail_table, name='testsuit_overview_detail_table'),
    url(r'^utterance_table/$', views.utterance_table, name='utterance_table'),
    url(r'^(?P<testsuit_id>\w+)/testsuit_overview_detail/$', views.testsuit_overview_detail,name='testsuit_overview_detail'),
    url(r'^new_project/$',views.new_project,name='new_project'),
    url(r'^new_testsuit/$',views.new_testsuit,name='new_testsuit'),
    url(r'^utterance/$', views.utterance, name='utterance'),
    url(r'^upload_hrl/$', views.upload_hrl, name='upload_hrl'),
    url(r'^project_and_testsuit_overview_detail/$', views.project_and_testsuit_overview_detail, name='project_and_testsuit_overview_detail'),
    #filter
    url(r'^get_all_intent/$', views.get_all_intent, name='get_all_intent'),
    url(r'^get_testsuit_all_intent/$', views.get_testsuit_all_intent, name='get_testsuit_all_intent'),

    #error
    url(r'^error_page/$', views.error_page, name='error_page'),

    #delete testsuit
    url(r'^delete_testsuit/$', views.delete_testsuit,name='delete_tesuit'),
    # add testSuit
    url(r'^add_testsuit/$', views.add_testsuit, name='add_testsuit'),
    # delete_testsuit_item
    url(r'^delete_testsuit_item/$', views.delete_testsuit_item, name='delete_testsuit_item'),
    #download_testsuit
    url(r'^download_testsuit/$', views.download_testsuit, name='download_testsuit'),
    url(r'^zip_download/$', views.zip_download, name='zip_download'),
    #upload audio
    url(r'^upload_utterance_table/$', views.upload_utterance_table, name='upload_utterance_table'),

]