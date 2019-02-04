from django.db import models
from django.utils import timezone
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


class Customer(models.Model):
  Men = '男'
  Women = '女'
  GENDER = (
    (Men, '男'),
    (Women, '女'),
  )

  name = models.CharField('名前', null=False, max_length = 20)
  gender = models.CharField(
    '性別',
    max_length = 1,
    choices=GENDER,
    )
  age = models.PositiveIntegerField('年齢', null=False)

  def __str__(self):
    return self.name


class Lesson(models.Model):
  name = models.CharField('ジャンル', null=True, max_length=255)
  flat_price = models.PositiveIntegerField('基本料金', null=False, default=0)

  def __str__(self):
    return self.name

  def calculate_measured_price(lesson_hour):
    lesson_measured_price = LessonMeasuredPrice.objects.select(record, record.lesson_hour <= lesson_hour ).sort_by(lesson_hours).last
    lesson_measured_price.price

class LessonMeasuredPrice(models.Model):
  lesson_id = models.ForeignKey(Lesson, on_delete=models.PROTECT)
  price = models.PositiveIntegerField('金額', null=False, default=0)
  threshold_hours = models.PositiveIntegerField('受講時間（h）', null=False, default=0)


class CustomerLesson(models.Model):
  customer = models.ForeignKey(Customer, verbose_name='顧客名', on_delete=models.PROTECT)
  lesson = models.ForeignKey(Lesson,verbose_name='ジャンル', on_delete=models.PROTECT)

  lesson_date = models.DateField('受講日', default=timezone.now)
  lesson_hour = models.PositiveIntegerField(
    '受講時間（h）',
    default = 1,
    validators=[
      MaxValueValidator(12),
      MinValueValidator(1)
    ]
  )

  def __str__(self):
    return self.lesson

class BillingPriceCalculator(Lesson):

  def __init__(self, genre, this_month_lessons):
    self.genre = genre
    self.this_month_lessons = this_month_lessons

  def flat_price(self):
    return genre.flat_price

  def total_hours(self):
    return customer_lessons.sum(lesson_hour)

  def measured_price_unit(self):
    return lesson.calculate_measured_price(total_hours)

  def measured_price(self):
    return measured_price_unit * total_hours


  def total_price(self):
    return flat_price() + measured_price()
