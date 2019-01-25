from django import forms
from exam.models import Customer


class CustomerForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)


class CustomerEdit(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('name', 'gender', 'age',)
