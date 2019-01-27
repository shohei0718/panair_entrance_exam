from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse
from exam.models import Customer
from exam.forms import CustomerForm
from exam.forms import CustomerEdit
from exam.models import Lesson
from exam.forms import LessonForm
from exam.forms import LessonEdit
# Create your views here.


def index(request):
  return render(request, 'exam/index.html')


def customer_index(request):
  columns = {'customer_list': Customer.objects.all()}
  return render(request, 'exam/customer_index.html', columns)


def customer_form(request):
  if request.method == 'POST':
    form = CustomerForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('customer_index'))

  else:
    form = CustomerForm()

  return TemplateResponse(request, 'exam/customer_form.html',
    {'form': form})


def customer_edit(request, customer_id):
  try:
    customer = Customer.objects.get(id = customer_id)
  except Customer.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = CustomerEdit(request.POST, instance=customer)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('customer_index'))
  else:
    form = CustomerEdit(instance=customer)
  return TemplateResponse(request, 'exam/customer_edit.html', {'form': form})


def lesson_index(request):
  lessons = {'lesson_list': Lesson.objects.all()}
  return render(request, 'exam/lesson_index.html', lessons)


def lesson_form(request):
  PRICE_PER_HOUR = {'英語':3500, 'ファイナンス':3500, 'プログラミング':3300}

  if request.method == "POST":
    form = LessonForm(request.POST)

    if form.is_valid():
      lesson = form.save(commit=False)
      if lesson.genre == '英語':
        lesson.price = lesson.lesson_time * PRICE_PER_HOUR['英語']
      elif lesson.genre == 'ファイナンス':
        lesson.price = lesson.lesson_time * PRICE_PER_HOUR['ファイナンス']
      elif lesson.genre == 'プログラミング':
        lesson.price = lesson.lesson_time * PRICE_PER_HOUR['プログラミング']
      lesson.save()
      return HttpResponseRedirect(reverse('lesson_index'))

  else:
    form = LessonForm()
  return TemplateResponse(request, 'exam/lesson_form.html', {'form': form})


def lesson_edit(request, lesson_id):
  try:
    lesson = Lesson.objects.get(id = lesson_id)
  except Lesson.DoesNotExist:
    raise Http404
  except ValidationError:
    return 入力内容に誤りがあります

  if request.method == "POST":
    form = LessonForm(request.POST, instance=lesson)
    if form.is_valid():
      lesson = form.save(commit=False)
      lesson.price = lesson.lesson_time * PRICE_PER_HOUR
      lesson.save()
      return HttpResponseRedirect(reverse('lesson_index'))
  else:
    form = LessonForm(instance=lesson)
  return TemplateResponse(request, 'exam/lesson_edit.html', {'form': form})


def invoice_index(request):
  return render(request, 'exam/invoice_index.html')


def report_index(request):
  return render(request, 'exam/report_index.html')
