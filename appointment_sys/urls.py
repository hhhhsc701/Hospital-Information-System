from django.urls import path

from . import views

app_name = 'appointment_sys'
urlpatterns = [
    path('', views.index, name='index'),
]
