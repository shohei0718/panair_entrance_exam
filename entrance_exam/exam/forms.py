from django import forms
from exam.models import Customer
from exam.models import Lesson
from datetime import datetime, date

class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)


class LessonForm(forms.ModelForm):
  class Meta:
    model = Lesson
    fields = ('customer', 'genre', 'lesson_day', 'lesson_time')

class InvoiceSearchForm(forms.Form):
  lesson_day = forms.CharField(label='受講日', required=False)

