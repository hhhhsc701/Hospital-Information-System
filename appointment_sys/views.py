from django.shortcuts import render
from django.http import HttpResponse, Http404
from datetime import datetime
from django.db.models import Q
import random
from django.utils import timezone

# Create your views here.


from HIS.models import Register, Doctor, Patient, Project


def index(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    if request.method == 'GET':
        return render(request, 'appointment_sys/index.html')
    elif request.method == 'POST':

        try:
            appointment_time = request.POST['appointment_time']  # 挂号时间
        except:
            # current_tz = timezone.get_current_timezone()  # 时区
            register_time = datetime.now()
            # register_time = current_tz.localize(register_time)
            register_department = int(request.POST['register_department'])  # 挂号科室
            register_type = int(request.POST['register_type'])  # 挂号类型
            optional_doctors = Doctor.objects.filter(Q(department=register_department), Q(job_title=register_type), Q(surgery=register_time.weekday()))
            try:
                selected_doctor = random.choice(optional_doctors)
            except:
                message2 = '挂号失败!该时间无所需在诊医生!请重新选择!'
                return render(request, 'appointment_sys/index.html', locals())
            id = '%d' % (Register.objects.all().count() + 1)
            if register_type == 0:
                project_ID = Project.objects.get(id='2')
            elif register_type == 1:
                project_ID = Project.objects.get(id='3')
            Register.objects.create(
                id=id,
                doctor_id=selected_doctor,
                patient_id=Patient.objects.get(id=request.session['user_id']),
                department=register_department,
                project=project_ID  # 项目表未创建，创建后需改动
            )
            message2 = '挂号成功!'
            return render(request, 'appointment_sys/index.html', locals())
        appointment_time = datetime.strptime(appointment_time, "%Y-%m-%d")
        register_department = int(request.POST['register_department'])  # 挂号科室
        register_type = int(request.POST['register_type'])  # 挂号类型
        optional_doctors = Doctor.objects.filter(Q(department=register_department), Q(job_title=register_type), Q(surgery=appointment_time.weekday()))
        try:
            selected_doctor = random.choice(optional_doctors)
        except:
            message1 = '预约失败!该时间无所需在诊医生!请重新选择!'
            return render(request, 'appointment_sys/index.html', locals())
        id = '%d' % (Register.objects.all().count() + 1)
        if register_type == 0:
            project_ID = Project.objects.get(id='2')
        elif register_type == 1:
            project_ID = Project.objects.get(id='3')
        Register.objects.create(
            id=id,
            doctor_id=selected_doctor,
            patient_id=Patient.objects.get(id=request.session['user_id']),
            department=register_department,
            project=project_ID  # 项目表未创建，创建后需改动
        )
        message1 = '预约成功!'
        return render(request, 'appointment_sys/index.html', locals())



