from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance


class Baby(models.Model):
    name = models.TextField(max_length=40,null=True)
    birthday = models.DateField(null=True)
    sex = models.TextField(max_length=10,null=True)
    weight = models.FloatField(2,null=True)
    height = models.FloatField(2,null=True)
    parent_id = models.IntegerField(10,null=True)
    homeaddr = models.TextField(max_length=100,null=True)
    schooladdr = models.TextField(max_length=100,null=True)
    homepoint = models.PointField(null=True)
    objects = models.GeoManager()