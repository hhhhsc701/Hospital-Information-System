from django.db import models

Status = ((0, '空'), (1, '满'))
Job_title = ((0, '普通'), (1, '专家'))
Gender_choices = ((0, '男'), (1, '女'))
Payment = ((0, '未支付'), (1, '已支付'))
Will = ((0, '允许出院'), (1, '自主出院'))
Hospitalization = ((0, '未住院'), (1, '已住院'))
Attribute = ((0, '病人'), (1, '医生'), (2, '护士'), (3, '财务人员'), (4, '药房人员'))
Department = ((0, '普通内科'), (1, '普通外科'), (2, '骨科'), (3, '儿科'), (4, '妇产科'))


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
    id_number = models.CharField(max_length=11, verbose_name='身份证号')
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
    id_number = models.CharField(max_length=11, verbose_name='身份证号')
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
    age = models.CharField(max_length=11, verbose_name='年龄')
    id_number = models.CharField(max_length=19, verbose_name='身份证号')
    phone = models.CharField(max_length=11, verbose_name='联系方式')
    emergency_contact = models.CharField(max_length=11, verbose_name='紧急联系人')
    address = models.CharField(max_length=256, verbose_name='家庭住址')
    status = models.SmallIntegerField(choices=Hospitalization, default=0, verbose_name='住院状态')

    class Meta:
        db_table = 'patient'
        verbose_name = '病人'

    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.CharField(max_length=11, verbose_name='项目编号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='项目名称')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='项目单价')

    class Meta:
        db_table = 'project'
        verbose_name = '收费项目'

    def __str__(self):
        return self.name


class Register(models.Model):
    id = models.CharField(max_length=11, verbose_name='挂号单编号', primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    department = models.SmallIntegerField(choices=Department, default=0, verbose_name='科室')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目编号')
    time = models.DateTimeField(auto_now_add=True, verbose_name='挂号时间')

    class Meta:
        db_table = 'register'
        verbose_name = '挂号单'

    def __str__(self):
        return self.time


class Bed(models.Model):
    id = models.CharField(max_length=11, verbose_name='床位', primary_key=True)
    status = models.SmallIntegerField(choices=Status, default=0, verbose_name='床位状态')

    class Meta:
        db_table = 'bed'
        verbose_name = '床位'

    def __str__(self):
        return self.id


class Hospitalized(models.Model):
    id = models.CharField(max_length=11, verbose_name='住院表编号', primary_key=True)
    bed_id = models.ForeignKey(Bed, on_delete=models.DO_NOTHING, verbose_name='床位号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    admission_time = models.DateTimeField(auto_now_add=True, verbose_name='入院时间')
    discharge_time = models.DateTimeField(verbose_name='出院时间')
    will = models.SmallIntegerField(choices=Will, default=0, verbose_name='自主出院')
    order = models.CharField(max_length=256, verbose_name='医嘱')

    class Meta:
        db_table = 'hospitalized'
        verbose_name = '住院表'

    def __str__(self):
        return self.order


class Rounds(models.Model):
    id = models.CharField(max_length=11, verbose_name='查房信息', primary_key=True)
    nurse_id = models.ForeignKey(Nurse, on_delete=models.DO_NOTHING, verbose_name='护士编号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    time = models.DateTimeField(auto_now_add=True, verbose_name='查房时间')
    information = models.CharField(max_length=256, verbose_name='查房信息')

    class Meta:
        db_table = 'rounds'
        verbose_name = '查房表'

    def __str__(self):
        return self.information


class Prescription(models.Model):
    id = models.CharField(max_length=11, verbose_name='处方单编号', primary_key=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    content = models.TextField(verbose_name='处方内容')
    annotation = models.CharField(max_length=256, verbose_name='批注')
    time = models.DateTimeField(auto_now_add=True, verbose_name='处方时间')

    class Meta:
        db_table = 'prescription'
        verbose_name = '处方单'

    def __str__(self):
        return self.content


class Operation(models.Model):
    id = models.CharField(max_length=11, verbose_name='手术单编号', primary_key=True)
    name = models.CharField(max_length=20, verbose_name='手术名称')
    prescription_id = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING, verbose_name='处方单编号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目编号')
    time = models.DateTimeField(auto_now_add=True, verbose_name='手术时间')

    class Meta:
        db_table = 'Operation'
        verbose_name = '手术'

    def __str__(self):
        return self.time


class DoctorOperation(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    operation_id = models.ForeignKey(Operation, on_delete=models.DO_NOTHING, verbose_name='手术单编号')

    class Meta:
        unique_together = ('doctor_id', 'operation_id')


class Inspection(models.Model):
    id = models.CharField(max_length=11, verbose_name='检验单编号', primary_key=True)
    prescription_id = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING, verbose_name='处方单编号')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, verbose_name='医生编号')
    project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目编号')
    name = models.CharField(max_length=20, verbose_name='检验名称')
    report = models.TextField(verbose_name='检验报告')
    time = models.DateTimeField(auto_now_add=True, verbose_name='检验时间')

    class Meta:
        db_table = 'inspection'
        verbose_name = '检验单'

    def __str__(self):
        return self.name


class Charge(models.Model):
    id = models.CharField(max_length=11, verbose_name='收费单编号', primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目编号')
    patient_id = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name='病人编号')
    number = models.IntegerField(verbose_name='项目次数')
    time = models.DateTimeField(auto_now=True, verbose_name='收费日期')
    status = models.SmallIntegerField(choices=Payment, default=0, verbose_name='缴费状态')

    class Meta:
        db_table = 'charge'
        verbose_name = '收费单'

    def __str__(self):
        return self.id


class Medicine(models.Model):
    id = models.CharField(max_length=11, verbose_name='收费单编号', primary_key=True)
    prescription_id = models.ForeignKey(Prescription, on_delete=models.DO_NOTHING, verbose_name='处方单编号')
    project_id = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目编号')
    name = models.CharField(max_length=20, verbose_name='药物名称')
    number = models.IntegerField(verbose_name='药物数目')
    text = models.TextField(verbose_name='注意事项')

    class Meta:
        db_table = 'Medicine'
        verbose_name = '取药单'

    def __str__(self):
        return self.name


class Inventory(models.Model):
    id = models.CharField(max_length=11, verbose_name='物品编号', primary_key=True)
    number = models.IntegerField(verbose_name='存货数目')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='成本')

    class Meta:
        db_table = 'inventory'
        verbose_name = '库存'

    def __str__(self):
        return self.number


class Replenishment(models.Model):
    id = models.CharField(max_length=11, verbose_name='补货单编号', primary_key=True)
    inventory_id = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, verbose_name='物品编号')
    number = models.IntegerField(verbose_name='补货数目')
    time = models.DateTimeField(auto_now=True, verbose_name='补货日期')

    class Meta:
        db_table = 'replenishment'
        verbose_name = '补货单'

    def __str__(self):
        return self.number
