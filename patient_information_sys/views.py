from django.shortcuts import render
from django.http import HttpResponse, Http404
import re
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

# Create your views here.


from HIS.models import Patient, Doctor, Project, Register, Prescription, Inspection, Operation, Medicine, Hospitalized, Rounds


def index(request):  # 查询首页
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    elif request.session['is_login']:
        return render(request, 'patient_information_sys/index.html')


def modify(request):  # 病人修改自身信息
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    if request.method == 'GET':
        if request.session['user_attr'] != 0:
            message1 = '没有权限！'
            return render(request, 'patient_information_sys/index.html', locals())
        patient = Patient.objects.get(id=request.session['user_id'])
        context = {'patient': patient}
        return render(request, 'patient_information_sys/modify.html', context=context)
    elif request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        # age = request.POST['age']
        # id_number = request.POST['id_number']
        phone = request.POST['phone']
        emergency_contact = request.POST['emergency_contact']
        address = request.POST['address']
        # 判断修改内容的格式是否正确（未实现）
        Patient.objects.filter(id=request.session['user_id']).update(
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


def search_result_for_doctor(request):  # 医生查询病人信息
    if not request.session.get('is_login', None):
        raise Http404('未登录')
    if request.method == 'GET':
        if request.session['user_attr'] != 0:
            message1 = '没有权限！'
            return render(request, 'patient_information_sys/index.html', locals())
        else:
            return render(request, 'patient_information_sys/search_result_for_doctor.html')
    elif request.method == 'POST':
        if request.session['user_attr'] != 0 and request.session['user_attr'] != 1:
            message2 = '没有权限！'
            return render(request, 'patient_information_sys/index.html', locals())
        try:
            patient_id = request.POST['patient_id']
        except:
            if request.session['user_attr'] == 1:
                patient_id = request.session['search_patient_id']
            elif request.session['user_attr'] == 0:
                patient_id = request.session['user_id']
        if not patient_id:
            message2 = '请输入病人id'
            return render(request, 'patient_information_sys/index.html', locals())
        elif not re.match(r"pat\d{6}", patient_id):
            message2 = '请输入正确格式的病人id'
            return render(request, 'patient_information_sys/index.html', locals())
        else:
            if request.session['user_attr'] == 1:
                request.session['search_patient_id'] = patient_id
            try:
                patient = Patient.objects.get(id=patient_id)
            except:
                message2 = '不存在编号为%s的患者' % patient_id
                return render(request, 'patient_information_sys/index.html', locals())
            else:
                type_dict = {"register": Register,
                             "prescription": Prescription,
                             "inspection": Inspection,
                             "operation": Operation,
                             "medicine": Medicine,
                             "hospitalized": Hospitalized,
                             "rounds": Rounds
                             }
                information_type = request.POST['information_type']
                try:
                    query_method = request.POST['query_method']
                except:
                    query_method = 'time_order'
                if query_method == 'all':
                    if information_type != "inspection" and information_type != "medicine":
                        data = type_dict[information_type].objects.filter(patient_id=patient_id)
                        message_num = len(data)
                        context = {'data': data, 'message_num': message_num, 'information_type': information_type}
                        return render(request, 'patient_information_sys/search_result_for_doctor.html', context=context)
                    else:
                        l1 = Prescription.objects.filter(patient_id=patient_id)
                        data = []
                        for i in l1:
                            for j in type_dict[information_type].objects.filter(prescription_id=i.id):
                                data.append(j)
                        message_num = len(data)
                        context = {'data': data, 'message_num': message_num, 'information_type': information_type}
                        return render(request, 'patient_information_sys/search_result_for_doctor.html', context=context)
                elif query_method == 'time_order':
                    current_tz = timezone.get_current_timezone()  # 时区
                    start_time = request.POST['start_time']
                    start_time = datetime.strptime(start_time, "%Y-%m-%d")  # 转化为datetime
                    start_time = current_tz.localize(start_time)  # 加上时区
                    end_time = request.POST['end_time']
                    end_time = datetime.strptime(end_time, "%Y-%m-%d")  # 转化为datetime
                    end_time = current_tz.localize(end_time)  # 加上时区
                    if information_type != "inspection" and information_type != "medicine":
                        data = type_dict[information_type].objects.filter(Q(patient_id=patient_id), Q(time__gte=start_time), Q(time__lte=end_time))
                        message_num = len(data)
                        context = {'data': data, 'message_num': message_num, 'information_type': information_type}
                        return render(request, 'patient_information_sys/search_result_for_doctor.html', context=context)
                    else:
                        l1 = Prescription.objects.filter(patient_id=patient_id)
                        data = []
                        for i in l1:
                            for j in type_dict[information_type].objects.filter(Q(prescription_id=i.id), Q(time__gte=start_time), Q(time__lte=end_time)):
                                data.append(j)
                        message_num = len(data)
                        context = {'data': data, 'message_num': message_num, 'information_type': information_type}
                        return render(request, 'patient_information_sys/search_result_for_doctor.html', context=context)
