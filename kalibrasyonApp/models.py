
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Gorev_listesi(models.Model):
    # görev listesi benzersiz
    task_number = models.CharField(verbose_name="görev numarası", max_length=200, unique=True, error_messages={
        "unique": "Görev numarası benzersiz olmalı"
    })  # görev numarası
    inventory_code = models.CharField(
        verbose_name="envanter kodu", max_length=200, blank=True, null=True)  # envanter kodu
    inventory_type = models.CharField(
        verbose_name="envanter tipi", max_length=200, blank=True, null=True)  # envanter tipi
    inventory_sub_type = models.CharField(
        verbose_name="envanter alt tipi", max_length=200, blank=True, null=True)  # envanter alt tipi
    device_brand = models.CharField(
        verbose_name="marka", max_length=200, blank=True, null=True)  # marka
    device_model = models.CharField(
        verbose_name="model", max_length=200, blank=True, null=True)  # model
    serial_number = models.CharField(
        verbose_name="seri numarası", max_length=200, blank=True, null=True)  # seri numarası
    task_type = models.CharField(
        verbose_name="görev tipi", max_length=200, blank=True, null=True)  # görev tipi
    task_name = models.CharField(
        verbose_name="görev adı", max_length=200, blank=True, null=True)  # görev adı
    plan_date = models.DateField(verbose_name="plan tarih", auto_now=False,
                                 auto_now_add=False, blank=True, null=True)  # plan tarih
    task_status = models.CharField(
        verbose_name="görev durumu", max_length=200, blank=True, null=True)  # görev durumu
    explanation = models.CharField(
        verbose_name="açıklama", max_length=200, blank=True, null=True)  # açıklama
    liable_type = models.CharField(
        verbose_name="sorumlu tipi", max_length=200, blank=True, null=True)  # sorumlu tipi
    responsible = models.CharField(
        verbose_name="sorumlu kişi", max_length=200, blank=True, null=True)  # sorumlu kişi
    completion_date = models.DateField(
        verbose_name="tamamlama tarih", blank=True, null=True)  # tamamlama tarih
    branch = models.CharField(
        verbose_name="şube", max_length=200, blank=True, null=True)  # şube
    branch_building = models.CharField(
        verbose_name="bina", max_length=200, blank=True, null=True)  # bina
    building_floor = models.CharField(
        verbose_name="kat", max_length=200, blank=True, null=True)  # kat
    location = models.CharField(
        verbose_name="konum", max_length=200, blank=True, null=True)  # konum
    person_doing = models.CharField(
        verbose_name="yapan kişi", max_length=200, blank=True, null=True)  # yapan kişi
    label = models.BooleanField(verbose_name="etiket", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:

        return f"Görev numarası: {self.task_number}, Envanter numrası: {self.inventory_code}, Envanter tipi: {self.inventory_type},Marka: {self.device_brand}, Model: {self.device_model}, Serinumrası: {self.serial_number}, Konum {self.location}, Şube: {self.branch}"

    class Meta:
        verbose_name = "görev listesi"
        verbose_name_plural = "görev listesi"

    # kullanıcadan bire çok ilişki


class Kalibrator_listesi(models.Model):
    inventory_code = models.CharField(
        verbose_name="envanter kodu", max_length=200, blank=True, null=True)  # envanter kodu
    inventory_type = models.CharField(
        verbose_name="envanter tipi", max_length=200, blank=True, null=True)  # envanter tipi
    inventory_sub_type = models.CharField(
        verbose_name="envanter alt tipi", max_length=200, blank=True, null=True)  # envanter alt tipi
    device_brand = models.CharField(
        verbose_name="marka", max_length=200, blank=True, null=True)  # marka
    device_model = models.CharField(
        verbose_name="model", max_length=200, blank=True, null=True)  # model
    serial_number = models.CharField(
        verbose_name="seri numarası", max_length=200, blank=True, null=True)  # seri numarası
    period_of_validity=models.DateField(verbose_name="geçerlilik süresi", auto_now=False,
                                 auto_now_add=False, blank=True, null=True)
    traceability=models.CharField(verbose_name="izlenebilirlik",blank=True, null=True, max_length=200)

    def __str__(self):
        return f"Envanter numrası: {self.inventory_code},  Envanter tipi: {self.inventory_type},Marka: {self.device_brand}, Model: {self.device_model}, Serinumrası: {self.serial_number}"

    class Meta:
        verbose_name = "kalibratör listesi"
        verbose_name_plural = "kalibratör listesi"


class Sablon_Adı(models.Model):
    template_name = models.CharField(

        verbose_name="şablon adı", max_length=200, blank=True, null=True)
    template_test=models.JSONField(blank=True,null=True)
    calibrator=models.ManyToManyField(Kalibrator_listesi)
    def __str__(self) -> str:
        return f"Şablon adı:{self.template_name} Kalibratör adı:{self.calibrator}"

    class Meta:
        verbose_name = "şablon adı"
        verbose_name_plural = "şablon adı"


class Sablon_olustur(models.Model):

 
    test_name = models.CharField(
        verbose_name="Test adı", max_length=200, blank=True, null=True)

    set_test = models.CharField(
        verbose_name="ayarlanan", max_length=200,blank=True,null=True)
    # input1=models.BooleanField(verbose_name="input1",default=False,blank=True)
    # input2=models.BooleanField(verbose_name="input2",default=False,blank=True)
    # chackBox=models.BooleanField(verbose_name="chackbox",default=False,blank=True)
    template_name = models.ForeignKey(Sablon_Adı, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"Test adı: {self.test_name}, Ayarlanan: {self.set_test}"
    class Meta:
        verbose_name = "şablon oluştur"
        verbose_name_plural = "şablon oluştur"

# yapılan iş
class Finished_task(models.Model):
    fs = FileSystemStorage(location='/media/photos')
    task_number = models.CharField(verbose_name="görev numarası", max_length=200, unique=True, error_messages={
        "unique": "Görev numarası benzersiz olmalı"
    })  # görev numarası
    inventory_code = models.CharField(
        verbose_name="envanter kodu", max_length=200, blank=True, null=True)  # envanter kodu
    inventory_type = models.CharField(
        verbose_name="envanter tipi", max_length=200, blank=True, null=True)  # envanter tipi
    inventory_sub_type = models.CharField(
        verbose_name="envanter alt tipi", max_length=200, blank=True, null=True)  # envanter alt tipi
    device_brand = models.CharField(
        verbose_name="marka", max_length=200, blank=True, null=True)  # marka
    device_model = models.CharField(
        verbose_name="model", max_length=200, blank=True, null=True)  # model
    serial_number = models.CharField(
        verbose_name="seri numarası", max_length=200, blank=True, null=True)  # seri numarası
    task_type = models.CharField(
        verbose_name="görev tipi", max_length=200, blank=True, null=True)  # görev tipi
    task_name = models.CharField(
        verbose_name="görev adı", max_length=200, blank=True, null=True)  # görev adı
    plan_date = models.DateField(verbose_name="plan tarih", auto_now=False,
                                 auto_now_add=False, blank=True, null=True)  # plan tarih
    task_status = models.CharField(
        verbose_name="görev durumu", max_length=200, blank=True, null=True)  # görev durumu
    explanation = models.CharField(
        verbose_name="açıklama", max_length=200, blank=True, null=True)  # açıklama
    liable_type = models.CharField(
        verbose_name="sorumlu tipi", max_length=200, blank=True, null=True)  # sorumlu tipi
    responsible = models.CharField(
        verbose_name="sorumlu kişi", max_length=200, blank=True, null=True)  # sorumlu kişi
    completion_date = models.DateField(
        verbose_name="tamamlama tarih", blank=True, null=True)  # tamamlama tarih
    branch = models.CharField(
        verbose_name="şube", max_length=200, blank=True, null=True)  # şube
    branch_building = models.CharField(
        verbose_name="bina", max_length=200, blank=True, null=True)  # bina
    building_floor = models.CharField(
        verbose_name="kat", max_length=200, blank=True, null=True)  # kat
    location = models.CharField(
        verbose_name="konum", max_length=200, blank=True, null=True)  # konum
    person_doing = models.CharField(
        verbose_name="yapan kişi", max_length=200, blank=True, null=True)  # yapan kişi
    label = models.BooleanField(verbose_name="etiket", blank=True, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    test_start_date=models.CharField(verbose_name="Test başlangıç tarihi", max_length=200, blank=True, null=True)
    test_end_date=models.CharField(verbose_name="Test bitiş tarihi", max_length=200, blank=True, null=True)
    device_image=models.ImageField(upload_to='media/',max_length=900,blank=True,null=True)
    functionTest=models.JSONField(verbose_name="Fonksiyon Testi",blank=True,null=True)
    measurement_result=models.JSONField(verbose_name="Ölçüm sonucu",blank=True,null=True)
    calibratorData=models.JSONField(verbose_name="Kalibratör datası",blank=True,null=True)
    class Meta:
        verbose_name = "Biten iş"
        verbose_name_plural = "Biten iş"