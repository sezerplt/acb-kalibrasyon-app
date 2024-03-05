from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Gorev_listesi, Kalibrator_listesi, Sablon_Adı, Sablon_olustur
from django.utils.safestring import mark_safe
from django.utils.html import format_html
# date filter
import datetime
# plan date filter
from rangefilter.filters import DateRangeFilter

header = "Kalibrasyon Admin"
title = "Kalibrasyon site yönetimi"
# Register your models here.


@admin.register(Gorev_listesi)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number", "task_type", "task_name", "plan_date",
                    "task_status", "explanation", "liable_type", "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label",)
    list_filter = ("person_doing", "branch", "task_status", "task_type",
                   "branch", "responsible", ('plan_date', DateRangeFilter),)
    date_hierarchy = 'plan_date'

    AdminSite.site_header = header
    AdminSite.site_title = title


@admin.register(Kalibrator_listesi)
class CalibratorList(admin.ModelAdmin):
    list_display = ("inventory_code", "inventory_type", "inventory_sub_type",
                    "device_brand", "device_model", "serial_number","period_of_validity","traceability")
    list_filter = ("inventory_code", "inventory_type", "serial_number",("period_of_validity",DateRangeFilter),"traceability")
    date_hierarchy = 'period_of_validity'
    AdminSite.site_header = header
    AdminSite.site_title = title


@admin.register(Sablon_Adı)
class CreateAdd(admin.ModelAdmin):
    list_display = ("template_name","template_test","kalibrator_list")
    AdminSite.site_header = header
    AdminSite.site_title = title
    def kalibrator_list(self,obj):
        html="<ul>"
        for calibrator in obj.calibrator.all():
            html+=f"<li> {calibrator.inventory_code} {calibrator.inventory_type} {calibrator.inventory_sub_type} {calibrator.device_brand} {calibrator.device_model} {calibrator.serial_number}</li>"
        html+="</ul>"
        return mark_safe(html)

@admin.register(Sablon_olustur)
class CreateTemplate(admin.ModelAdmin):
    list_display = ("test_name", "set_test", "sablon_adı")
    def sablon_adı(self,obj):
        return format_html("<span>{}<span>",obj.template_name.template_name)

    AdminSite.site_header = header
    AdminSite.site_title = title
