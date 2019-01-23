from django.shortcuts import render
from django.http import HttpResponse
from exam.models import Customer

# Create your views here.

def index(request):
  context = {'word': 'Hello, World'}
  return render(request, 'exam/index.html', context)


def customer_index(request):
  columns = {'word': 'Hello, World'}
  return render(request, 'exam/customer_index.html', columns)


def lesson_index(request):
  columns = {'word': 'Hello, World'}
  return render(request, 'exam/lesson_index.html', columns)


def invoice_index(request):
  columns = {'word': 'Hello, World'}
  return render(request, 'exam/invoice_index.html', columns)


def report_index(request):
  columns = {'word': 'Hello, World'}
  return render(request, 'exam/report_index.html', columns)
