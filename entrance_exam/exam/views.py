from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponse
from exam.models import Customer
from exam.forms import CustomerForm
from exam.forms import CustomerEdit

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
  return render(request, 'exam/lesson_index.html')


def invoice_index(request):
  return render(request, 'exam/invoice_index.html')


def report_index(request):
  return render(request, 'exam/report_index.html')
