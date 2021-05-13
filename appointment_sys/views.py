from django.shortcuts import render

# Create your views here.


from HIS.models import Register


def index(request):
    return render(request, 'appointment_sys/index.html')


