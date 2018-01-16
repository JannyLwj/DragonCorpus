from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^new_project/$',views.new_project,name='new_project'),
]