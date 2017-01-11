#_*_coding:utf-8_*_
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'client/config/(\d+)/$',views.client_configs)
]