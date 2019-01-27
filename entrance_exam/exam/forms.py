from django import forms
from exam.models import Customer
from exam.models import Lesson

class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)


class CustomerEdit(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)

class LessonForm(forms.ModelForm):
  class Meta:
    model = Lesson
    fields = ('customer', 'genre', 'lesson_day', 'lesson_time')

class LessonEdit(forms.ModelForm):
  class Meta:
    model = Lesson
    fields = ('customer', 'genre', 'lesson_day', 'lesson_time')
