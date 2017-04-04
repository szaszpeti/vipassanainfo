from django.conf.urls import url
from . import views

# app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^english/$', views.english, name='english')
]