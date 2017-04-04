from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.user_login, name='user_login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^create/$', views.post_create, name="create"),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.post_detail, name="detail"),
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', views.post_update, name="edit"),
    url(r'^update/$', views.post_update, name="update"),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.post_delete, name="delete"),



]
