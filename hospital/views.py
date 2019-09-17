from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import models as m
import json
from django.http import JsonResponse
from django.contrib import auth
import requests
import datetime
from django.core import serializers
from accounts.models import User


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin/dashboard/")
        elif request.user.is_staff:
            return HttpResponseRedirect("/staff/dashboard/")
        else:
            return HttpResponseRedirect("/dashboard/")
    return render(request, "index.html")


def login_admin_api(request):
    if request.method == "POST" and request.is_ajax():
        username = request.POST.get("username", False)
        password = request.POST.get("password", False)

        user = auth.authenticate(username=username, password=password)
        if user and user.is_staff:
            auth.login(request, user)
            return JsonResponse({"success": "You have successfully logged in. You are now being redirected"},
                                status=200)
        elif user and not user.is_staff:
            return JsonResponse({"error": "You don't have admin access. Try Login in as a patient"},
                                status=401)
        return JsonResponse({"error": "Your username or password is incorrect"}, status=400)
    return JsonResponse({"error": "You can't send GET Requests to this link"}, status=403)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def confirm_patient_api(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get("patient_id", False)
        if id:
            try:
                u = User.objects.get(hospital_id=id)
            except User.DoesNotExist:
                return JsonResponse({"error": "No user with this patient ID"}, status=404)
            return JsonResponse({"success": "User with the patient ID was found"})
        else:
            return JsonResponse({"error": "You must provide an ID."}, status=400)
    return JsonResponse({"error": "You must use a GET request to access this link"}, status=403)


def dashboard(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return HttpResponseRedirect("/")
    return render(request, "dashboard.html", {'user': request.user})


def json_parse(x):
    return json.loads(serializers.serialize('json', x))


def receipts_api(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return JsonResponse({"error": "You have to login to access this API"},
                            status=401)
    if request.method == "GET" and request.is_ajax():
        if request.GET.get("full"):
            r = m.Receipt.objects.filter(user=request.user).order_by("date").reverse()
        else:
            r = m.Receipt.objects.filter(user=request.user).order_by("date").reverse()[:5]
        data = serializers.serialize('json', r)
        data = json.loads(data)
        for i in data:
            i["consultations"] = json_parse([m.Consultation.objects.get(pk=a) for a in i["fields"]["consultations"]])
            i["services"] = json_parse([m.ServiceStat.objects.get(pk=a) for a in i["fields"]["services"]])
            i["drugs"] = json_parse([m.DrugStat.objects.get(pk=a) for a in i["fields"]["drugs"]])
            i["tests"] = json_parse([m.LabStat.objects.get(pk=a) for a in i["fields"]["tests"]])

            i["services"] = [{"name": m.Service.objects.get(pk=j["fields"]["service"]).name, **j["fields"]} for j in i["services"]]
            i["drugs"] = [{"name": m.Drug.objects.get(pk=j["fields"]["drug"]).name, **j["fields"]} for j in i["drugs"]]
            i["tests"] = [{"name": m.Drug.objects.get(pk=j["fields"]["test"]).name, **j["fields"]} for j in i["tests"]]

        return JsonResponse({"receipts": json.dumps(data)}, safe=False)
    return JsonResponse({"error": "You can only send GET Requests to this link"}, status=403)


def print_receipt(request, uid):
    if request.user.is_active and request.user.is_authenticated:
        if request.method == "GET":
            context = {}
            context["receipt"] = m.Receipt.objects.get(pk=uid)
            if context["receipt"].user == request.user and context["receipt"].paid:
                return render(request, "print-receipt.html", context)


def stats_api(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == 'GET' and request.is_ajax() and request.user.is_staff:

            data = {}
            now = datetime.date.today()
            t = ""
            types = request.GET.get('types', 'daily')
            n = int(request.GET.get('n', 30))

            if types == "daily":
                then = now - datetime.timedelta(days=n)
                t = "day"
            elif types == "weekly":
                then = now - datetime.timedelta(weeks=n)
                t = "week"
            elif types == "monthly":
                then = now - datetime.timedelta(weeks=n * 4)
                t = "month"
            elif types == "yearly":
                then = now - datetime.timedelta(weeks=n * 52)
                t = "year"
            else:
                return JsonResponse({"error": "An error occurred"}, status=400)

            data["drug_count"] = m.DrugStat.objects.exclude(time_created__lt=then).count()
            data["test_count"] = m.LabStat.objects.exclude(time_created__lt=then).count()
            data["service_count"] = m.ServiceStat.objects.exclude(time_created__lt=then).count()

            data["drugs"] = json_parse(m.DrugStat.objects.exclude(time_created__lt=then))
            data["tests"] = json_parse(m.LabStat.objects.exclude(time_created__lt=then))
            data["services"] = json_parse(m.ServiceStat.objects.exclude(time_created__lt=then))

            for drug in data['drugs']:
                drug['drug'] = json_parse(m.Drug.objects.filter(pk=drug["fields"]["drug"]))[0]
            for service in data['services']:
                service['service'] = json_parse(m.Service.objects.filter(pk=service["fields"]["service"]))[0]
            for test in data['tests']:
                test['test'] = json_parse(m.Test.objects.filter(pk=test["fields"]["test"]))[0]

            data["summary"] = f"~ {n} {t} Summary"
            return JsonResponse({"stats": json.dumps(data)}, safe=False)
        return JsonResponse({"error": "You are not authorized. No POST requests"}, status=401)
    return JsonResponse({"error": "You are not authenticated"}, status=403)


def full_receipts(request):
    return render(request, "receipts.html")


def full_transactions(request):
    return render(request, "transactions.html")


def login_api(request):
    if request.method == "POST" and request.is_ajax():
        username = request.POST.get("username", False)
        password = request.POST.get("password", False)

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return JsonResponse({"success": "You have successfully logged in. You are now being redirected"},
                                status=200)
        return JsonResponse({"error": "Your username or password is incorrect"}, status=400)
    return JsonResponse({"error": "You can only send POST Requests to this link"}, status=403)


def pay_receipts_api(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return JsonResponse({"error": "You have to login to access this API"},
                            status=401)
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get("id")

        if id:
            try:
                receipt = m.Receipt.objects.get(pk=id)
                if receipt.user == request.user:
                    if not receipt.paid:
                        if receipt.total <= request.user.wallet_balance:
                            request.user.wallet_balance -= receipt.total
                            receipt.paid = True
                            request.user.save()
                            receipt.save()
                            return JsonResponse({"message": "You have successfully paid this invoice. Proceed to print!"})
                        return JsonResponse({"message": "You don't have enough credit. Top Up!"}, status=403)
                    return JsonResponse({"message": "You have already paid this invoice"}, status=403)
                return JsonResponse({"message": "You cannot pay an invoice you did not generate"}, status=401)
            except m.Receipt.DoesNotExist:
                return JsonResponse({"message": "Illegal Receipt"}, status=400)
        return JsonResponse({"message": "You must send id as a GET parameter"}, status=400)
    return JsonResponse({"error": "You can only send GET Requests to this link"}, status=403)


def transactions_api(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return JsonResponse({"error": "You have to login to access this API"},
                            status=401)
    if request.method == "GET" and request.is_ajax():
        if request.GET.get("full"):
            t = m.Transaction.objects.filter(user=request.user).order_by("date").reverse()
        else:
            t = m.Transaction.objects.filter(user=request.user).order_by("date").reverse()[:5]
        data = serializers.serialize('json', t)
        return JsonResponse({"transactions": data}, safe=False)
    return JsonResponse({"error": "You can only send GET Requests to this link"}, status=403)


def admin_dashboard(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return HttpResponseRedirect("/")
    if request.user.is_staff and not request.user.is_superuser:
        return HttpResponseRedirect("/staff/dashboard/")
    return render(request, "admin-dashboard.html")


def staff_dashboard(request):
    if not request.user.is_authenticated and not request.user.is_active and not request.user.is_staff:
        return HttpResponseRedirect("/")
    return render(request, "staff-dashboard.html")


def issue_invoice(request):
    if not request.user.is_authenticated and not request.user.is_active and not request.user.is_staff:
        return HttpResponseRedirect("/")
    return render(request, "issue-invoice.html")


def invoice_data_api(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return JsonResponse({"error": "You have to login to access this API"},
                            status=401)
    if request.method == "GET" and request.is_ajax() and request.user.is_staff:
        data = {
            "consultations": serializers.serialize("json", m.Consultation.objects.all()),
            "services": serializers.serialize("json", m.Service.objects.all()),
            "drugs": serializers.serialize("json", m.Drug.objects.all()),
            "tests": serializers.serialize("json", m.Test.objects.all()),
        }
        return JsonResponse({"data": data}, safe=False)
    return JsonResponse({"error": "Only staff can send GET Requests to this link"}, status=403)


def process_invoice_api(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return JsonResponse({"error": "You have to login to access this API"},
                            status=401)
    if request.method == "POST" and request.is_ajax() and request.user.is_staff:
        patient_id = request.POST.get("patient_id")
        ward_cost = int(request.POST.get("ward_cost"))
        days_in_ward = int(request.POST.get("days_in_ward"))
        consultations = json.loads(request.POST.get("consultations"))
        services = json.loads(request.POST.get("services"))
        drugs = json.loads(request.POST.get("drugs"))
        tests = json.loads(request.POST.get("tests"))
        consumables = int(request.POST.get("consumables"))
        pharmacy_bag = True if request.POST.get("pharmacy_bag") == "true" else False
        r = m.Receipt(
            user=User.objects.get(hospital_id=patient_id),
            ward_cost=ward_cost,
            days_in_ward=days_in_ward,
            consumables=consumables,
            pharmacy_bag=pharmacy_bag,
            total=0
        )
        r.save()
        for c in consultations:
            r.consultations.add(m.Consultation.objects.get(pk=c))
        for t in tests:
            test = m.Test.objects.get(pk=t)
            r.tests.add(
                m.LabStat.objects.create(test=test, total=test.price)
            )
        for s in services:
            service = m.Service.objects.get(pk=s)
            r.services.add(
                m.ServiceStat.objects.create(service=service, total=service.fee)
            )
        for d in drugs:
            drug = m.Drug.objects.get(pk=d["id"])
            r.drugs.add(
                m.DrugStat.objects.create(drug=drug, total=drug.price * int(d["qty"]))
            )

        r.total += (r.ward_cost * r.days_in_ward)
        r.total += r.consumables
        r.total += sum([c.price for c in r.consultations.all()])
        r.total += sum([s.total for s in r.services.all()])
        r.total += sum([d.total for d in r.drugs.all()])
        r.total += sum([t.total for t in r.tests.all()])
        r.save()
        return JsonResponse({"success": f"Your invoice has been Issued! Id is #{r.pk}"})

    return JsonResponse({"error": "Only staff can send POST Requests to this link"}, status=403)


def payment_made(request):
    if request.method == "GET" and "reference" in request.GET:
        ref = request.GET["reference"]
        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}",
                                headers={"Authorization": "Bearer sk_test_8e31ea60a3a6b4c890cd6dc090f4a9a96dc1031b"})
        resp = response.json()

        if resp.get("status"):
            u = User.objects.get(hospital_id=(resp["data"]["customer"]["email"].split("@")[0]).upper())
            u.wallet_balance += resp["data"]["amount"] / 100
            u.save()
            m.Transaction.objects.create(user=u, amount=resp["data"]["amount"] / 100)
        return HttpResponseRedirect("/dashboard/")


def make_payment(request):
    if not request.user.is_authenticated and not request.user.is_active:
        return HttpResponseRedirect("/")
    if request.method == "GET":
        hospital_id = request.user.hospital_id
        amount = int(request.GET.get("amount")) * 100
        response = requests.post("https://api.paystack.co/transaction/initialize",
                                 data={"email": f"{hospital_id}@hospital.io", "amount": amount,
                                       "callback_url": "https://da51dec7.ngrok.io/payment-made"},
                                 headers={"Authorization": "Bearer sk_test_8e31ea60a3a6b4c890cd6dc090f4a9a96dc1031b"})
        url = response.json()["data"]["authorization_url"]
        return HttpResponseRedirect(url)
