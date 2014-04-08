'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from consumption import views

urlpatterns = patterns('',
    url(r'^webview/([0-9]*)/$', views.consumption_web_view),
    url(r'^addconsumption/', views.consumptionFormView.as_view(success_url='/consumption/addconsumption/')),
    url(r'^addconsumptioncomment/(\d+)/$', views.addconsumptioncomment),
)
