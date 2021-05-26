from django.urls import path

from . import views

app_name = 'hospitalization_sys'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_rounds_for_nurse/', views.search_round_for_nurse, name='search_for_nurse'),
    path('search_discharge/', views.search_discharge, name='search_discharge'),
    path('search_discharge/process_apply_discharge/', views.process_apply_discharge, name='process_apply_discharge'),
    path('discharge_process/', views.discharge_process, name='discharge_process'),
]