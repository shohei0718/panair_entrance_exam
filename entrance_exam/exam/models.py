from django.db import models
from django.utils import timezone


class Customer(models.Model):
  title = models.CharField('名前', max_length = 20)
  gender = models.CharField('性別', max_length = 2)
  age = models.IntegerField('年齢')
