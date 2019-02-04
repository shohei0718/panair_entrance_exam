from django import forms
from exam.models import Customer, Lesson, CustomerLesson
from exam.models import Lesson
from datetime import datetime, date

class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)


class LessonForm(forms.ModelForm):
  class Meta:
    model = CustomerLesson
    fields = ('customer', 'lesson', 'lesson_date', 'lesson_hour')

class InvoiceSearchForm(forms.Form):
  lesson_date = forms.CharField(label='受講日', required=False)
