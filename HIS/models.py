from django.db import models

Gender_choices = ((0, 'male'), (1, 'female'))
Department = ((0, '普通内科'), (1, '普通外科'), (2, '骨科'), (3, '儿科'), (4, '妇产科'))
Job_title = ((0, '普通'), (1, '专家'))
Attribute = ((0, '病人'), (1, '医生'), (2, '护士'), (3, '财务人员'), (4, '药房人员'))
Hospitalization = ((0, '未住院'), (1, '已住院'))


class User(models.Model):
    id = models.CharField(max_length=11, verbose_name='用户编号', primary_key=True)
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=20, verbose_name='密码')
    attr = models.SmallIntegerField(choices=Attribute, default=0, verbose_name='人员属性')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'

    def __str__(self):
        return self.username


class Doctor(models.Model):
    id = models.CharField(max_length=11, verbose_name='医生编号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    age = models.SmallIntegerField(verbose_name='年龄')
    id_num = models.CharField(max_length=11, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='联系方式')
    department = models.SmallIntegerField(choices=Department, default=0, verbose_name='科室')
    job_title = models.SmallIntegerField(choices=Job_title, default=0, verbose_name='职称')

    class Meta:
        db_table = 'doctor'
        verbose_name = '医生'

    def __str__(self):
        return self.name


class Nurse(models.Model):
    id = models.CharField(max_length=11, verbose_name='护士编号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    id_num = models.CharField(max_length=11, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        db_table = 'nurse'
        verbose_name = '护士'

    def __str__(self):
        return self.name


class Patient(models.Model):
    id = models.CharField(max_length=11, verbose_name='病人编号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    id_num = models.CharField(max_length=11, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='联系方式')
    emergency_contact = models.CharField(max_length=11, verbose_name='紧急联系人')
    address = models.CharField(max_length=256, verbose_name='家庭住址')
    status = models.SmallIntegerField(choices=Hospitalization, default=0, verbose_name='住院状态')

    class Meta:
        db_table = 'patient'
        verbose_name = '病人'

    def __str__(self):
        return self.name


class Register(models.Model):
    id = models.CharField(max_length=11, verbose_name='挂号单编号', primary_key=True)
    d_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    p_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    department = models.SmallIntegerField(choices=Department, default=0, verbose_name='科室')
    time = models.DateTimeField(auto_now_add=True, verbose_name='挂号时间')

    class Meta:
        db_table = 'register'
        verbose_name = '挂号单'

    def __str__(self):
        return self.id