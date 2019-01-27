from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

class Customer(models.Model):
  Men = '男'
  Women = '女'
  GENDER = (
    (Men, '男'),
    (Women, '女'),
  )

  name = models.CharField('名前', max_length = 20)
  gender = models.CharField(
    '性別',
    max_length = 1,
    choices=GENDER,
    )
  age = models.IntegerField('年齢')

class Lesson(models.Model):
  English = '英語'
  Finance = 'ファイナンス'
  Programing = 'プログラミング'
  GENRE = (
    (English, '英語'),
    (Finance, 'ファイナンス'),
    (Programing, 'プログラミング'),
  )

  customer = models.ForeignKey(Customer, verbose_name='顧客名', on_delete=models.PROTECT)

  genre = models.CharField(
    'ジャンル',
    max_length = 255,
    choices=GENRE,
    default=English)
  lesson_day = models.DateField('受講日')
  lesson_time = models.PositiveIntegerField(
    '受講時間（h）',
    default = 1,
    validators=[
      MaxValueValidator(12),
      MinValueValidator(1)
    ]
  )
  price = models.IntegerField('支払金額', null=True)

