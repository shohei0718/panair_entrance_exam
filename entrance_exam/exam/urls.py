from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('customer_index', views.customer_index, name = 'customer_index'),
    path('customer_form', views.customer_form, name = 'customer_form'),
    path('customer/<int:customer_id>/edit', views.customer_edit, name = 'customer_edit'),
    path('lesson_index', views.lesson_index, name = 'lesson_index'),
    path('lesson_form', views.lesson_form, name = 'lesson_form'),
    path('lesson/<int:lesson_id>/edit', views.lesson_edit, name = 'lesson_edit'),
    path('invoice_index', views.invoice_index, name = 'invoice_index'),
    path('report_index', views.report_index, name = 'report_index'),
]
