from django.db import models

Gender_choices = ((0, 'male'), (1, 'female'))


class Doctor(models.Model):
    d_id = models.CharField(max_length=11, verbose_name='医生编号', primary_key=True)
    d_name = models.CharField(max_length=20, verbose_name='姓名')
    d_gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    d_age = models.IntegerField(verbose_name='年龄')
    d_id_num = models.CharField(max_length=11, verbose_name='身份证号')
    d_phone = models.CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        db_table = 'doctor'
        verbose_name = '医生'

    def __str__(self):
        return self.d_name


class Nurse(models.Model):
    n_id = models.CharField(max_length=11, verbose_name='护士编号', primary_key=True)
    n_name = models.CharField(max_length=20, verbose_name='姓名')
    n_gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    n_age = models.IntegerField(verbose_name='年龄')
    n_id_num = models.CharField(max_length=11, verbose_name='身份证号')
    n_phone = models.CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        db_table = 'nurse'
        verbose_name = '护士'

    def __str__(self):
        return self.n_name


class Patient(models.Model):
    p_id = models.CharField(max_length=11, verbose_name='病人编号', primary_key=True)
    p_name = models.CharField(max_length=20, verbose_name='姓名')
    p_gender = models.SmallIntegerField(choices=Gender_choices, default=0, verbose_name='性别')
    p_age = models.IntegerField(verbose_name='年龄')
    p_id_num = models.CharField(max_length=11, verbose_name='身份证号')
    p_phone = models.CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        db_table = 'nurse'
        verbose_name = '护士'

    def __str__(self):
        return self.p_name