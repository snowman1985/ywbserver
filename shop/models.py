from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
import random

class Shop(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    abstract = models.CharField(max_length=2000)
    description = models.CharField(max_length=5000)
    url = models.CharField(max_length=1000)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    point = models.PointField()
    objects = models.GeoManager()

class EduShop(Shop):
    pass

class EntertainShop(Shop):
    pass

class ShopComment(models.Model):
    shopid = models.ForeignKey(Shop)
    comment = models.CharField(max_length=500)


def get_shop_nearby(latitude, longitude, number=1, distance = 5000):
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    nearby = Shop.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    count = nearby.count()
    if number >= count:
        print('shop nearby %f,%f is not enough' % (latitude, longitude))
        return list(Shop.objects.all()[:number-1])
    else:
        return random.sample(list(nearby), number)

def get_shop_random(number=1):
    all = Shop.objects.all()
    count = all.count()
    if number >= count:
        print('shop random  is not enough')
        return list(all[:count])
    else:
        return random.sample(list(all), number)
