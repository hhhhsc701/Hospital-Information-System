from django.urls import path

from . import views

app_name = 'patient_information_sys'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('modify/', views.modify, name='modify'),
    path('search_for_patient/', views.search_for_patient, name='search_for_patient'),
    path('search_for_doctor_enter/', views.search_for_doctor_enter, name='search_for_doctor_enter'),
    path('search_for_doctor_option/', views.search_for_doctor_option, name='search_for_doctor_option'),
    path('register_information/', views.register_information, name='register_information'),
    path('prescription_information/', views.prescription_information, name='prescription_information'),
    path('inspection_information/', views.inspection_information, name='inspection_information'),
    path('operation_information/', views.operation_information, name='operation_information'),
    path('medicine_information/', views.medicine_information, name='medicine_information'),
    path('hospitalized_information/', views.hospitalized_information, name='hospitalized_information'),
    path('rounds_information/', views.rounds_information, name='rounds_information'),
]