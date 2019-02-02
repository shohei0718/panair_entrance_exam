from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from exam.models import Customer, Lesson
from exam.forms import CustomerForm, LessonForm, InvoiceSearchForm
import copy


def index(request):
  return render(request, 'exam/index.html')


def customer_index(request):
  columns = {
    'customer_list': Customer.objects.all()
  }
  return render(request, 'exam/customer_index.html', columns)


def customer_form(request):
  form = CustomerForm(request.POST or None)

  if request.method == 'POST' and form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('customer_index'))

  return render(request, 'exam/customer_form.html',
    {'form': form})


def customer_edit(request, pk):
  customer = get_object_or_404(Customer, pk=pk)

  form = CustomerForm(request.POST or None, instance=customer)

  if request.method == 'POST' and form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('customer_index'))

  return render(request, 'exam/customer_edit.html', {'form': form})


def lesson_index(request):
  lessons = Lesson.objects.all()

  form = InvoiceSearchForm(request.GET)

  if form.is_valid():
    lesson_day = form.cleaned_data.get('lesson_day')
    if lesson_day:
      lessons = lessons.filter(lesson_day__contains=lesson_day)

  return render(request, 'exam/lesson_index.html', {'lessons':lessons, 'form':form})


def lesson_form(request):
  PRICE_PER_HOUR = {'英語':3500, 'ファイナンス':3500, 'プログラミング':3300}
  form = LessonForm(request.POST or None)

  if request.method == "POST" and form.is_valid():
    lesson = form.save(commit=False)

    if lesson.genre == '英語':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['英語']
    elif lesson.genre == 'ファイナンス':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['ファイナンス']
    elif lesson.genre == 'プログラミング':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['プログラミング']

    lesson.save()
    return HttpResponseRedirect(reverse('lesson_index'))

  return render(request, 'exam/lesson_form.html', {'form': form})


def lesson_edit(request, pk):
  PRICE_PER_HOUR = {'英語':3500, 'ファイナンス':3500, 'プログラミング':3300}

  lesson = get_object_or_404(Lesson, pk=pk)
  form = LessonForm(request.POST or None, instance=lesson)

  if request.method == "POST" and form.is_valid():
    lesson = form.save(commit=False)

    if lesson.genre == '英語':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['英語']
    elif lesson.genre == 'ファイナンス':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['ファイナンス']
    elif lesson.genre == 'プログラミング':
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR['プログラミング']

    lesson.save()
    return HttpResponseRedirect(reverse('lesson_index'))

  return render(request, 'exam/lesson_edit.html', {'form': form})


def invoice_index(request):

  customers = Customer.objects.all()
  sum_template =  {'英語': 0, 'ファイナンス': 0, 'プログラミング': 0}
  invoice_list = []

  for customer in customers:
    columns = {}

    english_invoice = 0
    finance_invoice = 0
    programing_invoice = 0

    genre_sum = sum_template.copy()
    lesson_time_sum = sum_template.copy()

    lessons = customer.lesson_set.all()
    lesson_sum = lessons.count()

    columns['id'] = customer.id
    columns['name'] = customer.name
    columns['lesson'] = lesson_sum

    for lesson in lessons:
      lesson_day = lesson.lesson_day
      columns['lesson_day'] = lesson_day

      form = InvoiceSearchForm(request.GET)
      form.is_valid()

      lesson_day = form.cleaned_data.get('lesson_day')

      if lesson_day:
        columns = columns.filter(lesson_day__icontains=lesson_day)

      genre = lesson.genre
      genre_sum[genre] += 1
      columns['genre'] = genre_sum

      lesson_time = lesson.lesson_time
      lesson_time_sum[genre] += lesson_time
      columns['lesson_time'] = lesson_time_sum

      if genre == '英語':
        english_invoice = 5000 + lesson_time * 3500

      if genre == 'ファイナンス' and (lesson_time <= 20):
        finance_invoice = lesson_time * 3300
      elif genre == 'ファイナンス' and (20 < lesson_time <= 50):
        finance_invoice = (20 * 3300) + (lesson_time - 20)* 2800
      elif genre == 'ファイナンス' and (lesson_time > 50):
        finance_invoice = (20 * 3300) + (30 * 2800) + (lesson_time - 50)* 2500

      if genre == 'プログラミング' and (lesson_time <= 5):
        programing_invoice = 20000
      elif genre == 'プログラミング' and (5 < lesson_time <= 20):
        programing_invoice = 20000 + (lesson_time - 5)* 3500
      elif genre == 'プログラミング' and (20 < lesson_time <= 35):
        programing_invoice = 20000 + (15 * 3500) + (lesson_time - 20)* 3000
      elif genre == 'プログラミング' and (35 < lesson_time <= 50):
        programing_invoice = 20000 + (15 * 3500) + (15 * 3000) + (lesson_time - 35)* 3000
      elif genre == 'プログラミング' and (lesson_time > 50):
        programing_invoice = 20000 + (lesson_time - 5)* 2500

      total = english_invoice + finance_invoice + programing_invoice
      columns['price'] = total

    invoice_list.append(columns)


  return render(request, 'exam/invoice_index.html', {'customers': customers, 'columns':columns, 'invoice_list':invoice_list, 'form':form})

def report_index(request):
  invoice_list = []
  lessons = [
    {'genre':'英語', 'gender':'男'},
    {'genre':'英語', 'gender':'女'},
    {'genre':'ファイナンス', 'gender':'男'},
    {'genre':'ファイナンス', 'gender':'女'},
    {'genre':'プログラミング', 'gender':'男'},
    {'genre':'プログラミング', 'gender':'女'}
  ]

  for lesson in lessons:
    english_invoice = 0
    finance_invoice = 0
    programing_invoice = 0

    les_sum = {'lesson':0}

# ジャンルが英語の場合

    if lesson['genre'] =='英語' and lesson['gender'] == '男':
      men = Customer.objects.filter(gender='男')
      customer_list = []
      lesson_time_sum = 0

      for man in men:
        en_lessons = man.lesson_set.filter(genre='英語')
        lesson_sum = en_lessons.count()
        les_sum['lesson'] += lesson_sum

        for en_lesson in en_lessons:
          name = en_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)
          lesson['customer'] = customer

          lesson_time = en_lesson.lesson_time
          lesson_time_sum += lesson_time

      english_invoice = 5000 * customer + lesson_time_sum * 3500
      lesson['price']= english_invoice
      lesson['lesson'] = les_sum['lesson']


    if lesson['genre'] =='英語' and lesson['gender'] == '女':
      women = Customer.objects.filter(gender='女')
      customer_list = []
      lesson_time_sum = 0

      for woman in women:
        en_lessons = woman.lesson_set.filter(genre='英語')
        lesson_sum = en_lessons.count()
        les_sum['lesson'] += lesson_sum

        for en_lesson in en_lessons:
          name = en_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)
          lesson['customer'] = customer

          lesson_time = en_lesson.lesson_time
          lesson_time_sum += lesson_time

      english_invoice = 5000 * customer + lesson_time_sum * 3500
      lesson['price']= english_invoice
      lesson['lesson'] = les_sum['lesson']

# ジャンルがファイナンスの場合

    if lesson['genre'] =='ファイナンス' and lesson['gender'] == '男':
      men = Customer.objects.filter(gender='男')
      customer_list = []
      lesson_time_sum = 0

      for man in men:
        fi_lessons = man.lesson_set.filter(genre='ファイナンス')
        lesson_sum = fi_lessons.count()
        les_sum['lesson'] += lesson_sum

        for fi_lesson in fi_lessons:
          name = fi_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)

          lesson_time = fi_lesson.lesson_time
          lesson_time_sum += lesson_time
          lesson['customer'] = customer

      if lesson_time_sum == 0:
        finance_invoice = 0
      elif lesson_time_sum <= 20:
        finance_invoice = lesson_time_sum * 3300
      elif 20 < lesson_time_sum <= 50:
        finance_invoice = (20 * 3300) + (lesson_time_sum - 20)* 2800
      elif lesson_time_sum > 50:
        finance_invoice = (20 * 3300) + (30 * 2800) + (lesson_time_sum - 50)* 2500
      lesson['price']= finance_invoice

      lesson['lesson'] = les_sum['lesson']


    if lesson['genre'] =='ファイナンス' and lesson['gender'] == '女':
      women = Customer.objects.filter(gender='女')
      customer_list = []
      lesson_time_sum = 0

      for woman in women:
        fi_lessons = woman.lesson_set.filter(genre='ファイナンス')
        lesson_sum = fi_lessons.count()
        les_sum['lesson'] += lesson_sum

        for fi_lesson in fi_lessons:
          name = en_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)
          lesson['customer'] = customer

          lesson_time = fi_lesson.lesson_time
          lesson_time_sum += lesson_time

      if lesson_time_sum == 0:
        finance_invoice = 0
      elif lesson_time_sum <= 20:
        finance_invoice = lesson_time_sum * 3300
      elif 20 < lesson_time_sum <= 50:
        finance_invoice = (20 * 3300) + (lesson_time_sum - 20)* 2800
      elif lesson_time_sum > 50:
        finance_invoice = (20 * 3300) + (30 * 2800) + (lesson_time_sum - 50)* 2500
      lesson['price']= finance_invoice

      lesson['lesson'] = les_sum['lesson']

# ジャンルがプログラミングの場合

    if lesson['genre'] =='プログラミング' and lesson['gender'] == '男':
      men = Customer.objects.filter(gender='男')
      customer_list = []
      lesson_time_sum = 0

      for man in men:
        pro_lessons = man.lesson_set.filter(genre='プログラミング')
        lesson_sum = pro_lessons.count()
        les_sum['lesson'] += lesson_sum

        for pro_lesson in pro_lessons:
          name = pro_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)
          lesson['customer'] = customer

          lesson_time = pro_lesson.lesson_time
          lesson_time_sum += lesson_time

      if lesson_time_sum == 0:
        programing_invoice = 0
      elif 0 < lesson_time_sum <= 5:
        programing_invoice = 20000 * customer
      elif 5 < lesson_time_sum <= 20:
        programing_invoice = 20000 * customer + (lesson_time_sum - 5)* 3500
      elif 20 < lesson_time_sum <= 35:
        programing_invoice = 20000 * customer + (15 * 3500) + (lesson_time_sum - 20)* 3000
      elif 35 < lesson_time_sum <= 50:
        programing_invoice = 20000 * customer + (15 * 3500) + (15 * 3000) + (lesson_time_sum - 35)* 3000
      elif lesson_time_sum > 50:
        programing_invoice = 20000 * customer + (lesson_time_sum - 5)* 2500
      lesson['price']= programing_invoice

      lesson['lesson'] = les_sum['lesson']


    if lesson['genre'] =='プログラミング' and lesson['gender'] == '女':
      women = Customer.objects.filter(gender='女')
      customer_list = []
      lesson_time_sum = 0

      for woman in women:
        pro_lessons = woman.lesson_set.filter(genre='プログラミング')
        lesson_sum = pro_lessons.count()
        les_sum['lesson'] += lesson_sum

        for pro_lesson in pro_lessons:
          name = en_lesson.customer.name
          customer_list.append(name)
          customer_set = list(set(customer_list))
          customer = len(customer_set)
          lesson['customer'] = customer

          lesson_time = pro_lesson.lesson_time
          lesson_time_sum += lesson_time

      if lesson_time_sum == 0:
        programing_invoice = 0
      elif 0 < lesson_time_sum <= 5:
        programing_invoice = 20000 * customer
      elif 5 < lesson_time_sum <= 20:
        programing_invoice = 20000 * customer + (lesson_time_sum - 5)* 3500
      elif 20 < lesson_time_sum <= 35:
        programing_invoice = 20000 * customer + (15 * 3500) + (lesson_time_sum - 20)* 3000
      elif 35 < lesson_time_sum <= 50:
        programing_invoice = 20000 * customer + (15 * 3500) + (15 * 3000) + (lesson_time_sum - 35)* 3000
      elif lesson_time_sum > 50:
        programing_invoice = 20000 * customer + (lesson_time_sum - 5)* 2500
      lesson['price']= programing_invoice

      lesson['lesson'] = les_sum['lesson']


    invoice_list.append(lesson)

  return render(request, 'exam/report_index.html', {'lessons':lessons, 'invoice_list':invoice_list})
