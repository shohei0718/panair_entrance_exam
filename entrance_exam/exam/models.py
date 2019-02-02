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

  def __str__(self):
    return self.name

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

  def __str__(self):
    return self.genre

"""
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

today = datetime.today()

#今月の月初日と月末日の算出
month_start = today.replace(day=1)
next_month_start = (today + relativedelta(months=1)).replace(day=1)
month_end = next_month_start - timedelta(days=1)

#先月の月初日と月末日の算出
one_month_ago_start = (today - relativedelta(months=1)).replace(days=1)
one_month_ago_end = next_month_start - timedelta(days=1)

#2ヶ月前の月初日と月末日の算出
two_month_ago_start = (today - relativedelta(months=2)).replace(days=1)
two_month_ago_end = one_month_ago_start - timedelta(days=1)

#3ヶ月前の月初日と月末日の算出
three_month_ago_start = (today - relativedelta(months=3)).replace(days=1)
three_month_ago_end = two_month_ago_start - timedelta(days=1)
"""
