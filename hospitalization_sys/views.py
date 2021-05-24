from django.utils import timezone
from django.shortcuts import render
from HIS.models import Rounds, Patient, Hospitalized, Nurse, Bed, Doctor
from django.http import HttpResponse, Http404


# Create your views here.
def index(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    elif request.session['is_login']:  # 如果已经登录，则直接跳转到登陆后首页
        if request.method == 'GET':
            bed_id = Bed.objects.filter(status=0).all()
            bed_id = [bed.id[-3:] for bed in bed_id]
            return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})
        else:
            if 'enter' in request.POST:
                if request.session['user_attr'] == 1:
                    patient_id = request.POST.get('patient_id')
                    bed_id = 'bed000' + request.POST.get('bed_id')
                    patient = Hospitalized.objects.filter(patient_id_id=patient_id, will__in=[0, 2]).all()
                    if patient.exists():
                        # 已住院!
                        pass
                    else:
                        Bed.objects.filter(id=bed_id).update(status=1)
                        Hospitalized.objects.create(
                            id='hos' + "{:0>6}".format(Hospitalized.objects.all().count() + 1),
                            bed_id=Bed.objects.get(id=bed_id),
                            patient_id_id=patient_id,
                            doctor_id=Doctor.objects.get(id=request.session['user_id']),
                        )
                        # 入住成功！
                else:
                    # 没有权限
                    pass
            elif 'apply' in request.POST:
                if request.session['user_attr'] == 0:
                    patient_id = request.session['user_id']
                    try:
                        hospitalized = Hospitalized.objects.get(patient_id_id=patient_id, will=0)
                        hospitalized.will = 2
                        hospitalized.save()
                        print('申请成功')
                    except Hospitalized.DoesNotExist:
                        # 已出院，已申请
                        pass
            bed_id = Bed.objects.filter(status=0).all()
            bed_id = [bed.id[-3:] for bed in bed_id]
            return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})


def search_round_for_nurse(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    if request.method == 'GET':
        if request.session['user_attr'] == 2:
            return render(request, 'hospitalization_sys/search_rounds_for_nurse.html')
        else:
            # 弹窗
            bed_id = Bed.objects.filter(status=0).all()
            bed_id = [bed.id[-3:] for bed in bed_id]
            return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})
    elif request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        time = request.POST.get('date')
        message1 = request.POST.get('message1')
        message2 = request.POST.get('message2')
        message3 = request.POST.get('message3')
        message0 = request.POST.get('message0')
        Rounds.objects.create(
            id=Rounds.objects.all().count() + 1,
            nurse_id=Nurse.objects.get(id=request.session['user_id']),
            patient_id=Patient.objects.get(id=patient_id),
            time=time,
            information='体温：' + message1 + '\n' +
                        '血压：' + message2 + '\n' +
                        '脉搏：' + message3 + '\n' +
                        '其它：' + message0
        )
        return render(request, 'hospitalization_sys/index.html')


def search_discharge(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    if request.session['user_attr'] != 1:
        # 弹窗
        bed_id = Bed.objects.filter(status=0).all()
        bed_id = [bed.id[-3:] for bed in bed_id]
        return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})
    patient_id_0 = Hospitalized.objects.filter(doctor_id=request.session['user_id'], will=0).all()
    patient_id_2 = Hospitalized.objects.filter(doctor_id=request.session['user_id'], will=2).all()
    if request.method == 'GET':
        return render(request, 'hospitalization_sys/search_discharge.html',
                      context={'patient_id_0': patient_id_0, 'patient_id_2': patient_id_2})
    elif request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        date = request.POST.get('date')
        order = request.POST.get('order')
        Bed.objects.filter(id=Hospitalized.objects.get(patient_id_id=patient_id, will=0).bed_id_id).update(
            status=0)
        Hospitalized.objects.filter(patient_id_id=patient_id, will=0).update(discharge_time=date, order=order, will=3)
        return render(request, 'hospitalization_sys/search_discharge.html',
                      context={'patient_id_0': patient_id_0, 'patient_id_2': patient_id_2})


def process_apply_discharge(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    if request.method == 'GET':
        patient_id = request.GET.get('id')
        return render(request, 'hospitalization_sys/process_apply_discharge.html',
                      context={'patient_id': patient_id})
    elif request.method == 'POST':
        order = request.POST.get('order')
        if 'allow' in request.POST:
            patient_id = request.POST.get('allow')
            Bed.objects.filter(id=Hospitalized.objects.get(patient_id_id=patient_id, will=2).bed_id_id).update(
                status=0)
            Hospitalized.objects.filter(patient_id_id=patient_id, will=2). \
                update(order=order, will=1)
        elif 'refuse' in request.POST:
            patient_id = request.POST.get('refuse')
            Hospitalized.objects.filter(patient_id_id=patient_id, will=2).update(order=order, will=0)
        patient_id_0 = Hospitalized.objects.filter(doctor_id=request.session['user_id'], will=0).all()
        patient_id_2 = Hospitalized.objects.filter(doctor_id=request.session['user_id'], will=2).all()
        return render(request, 'hospitalization_sys/search_discharge.html',
                      context={'patient_id_0': patient_id_0, 'patient_id_2': patient_id_2})


def discharge_process(request):
    if not request.session.get('is_login', None):
        return render(request, 'users/index.html')
    if request.session['user_attr'] != 0:
        # 无权限
        return index(request)
    if request.method == 'GET':
        patient = Hospitalized.objects.filter(patient_id_id=request.session['user_id'], discharge_time__isnull=True)
        if patient.exists():
            if patient[0].will <= 1:
                return render(request, 'hospitalization_sys/discharge_process.html', context={'patient': patient[0]})
            if patient[0].will == 2:
                print('申请中')
        else:
            print('已出院')
        bed_id = Bed.objects.filter(status=0).all()
        bed_id = [bed.id[-3:] for bed in bed_id]
        return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})
    else:
        if 'confirm' in request.POST:
            Hospitalized.objects.filter(patient_id_id=request.session['user_id'], discharge_time__isnull=True). \
                update(discharge_time=timezone.now())
            bed_id = Bed.objects.filter(status=0).all()
            bed_id = [bed.id[-3:] for bed in bed_id]
            return render(request, 'hospitalization_sys/index.html', context={'bed_id': bed_id})
