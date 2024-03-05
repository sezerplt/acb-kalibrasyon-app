
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .form import UplaoadFileForm
from .excel_up.excel_load import excelLoad
from .excel_up.excel_export import export_data
from django.db import IntegrityError
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import Gorev_listesi, Finished_task, Kalibrator_listesi, Sablon_olustur,Sablon_Adı
from django.core.paginator import Paginator
from kalibrasyonApp.serializers import TaskSerializer, FinishedSerializer, CalibratorSerializer, TemplateSerializer,TemplateNameSerializer,UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import status
import json
from django.utils.safestring import mark_safe
import datetime
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
# from knox.auth import AuthToken


# knox Kimlik doğrulama
# class Login_api(APIView):
#     def post(self,request):
#         serializer=AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user =serializer.validated_data["user"]
#         _,token=AuthToken.objects.create(user)
#         return Response({
#             "user_info":{
#                 "id":user.id,
#                 "username":user.username,
#                 "email":user.email
#             },
#             "token":token

#         })


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
    
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class UserId(APIView):
    authentication_classes = [TokenAuthentication]
    # sadece doğrulanmış kullanıcılara izin
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    def post(self,request):
        user=User.objects.filter(username=request.data["username"])
        serializer=UserSerializer(user, many=True)

        return Response(serializer.data)
class Task_data(APIView):
    authentication_classes = [TokenAuthentication]
    # sadece doğrulanmış kullanıcılara izin
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def post(self, request):

        year = request.data["year"]
        month = request.data["month"]

        user = User.objects.get(username=request.data["id"])  # username
        data = Gorev_listesi.objects.filter(
            user=user, plan_date__month=int(month), plan_date__year=int(year))

        serializer = TaskSerializer(data, many=True)
        return Response(serializer.data)

class TemplateName(APIView):
    # authentication_classes = [TokenAuthentication]
    # sadece doğrulanmış kullanıcılara izin
    # permission_classes = [IsAuthenticated]
    serializer_class = TemplateNameSerializer
    def get(self,request):
        data=Sablon_Adı.objects.all()
        serializer=TemplateNameSerializer(data,many=True)
        return Response(serializer.data)
    
class Template_data(APIView):
    # authentication_classes = [TokenAuthentication]
    # sadece doğrulanmış kullanıcılara izin
    # permission_classes = [IsAuthenticated]
    serializer_class = TemplateSerializer

    def get(self, request):
        data = Sablon_olustur.objects.all()
        serializer = TemplateSerializer(data, many=True)
        return Response(serializer.data)


class Calibrator_data(APIView):
    # authentication_classes = [TokenAuthentication]
    # sadece doğrulanmış kullanıcılara izin
    # permission_classes = [IsAuthenticated]
    serializer_class = CalibratorSerializer

    def get(self, request):
        data = Kalibrator_listesi.objects.all()
        serializer = CalibratorSerializer(data, many=True)
        return Response(serializer.data)


class Finished_list(APIView):
    authentication_classes = [TokenAuthentication]  # TOKEN DOĞRULAMA
    # sadece doğrulanmış kullanıcılara izin
    permission_classes = [IsAuthenticated]
    serializer_class = FinishedSerializer
    parser_classes = [MultiPartParser]

    def get(self, request):
        data = Finished_task.objects.all()
        serializer = FinishedSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
       
        # data["user"]=float(data["user"])
       
        serializer = FinishedSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                task_delete = Gorev_listesi.objects.get(
                    task_number=data["task_number"])
                task_delete.delete()
            except ObjectDoesNotExist:
                return Response({"message": "görev numarası kayıtlı değil"})

            return Response(serializer.data)
        return Response(serializer.errors)

    
def home(request, username):
    superusers = User.objects.filter(is_superuser=True, username=username)

    if superusers:
        all_task_list = Gorev_listesi.objects.all()

        # tarihe göre toplam iş
        task_lists_total = Gorev_listesi.objects.all().count()
        finished_task_lists_total = Finished_task.objects.all().count()
        total_job = [['Yıl', 'Bekleyen', 'Biten']]
        date_count = all_task_list.values_list("plan_date")
        date_count_set = set()
        date_count_select = set()  # home page select
        for dateYYYY in date_count:
            date_count_set.add(dateYYYY[0].strftime("%Y"))
            date_count_select.add(dateYYYY[0].strftime("%d.%m.%Y"))
        draw_date_task = [["date", "waiting"]]
        draw_date_finished = [["date", "finished"]]

        for d in date_count_set:
            date_year_x = Gorev_listesi.objects.filter(
                plan_date__year=d).values_list("plan_date").count()
            date_year_y = Finished_task.objects.filter(
                plan_date__year=d).values_list("plan_date").count()
            total_job.append([d, date_year_x, date_year_y])

        # hastane bazlı toplam
        branch_count = all_task_list.values_list("branch")
        branch_set = set()
        for i in branch_count:
            branch_set.add(i[0])

        draw_branch_task = [['branch', 'pending task number']]
        draw_branch_finished = [['branch', 'finished task number']]
        for b in branch_set:

            branch_x = Gorev_listesi.objects.filter(
                branch=b).values_list("branch").count()
            branch_y = Finished_task.objects.filter(
                branch=b).values_list("branch").count()

            draw_branch_task.append([b, branch_x])
            draw_branch_finished.append([b, branch_y])

        # kişi bazlı iş
        user_task_total_list = [['Kullanıcı', 'Bekleyen', 'Biten']]
        user_task = all_task_list.values_list("person_doing")

        for u in set(user_task):
            user_task_total = Gorev_listesi.objects.filter(
                person_doing=u[0]).values_list("person_doing").count()
            user_finished_total = Finished_task.objects.filter(
                person_doing=u[0]).values_list("person_doing").count()
            user_task_total_list.append(
                [u[0], user_task_total, user_finished_total])
        # select data
        if request.method == "POST":
            branch_select = request.POST["branch_select"]
            plan_date_select = request.POST["plan_date_select"]
            plan_date_select_dd = plan_date_select[0:2]
            plan_date_select_mm = plan_date_select[3:5]
            plan_date_select_yy = plan_date_select[6:10]
            plan_date_select_full = datetime.date(year=int(plan_date_select_yy), month=int(
                plan_date_select_mm), day=int(plan_date_select_dd))

            user_branch_task_date = [['Kullanıcı', 'Bekleyen', 'Biten']]
            for u in set(user_task):
                user_branch_filter_task = Gorev_listesi.objects.filter(
                    person_doing=u[0], branch=branch_select, plan_date=plan_date_select_full).count()
                user_branch_filter_finished = Finished_task.objects.filter(
                    person_doing=u[0], branch=branch_select, plan_date=plan_date_select_full).count()
                user_branch_task_date.append(
                    [u[0], user_branch_filter_task, user_branch_filter_finished])

        else:
            user_branch_task_date = [['Kullanıcı', 'Bekleyen', 'Biten']]
            for u in set(user_task):
                user_task_total = Gorev_listesi.objects.filter(
                    person_doing=u[0]).values_list("person_doing").count()
                user_finished_total = Finished_task.objects.filter(
                    person_doing=u[0]).values_list("person_doing").count()
                user_branch_task_date.append(
                    [u[0], user_task_total, user_finished_total])
        context = {
            "superusers": superusers,
            "bekleyen_is": task_lists_total,
            "biten_is": finished_task_lists_total,
            "hastaneler": all_task_list,
            "draw_branch_task": mark_safe(json.dumps(draw_branch_task)),
            "draw_branch_finished": mark_safe(json.dumps(draw_branch_finished)),
            "total_job": mark_safe(json.dumps(total_job)),
            "draw_date_task": mark_safe(json.dumps(draw_date_task)),
            "draw_date_finished": mark_safe(json.dumps(draw_date_finished)),
            "user_task_total_list": mark_safe(json.dumps(user_task_total_list)),
            "branch_set": branch_set,
            "date_select": date_count_select,
            "user_branch_task_date": mark_safe(json.dumps(user_branch_task_date)),
            "username": username
        }
        return render(request, "home/home.html", context=context)
    else:
        users = User.objects.filter(is_superuser=False, username=username)
        user_id = User.objects.get(username=username).id
        branch_count = Gorev_listesi.objects.filter(
            user_id=user_id).values_list("branch")
        date_count = Gorev_listesi.objects.filter(
            user_id=user_id).values_list("plan_date")
        branch_set = set()
        for i in branch_count:
            branch_set.add(i[0])
        date_count_select = set()  # home page select
        for dateYYYY in date_count:
            date_count_select.add(dateYYYY[0].strftime("%d.%m.%Y"))
        if request.method == "POST":
            branch_select = request.POST["branch_select"]
            plan_date_select = request.POST["plan_date_select"]
            plan_date_select_dd = plan_date_select[0:2]
            plan_date_select_mm = plan_date_select[3:5]
            plan_date_select_yy = plan_date_select[6:10]
            plan_date_select_full = datetime.date(year=int(plan_date_select_yy), month=int(
                plan_date_select_mm), day=int(plan_date_select_dd))
            user_branch_task_date = [['Kullanıcı', 'Bekleyen', 'Biten']]
            user_branch_filter_task = Gorev_listesi.objects.filter(
                user_id=user_id, branch=branch_select, plan_date=plan_date_select_full).count()
            user_branch_filter_finished = Finished_task.objects.filter(
                user_id=user_id, branch=branch_select, plan_date=plan_date_select_full).count()
            person_doing = Gorev_listesi.objects.filter(
                user_id=user_id).values_list("person_doing")[0][0]
            user_branch_task_date.append(
                [person_doing, user_branch_filter_task, user_branch_filter_finished])

        else:

            user_branch_task_date = [['Kullanıcı', 'Bekleyen', 'Biten']]
            user_task_total = Gorev_listesi.objects.filter(
                user_id=user_id).values_list("person_doing").count()
            user_finished_total = Finished_task.objects.filter(
                user_id=user_id).values_list("person_doing").count()
            person_doing = Gorev_listesi.objects.filter(
                user_id=user_id).values_list("person_doing")[0][0]
            user_branch_task_date.append(
                [person_doing, user_task_total, user_finished_total])

        context = {
            "username": users,
            "user_branch_task_date": mark_safe(json.dumps(user_branch_task_date)),
            "branch_set": branch_set,
            "date_select": date_count_select,
            "username": username

        }

        return render(request, "home/home.html", context=context)


def finished_task(request, username):
    page = request.GET.get("page")
    superusers = User.objects.filter(is_superuser=True, username=username)
    branch_list = Finished_task.objects.all().values_list("branch")

    # superuser
    if superusers:

        if request.method == "POST":
            if "filter" in request.POST:
                task_number = request.POST["gorevnumrasi"]
                inventory_code = request.POST["envanter-numarasi"]
                inventory_type = request.POST["envanter-tipi"]
                device_brand = request.POST["marka"]
                device_model = request.POST["model"]
                serial_number = request.POST["serino"]
                task_type = request.POST["gorev-tipi"]
                plan_date = request.POST["plan-tarih"]
                branch = request.POST["sube"]
                location = request.POST["konum"]
                # filterList=[task_number,inventory_code, inventory_type,device_brand,device_model,
                # serial_number,task_type,plan_date,branch,location]

                # getValue=Gorev_listesi.objects.get(Q(task_name=task_list) | Q(inventory_code=inventory_code))
                filters = Finished_task.objects.filter(task_number__icontains=task_number, inventory_code__icontains=inventory_code,
                                                       inventory_type__icontains=inventory_type, device_brand__icontains=device_brand, device_model__icontains=device_model,
                                                       serial_number__icontains=serial_number, task_type__icontains=task_type, plan_date__icontains=plan_date,
                                                       branch__icontains=branch,
                                                       location__icontains=location).order_by('id')

                paginsf = Paginator(filters, 20)
                task = paginsf.get_page(page)

                context = {"task_list": task,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/finished_task.html", context=context)
        elif request.method == "GET":

            if "dropdown" in request.GET:
                branch_select = request.GET["dropdown"]

                if branch_select == "branch_option":

                    ranch_full_data = Finished_task.objects.all().values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                              "task_type", "task_name", "plan_date",
                                                                              "task_status", "explanation", "liable_type",
                                                                              "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    # exceli dışa aktar
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "biten isler", ranch_full_data, header)
                    return excel_export

                else:
                    branch_data = Finished_task.objects.filter(
                        branch__icontains=branch_select).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                     "task_type", "task_name", "plan_date",
                                                                     "task_status", "explanation", "liable_type",
                                                                     "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    # exceli dışa aktar
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "biten isler", branch_data, header)
                    return excel_export

            else:
                gorevListe = Finished_task.objects.all().order_by('id')
                pagins = Paginator(gorevListe, 20)

                task = pagins.get_page(page)
                context = {"task_list": task,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/finished_task.html", context=context)
        gorevListe = Finished_task.objects.all().order_by('id')
        pagins = Paginator(gorevListe, 20)

        task = pagins.get_page(page)

        context = {"task_list": task,
                   "branch_list": branch_list, "username": username}
        return render(request, "home/finished_task.html", context=context)

    # user
    else:
        user_id = User.objects.get(is_superuser=False, username=username).id
        if request.method == "POST":
            task_number = request.POST["gorevnumrasi"]
            inventory_code = request.POST["envanter-numarasi"]
            inventory_type = request.POST["envanter-tipi"]
            device_brand = request.POST["marka"]
            device_model = request.POST["model"]
            serial_number = request.POST["serino"]
            task_type = request.POST["gorev-tipi"]
            plan_date = request.POST["plan-tarih"]
            branch = request.POST["sube"]
            location = request.POST["konum"]
            # filterList=[task_number,inventory_code, inventory_type,device_brand,device_model,
            # serial_number,task_type,plan_date,branch,location]

            # getValue=Gorev_listesi.objects.get(Q(task_name=task_list) | Q(inventory_code=inventory_code))
            filters = Finished_task.objects.filter(task_number__icontains=task_number, inventory_code__icontains=inventory_code,
                                                   inventory_type__icontains=inventory_type, device_brand__icontains=device_brand, device_model__icontains=device_model,
                                                   serial_number__icontains=serial_number, task_type__icontains=task_type, plan_date__icontains=plan_date,
                                                   branch__icontains=branch,
                                                   location__icontains=location, user_id=user_id).order_by('id')

            paginsf = Paginator(filters, 20)
            taks = paginsf.get_page(page)
            context = {"task_list": taks,
                       "branch_list": branch_list, "username": username}

            return render(request, "home/finished_task.html", context=context)
        elif request.method == "GET":
            if "dropdown" in request.GET:
                branch_select = request.GET["dropdown"]
                if branch_select == "branch_option":
                    ranch_full_data = Finished_task.objects.filter(user_id=user_id).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                                                "task_type", "task_name", "plan_date",
                                                                                                "task_status", "explanation", "liable_type",
                                                                                                "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "biten isler", ranch_full_data, header)
                    return excel_export
                else:
                    branch_data = Finished_task.objects.filter(
                        branch__icontains=branch_select, user_id=user_id).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                                      "task_type", "task_name", "plan_date",
                                                                                      "task_status", "explanation", "liable_type",
                                                                                      "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "biten isler", branch_data, header)
                    return excel_export

            else:

                userGorevList = Finished_task.objects.filter(
                    user_id=user_id).order_by('id')

                pagins = Paginator(userGorevList, 20)
                taks = pagins.get_page(page)

                context = {"task_list": taks,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/finished_task.html", context=context)

        userGorevList = Finished_task.objects.filter(
            user_id=user_id).order_by('id')
        pagins = Paginator(userGorevList, 20)
        taks = pagins.get_page(page)
        context = {"task_list": taks,
                   "branch_list": branch_list, "username": username}

        return render(request, "home/finished_task.html", context=context)


def task_list(request, username):
    page = request.GET.get("page")
    superusers = User.objects.filter(is_superuser=True, username=username)
    branch_list = Gorev_listesi.objects.all().values_list("branch")
    # superuser
    if superusers:

        if request.method == "POST":
            if "filter" in request.POST:
                task_number = request.POST["gorevnumrasi"]
                inventory_code = request.POST["envanter-numarasi"]
                inventory_type = request.POST["envanter-tipi"]
                device_brand = request.POST["marka"]
                device_model = request.POST["model"]
                serial_number = request.POST["serino"]
                task_type = request.POST["gorev-tipi"]
                plan_date = request.POST["plan-tarih"]
                branch = request.POST["sube"]
                location = request.POST["konum"]
                # filterList=[task_number,inventory_code, inventory_type,device_brand,device_model,
                # serial_number,task_type,plan_date,branch,location]

                # getValue=Gorev_listesi.objects.get(Q(task_name=task_list) | Q(inventory_code=inventory_code))
                filters = Gorev_listesi.objects.filter(task_number__icontains=task_number, inventory_code__icontains=inventory_code,
                                                       inventory_type__icontains=inventory_type, device_brand__icontains=device_brand, device_model__icontains=device_model,
                                                       serial_number__icontains=serial_number, task_type__icontains=task_type, plan_date__icontains=plan_date,
                                                       branch__icontains=branch,
                                                       location__icontains=location).order_by('id')

                paginsf = Paginator(filters, 20)
                task = paginsf.get_page(page)

                context = {"task_list": task,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/task_list.html", context=context)
        elif request.method == "GET":

            if "dropdown" in request.GET:
                branch_select = request.GET["dropdown"]

                if branch_select == "branch_option":

                    ranch_full_data = Gorev_listesi.objects.all().values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                              "task_type", "task_name", "plan_date",
                                                                              "task_status", "explanation", "liable_type",
                                                                              "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    # exceli dışa aktar
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "bekleyen isler", ranch_full_data, header)
                    return excel_export

                else:
                    branch_data = Gorev_listesi.objects.filter(
                        branch__icontains=branch_select).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                     "task_type", "task_name", "plan_date",
                                                                     "task_status", "explanation", "liable_type",
                                                                     "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    # exceli dışa aktar
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "bekleyen isler", branch_data, header)
                    return excel_export

            else:
                gorevListe = Gorev_listesi.objects.all().order_by('id')
                pagins = Paginator(gorevListe, 20)

                task = pagins.get_page(page)
                context = {"task_list": task,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/task_list.html", context=context)

        gorevListe = Gorev_listesi.objects.all().order_by('id')
        pagins = Paginator(gorevListe, 20)

        task = pagins.get_page(page)
        context = {"task_list": task,
                   "branch_list": branch_list, "username": username}

        return render(request, "home/task_list.html", context=context)

    # user
    else:
        user_id = User.objects.get(username=username).id
        if request.method == "POST":
            task_number = request.POST["gorevnumrasi"]
            inventory_code = request.POST["envanter-numarasi"]
            inventory_type = request.POST["envanter-tipi"]
            device_brand = request.POST["marka"]
            device_model = request.POST["model"]
            serial_number = request.POST["serino"]
            task_type = request.POST["gorev-tipi"]
            plan_date = request.POST["plan-tarih"]
            branch = request.POST["sube"]
            location = request.POST["konum"]
            # filterList=[task_number,inventory_code, inventory_type,device_brand,device_model,
            # serial_number,task_type,plan_date,branch,location]

            # getValue=Gorev_listesi.objects.get(Q(task_name=task_list) | Q(inventory_code=inventory_code))
            filters = Gorev_listesi.objects.filter(task_number__icontains=task_number, inventory_code__icontains=inventory_code,
                                                   inventory_type__icontains=inventory_type, device_brand__icontains=device_brand, device_model__icontains=device_model,
                                                   serial_number__icontains=serial_number, task_type__icontains=task_type, plan_date__icontains=plan_date,
                                                   branch__icontains=branch,
                                                   location__icontains=location, user_id=user_id).order_by('id')

            paginsf = Paginator(filters, 20)
            taks = paginsf.get_page(page)
            context = {"task_list": taks,
                       "branch_list": branch_list, "username": username}

            return render(request, "home/task_list.html", context=context)
        elif request.method == "GET":
            if "dropdown" in request.GET:
                branch_select = request.GET["dropdown"]
                if branch_select == "branch_option":
                    ranch_full_data = Gorev_listesi.objects.filter(user_id=user_id).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                                                "task_type", "task_name", "plan_date",
                                                                                                "task_status", "explanation", "liable_type",
                                                                                                "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "bekleyen isler", ranch_full_data, header)
                    return excel_export
                else:
                    branch_data = Gorev_listesi.objects.filter(
                        branch__icontains=branch_select, user_id=user_id).values_list("task_number", "inventory_code", "inventory_type", "inventory_sub_type", "device_brand", "device_model", "serial_number",
                                                                                      "task_type", "task_name", "plan_date",
                                                                                      "task_status", "explanation", "liable_type",
                                                                                      "responsible", "completion_date", "branch", "branch_building", "building_floor", "location", "person_doing", "label")
                    header = ["Görev Numarası", "Envanter Kodu", "Envanter Tipi", "Envanter Alt Tipi", "Marka", "Model", "Seri No",
                              "Görev Tipi", "Görev Adı", "Plan Tarihi",
                              "Durum", "Açıklama", "Sorumlu Tipi",
                              "Sorumlu Kişi", "Tamamlanma Tarihi", "Şube", "Bina", "Kat", "Konum", "Yapan Kişi", "Etiket"]
                    excel_export = export_data(
                        "bekleyen isler", branch_data, header)
                    return excel_export

            else:

                userGorevList = Gorev_listesi.objects.filter(
                    user_id=user_id).order_by('id')
                pagins = Paginator(userGorevList, 20)
                taks = pagins.get_page(page)
                context = {"task_list": taks,
                           "branch_list": branch_list, "username": username}
                return render(request, "home/task_list.html", context=context)
        userGorevList = Gorev_listesi.objects.filter(
            user_id=user_id).order_by('id')
        pagins = Paginator(userGorevList, 20)
        taks = pagins.get_page(page)
        context = {"task_list": taks,
                   "branch_list": branch_list, "username": username}

        return render(request, "home/task_list.html", context=context)


def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect(f"/kalibrasyonApp/home/{user.get_username()}")
        else:
            return render(request, "account/login.html", {
                "error": "Kullanıcı adı veya şifre yanlış"
            })
    return render(request, "account/login.html")


def logout_request(request):
    logout(request)
    return redirect("/")


def excel_upload(request):
    if request.method == "POST":
        form = UplaoadFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:

                excelLoad(request.FILES["file"])
            except IntegrityError:
                IntegrityError_message = "Görev numarası kayıtlı bulundu"
                return render(request, "FileUpdate/excel_upload.html", {"form": form, "IntegrityError_message": IntegrityError_message})
            except ValueError:
                date_format_error = "Tarih formatı dd.mm.yyyy düzeninde olmalı"
                return render(request, "FileUpdate/excel_upload.html", {"form": form, "date_format_error": date_format_error})
            except IndexError:
                index_error = "Eksik veya fazla sütun bulunmaktadır"
                return render(request, "FileUpdate/excel_upload.html", {"form": form, "index_error": index_error})
            except User.DoesNotExist:
                user_error = "Yapan kişilerden veri tabınında kayıt edilmeyen bulundu"
                return render(request, "FileUpdate/excel_upload.html", {"form": form, "user_error": user_error})
            except Exception as excep:
                return render(request, "FileUpdate/excel_upload.html", {"form": form, "user_error": excep})
            return redirect("/admin/")
    else:
        form = UplaoadFileForm()
        return render(request, "FileUpdate/excel_upload.html", {"form": form})


def measurement(request, username, taskname):
    superuser = User.objects.filter(is_superuser=True, username=username)
    if superuser:

        finish_task_measurement = Finished_task.objects.filter(task_number=taskname)
        context = {"measurement": finish_task_measurement, "username": username}
        return render(request, "measurement/measurement.html", context=context)
    else:
        finish_task_measurement = Finished_task.objects.filter(task_number=taskname)
        context = {"measurement": finish_task_measurement, "username": username}

        return render(request, "measurement/measurement.html", context=context)
