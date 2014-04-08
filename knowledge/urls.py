'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from knowledge import views

urlpatterns = patterns('',
    url(r'^collectknowl/',views.collectknowl, name='collectknowl'),
    url(r'^webview/([0-9]*)/$', views.web_view),
    url(r'^add/$', views.KnowledgeFormView.as_view(success_url='/knowledge/add/')),
)
