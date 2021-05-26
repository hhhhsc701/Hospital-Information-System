from django.urls import path

from . import views

app_name = 'patient_information_sys'
urlpatterns = [
    path('', views.index, name='index'),
    path('modify/', views.modify, name='modify'),
    path('search_result_for_doctor/', views.search_result_for_doctor, name='search_result_for_doctor'),
]