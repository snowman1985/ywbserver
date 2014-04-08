from django.db import models
import base64, json, random, math

class Knowledge(models.Model):
    title = models.CharField(max_length=1000)
    keyword = models.CharField(max_length=1000)
    abstract = models.TextField(max_length=1000)
    content = models.TextField(max_length=50000)
    min = models.IntegerField()
    max = models.IntegerField()
    apply_sex = models.CharField(max_length=10)
    url = models.CharField(max_length=1000)

class KnowledgeCollection(models.Model):
    user_id = models.IntegerField(10,null=True)
    collection_list = models.CharField(max_length=20000,null=True)


def get_knowls_byage(age, number = 5):
    knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
    count = knowls.count()
    if number >= count:
        print('knowledge in age %d is not enough' % age)
        return list(Knowledge.objects.all()[:number])
    else:
        return random.sample(list(knowls), number)

def get_knowls_random(number = 5):
    knowls = Knowledge.objects.all()
    count = knowls.count()
    if number >= count:
        return list(Knowledge.objects.all()[:1])
    else:
        return random.sample(list(knowls), number)
    