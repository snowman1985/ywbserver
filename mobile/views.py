from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import *
from shop.models import *
from consumption.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from datetime import *
from users.utils import *
import base64, json, random, math
from django.template.loader import get_template
from django.template import Context
from ywbserver.settings import *

def getknowllist(baby, number):
    if(baby.birthday):
        age= (int((date.today() - baby.birthday).days))
        response = knowledge_list_encode(get_knowls_byage(age, number))
    else:
        response = knowledge_list_encode(get_knowls_random(number))
    return response

def getshoplist(baby, number):
    respones = None
    if(baby.homepoint):
        latitude = baby.homepoint.y
        longitude = baby.homepoint.x
        response = shop_list_encode(get_shop_nearby(latitude, longitude, number))
    else:
        response = shop_list_encode(get_shop_random(number))
    return response

def getconsumptionlist(baby, number):
    respones = None
    if(baby.homepoint):
        latitude = baby.homepoint.y
        longitude = baby.homepoint.x
        response = consumption_list_encode(get_consumption_nearby(latitude, longitude, number))
    else:
        response = consumption_list_encode(get_consumption_random(number))
    return response

def getknowllist_anonymous(request, number):
    if not request.POST.get('age'):
        return HttpResponse('PARAMETER_NULL_AGE')
    age = int(request.POST.get('age'))
    response = knowledge_list_encode(get_knowls_byage(age, number))
    return response

def getshoplist_anonymous(request, number):
    response = shop_list_encode(get_shop_random(number))
    return response

def getconsumptionlist_anonymous(request, number):
    response = consumption_list_encode(get_consumption_random(number))
    return response

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def mobile_view(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    knumber = int(request.POST.get('knumber'))
    snumber = int(request.POST.get('snumber'))
    cnumber = int(request.POST.get('cnumber'))
    if knumber == None or snumber == None or cnumber == None:
        return HttpResponse('PARAMETER_NULL_number')
    if user.username == 'anonymous':
        knowls = getknowllist_anonymous(request, knumber)
        shops = getshoplist_anonymous(request, snumber)
        consumptions = getconsumptionlist_anonymous(request, cnumber)
        return HttpResponse(data_encode(knowls, shops, consumptions))
    else:
        baby = Baby.objects.get(parent_id=user.id)
        if not baby:
            return HttpResponse('BABY_DATA_NULL')
        knowls = getknowllist(baby, knumber)
        shops = getshoplist(baby, snumber)
        consumptions = getconsumptionlist(baby, cnumber)
        return HttpResponse(data_encode(knowls, consumptions, consumptions))
    
def data_encode(knowls, shops, consumptions):
    rets = knowls+shops+consumptions
    return json.dumps(rets, ensure_ascii=False)
    
def knowledge_list_encode(knowls):
    rets = []
    number = len(list(knowls))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        knowl = knowls[i]
        t = {}
        tags = knowl.keyword.split(';')
        t['id'] = knowl.id
        t['title'] = knowl.title
        t['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://wjbb.cloudapp.net:8001/icon/'+str(picindexes[i])+'.png'
        if knowl.abstract:
            t['Abstract'] = knowl.abstract
        else:
            t['Abstract'] = " "
        t['address'] = ""
        t['link'] = DOMAIN + ("knowledge/webview/%d/" % knowl.id)
        rets.append(t)
    return rets

def shop_list_encode(shops):
    rets = []
    number = len(list(shops))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        shop = shops[i]
        t = {}
        t['id'] = shop.id
        t['title'] = shop.name
        t['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://wjbb.cloudapp.net:8001/icon/'+str(picindexes[i])+'.png'
        if shop.abstract:
            t['Abstract'] = shop.abstract
        else:
            t['Abstract'] = " "
        t['address'] = shop.address
        t['link'] = DOMAIN + ("shop/webview/%d/" % shop.id)
        rets.append(t)
    return rets

def consumption_list_encode(consumptions):
    rets = []
    number = len(list(consumptions))
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        consumption = consumptions[i]
        t = {}
        t['id'] = consumption.id
        t['title'] = consumption.name
        t['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[i])+'.jpg'
        t['icon'] = 'http://wjbb.cloudapp.net:8001/icon/'+str(picindexes[i])+'.png'
        if consumption.abstract:
            t['Abstract'] = consumption.abstract
        else:
            t['Abstract'] = " "
        t['address'] = consumption.address
        t['link'] = DOMAIN + ("consumption/webview/%d/" % consumption.id)
        rets.append(t)
    return rets
