from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Finished_task,Gorev_listesi,Kalibrator_listesi,Sablon_olustur,Sablon_Adı


class TemplateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sablon_Adı
        fields=["id","template_name","calibrator"]

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sablon_olustur
        # fields=["id","test_choices","test_name","set_test","measurement_result","measurement_result_2","template_name"]
        fields=["id","test_name","set_test","template_name"]
class CalibratorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Kalibrator_listesi
        fields=["id","inventory_code","inventory_type","inventory_sub_type","device_brand",
        "device_model","serial_number","period_of_validity",
        "traceability"]

class FinishedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finished_task
        fields = ["task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number", "task_type", "task_name", "plan_date", "task_status", "explanation", "liable_type", "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label", "user","test_start_date","test_end_date",
                  'device_image','functionTest','measurement_result','calibratorData']
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gorev_listesi
        fields = ["task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number", "task_type", "task_name", "plan_date", "task_status", "explanation", "liable_type", "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label", "user"]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'first_name', 'last_name', 'email']