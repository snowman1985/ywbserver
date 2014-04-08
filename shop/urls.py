'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.conf.urls import patterns, url

from shop import views

urlpatterns = patterns('',
    url(r'^webview/([0-9]*)/$', views.web_view),
    url(r'^addshop/', views.ShopFormView.as_view(success_url='/shop/addshop/')),
    url(r'^addshopcomment/(\d+)/$', views.addshopcomment),
)
