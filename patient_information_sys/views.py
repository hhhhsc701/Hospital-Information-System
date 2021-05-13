from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.


from HIS.models import Patient, Register


def index(request):  # 查询首页
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    elif request.session['is_login']:
        return render(request, 'patient_information_sys/index.html')


def modify(request):  # 病人修改自身信息
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    if request.method == 'GET':
        if request.session['user_attr'] == 1:
            return render(request, 'patient_information_sys/modify.html')
        patient = Patient.objects.get(id=request.session['user_id'])
        context = {'patient': patient}
        return render(request, 'patient_information_sys/modify.html', context=context)
    elif request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        print(gender, type(gender))
        # age = request.POST['age']
        # id_number = request.POST['id_number']
        phone = request.POST['phone']
        emergency_contact = request.POST['emergency_contact']
        address = request.POST['address']
        patient = Patient.objects.get(id=request.session['user_id'])
        # 判断修改内容的格式是否正确
        Patient.objects.update(
            name=name,
            gender=gender,
            # age=age,
            # id_number=id_number,
            phone=phone,
            emergency_contact=emergency_contact,
            address=address
        )
        patient = Patient.objects.get(id=request.session['user_id'])
        context = {'patient': patient, 'message': '修改成功！'}
        return render(request, 'patient_information_sys/modify.html', context=context)


def search_for_patient(request):  # 医生查询
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    # return render(request, 'patient_information_sys/search_for_patient.html')
    return render(request, 'patient_information_sys/hospitalization.html')


def search_for_doctor_enter(request):  #
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    if request.method == 'GET':
        return render(request, 'patient_information_sys/search_for_doctor_enter.html')
    elif request.method == 'POST':
        try:
            id = request.POST['id']
            patient = Patient.objects.get(id=id)
        except:
            message = '不存在编号为'+id+'的患者'
            return render(request, 'patient_information_sys/search_for_doctor_enter.html', locals())
        else:
            request.session['search_id'] = id
            return render(request, 'patient_information_sys/search_for_doctor_option.html')


def search_for_doctor_option(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/search_for_doctor_option.html')


def register_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    context = {'data': Register.objects.filter(patient_id=request.session['search_id'])}
    return render(request, 'patient_information_sys/register_information.html', context=context)


def prescription_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    context = {'data': Register.objects.get(patient_id=request.session['search_id'])}
    return render(request, 'patient_information_sys/prescription_information.html', context=context)


def inspection_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/inspection_information.html')


def operation_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/operation_information.html')


def medicine_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/medicine_information.html')


def hospitalized_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/hospitalized_information.html')


def rounds_information(request):
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    return render(request, 'patient_information_sys/rounds_information.html')

