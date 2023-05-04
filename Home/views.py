import csv
import requests
import pandas as pd
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from datetime import date
from Home.decorators import allowed_users
from authentication.models import Profile
from payment_methods.models import Subscriber
from .models import *
from payment_methods.models import *

# Create your views here.
import stripe
from django.conf import settings

from dateutil.relativedelta import relativedelta
import datetime
from .serializers import *
from rest_framework import generics
import statistics
import numpy as np
from .models import *
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="Login")
def Setting(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    context = {"user_profile": user_profile, "users": users}
    if request.method == "POST":
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        email = request.POST.get("Email")
        phone = request.POST.get("phone")
        print(fname, lname, email)

        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname
        if len(email) != 0:
            users.email = email
        # if len(phone) != 0:
        #     user_profile.phone = phone

        if len(request.FILES) != 0:
            my_file = request.FILES["upload"]

            if (
                my_file.content_type == "image/jpg"
                or my_file.content_type == "image/jpeg"
                or my_file.content_type == "image/png"
            ):
                user_profile.picture = request.FILES["upload"]

                users.save()
                user_profile.save()

                messages.success(request, "Data updated successfully")
                return redirect("Settings")

            messages.success(request, "Only JPG, PNG & JPEG image type is allowed")
            return redirect("Settings")
        users.save()
        messages.success(request, "Data updated successfully")
        return redirect("Settings")

    return render(request, "settings.html", context)


@login_required(login_url="Login")
def setting_security(request):
    user_profile = Profile.objects.get(owner=request.user)

    context = {"user_profile": user_profile}
    if request.method == "POST":
        users = User.objects.get(username=request.user)
        current_password = request.POST.get("current_password")
        phone = request.POST.get("phone")

        new_password = request.POST.get("new_password")
        user = auth.authenticate(
            username=request.user.username, password=current_password
        )

        if user is not None:
            if len(new_password) != 0:
                users.set_password(new_password)
                users.save()
            # if len(phone) != 0:
            user_profile.changed_default_password = "Yes"
            user_profile.save()

            messages.info(
                request,
                "Password updated successfully,Please Login with New Set Password",
            )
            return redirect("Login")
        else:
            messages.info(request, "Current Password does not matched.")
            return render(request, "settings-security.html", context)

    else:
        return render(request, "settings-security.html", context)


@login_required(login_url="Login")
def my_devices(request):
    users = Profile.objects.get(owner=request.user)
    all_devices = Devices.objects.filter(owner=request.user, status="Un Activated")
    context = {"user_profile": users, "all_devices": all_devices}
    return render(request, "devices_index.html", context)


@login_required(login_url="Login")
def add_device(request):
    users = Profile.objects.get(owner=request.user)
    context = {"user_profile": users}
    if request.method == "POST":
        designation = request.POST.get("designation")
        sr_no = request.POST.get("serial_number")
        password = request.POST.get("password")

        if not designation:
            messages.error(request, "Designation is required")
            return redirect("add_device", context)
        if not sr_no:
            messages.error(request, "Serial No. is required")
            return redirect("add_device", context)
        if not password:
            messages.error(request, "Password is required")
            return redirect("add_device", context)
        try:
            if Devices.objects.filter(
                serial_no=sr_no, device_password=password, status="Active"
            ).exists():
                if Subscriber.objects.filter(
                    serial_no=Devices.objects.filter(
                        serial_no=sr_no, device_password=password, status="Active"
                    ).first(),
                    status="Active",
                ).exists():
                    subscriber = Subscriber.objects.filter(
                        serial_no=Devices.objects.filter(
                            serial_no=sr_no, device_password=password, status="Active"
                        ).first(),
                        status="Active",
                    ).first()
                    Devices.objects.create(
                        serial_no=sr_no,
                        designation=designation,
                        device_password=password,
                        owner=request.user,
                        status="Active",
                    ).save()
                    Subscriber.objects.create(
                        plan=subscriber.plan,
                        user=request.user,
                        price=subscriber.price,
                        serial_no=subscriber.serial_no,
                        status="Active",
                        subsciption_from=subscriber.subsciption_from,
                        subsciption_to=subscriber.subsciption_to,
                    )
                messages.success(request, "Device added Successfully.")
                return redirect("active_devices")

            Devices.objects.create(
                serial_no=sr_no,
                designation=designation,
                device_password=password,
                owner=request.user,
            ).save()
            messages.success(request, "Device added Successfully.")
            return redirect("active_devices")

        except Exception as e:
            print(e)
            messages.error(
                request, "Device did not added successfully, please try again "
            )
            return redirect("active_devices")
    return render(request, "add_device.html", context)


@login_required(login_url="Login")
def edit_device(request, id):
    users = Profile.objects.get(owner=request.user)
    device_details = Devices.objects.get(device_id=id)
    context = {"user_profile": users, "device_details": device_details}
    if request.method == "POST":
        designation = request.POST.get("designation")
        sr_no = request.POST.get("serial_number")
        password = request.POST.get("password")

        try:
            device_details.serial_no = sr_no
            device_details.designation = designation
            device_details.device_password = password
            device_details.owner = request.user
            device_details.save()
            messages.success(request, "Device Updated Successfully.")
            return redirect("active_devices")

        except Exception as e:
            print(e)
            messages.error(
                request, "Device did not updated successfully, please try again "
            )
            return redirect("active_devices")

    return render(request, "edit_device.html", context)


@login_required(login_url="Login")
def edit_device_after_activate(request, id):
    users = Profile.objects.get(owner=request.user)
    device_details = Devices.objects.get(device_id=id)
    context = {"user_profile": users, "device_details": device_details}
    if request.method == "POST":
        designation = request.POST.get("designation")

        password = request.POST.get("password")

        try:
            device_details.designation = designation
            device_details.device_password = password

            device_details.save()
            messages.success(request, "Device Updated Successfully.")
            return redirect("active_devices")

        except Exception as e:
            print(e)
            messages.error(
                request, "Device did not updated successfully, please try again "
            )
            return redirect("active_devices")

    return render(request, "edit_device_after_activate.html", context)


@login_required(login_url="Login")
def delete_device(request, id):
    device_details = Devices.objects.get(device_id=id)
    device_details.delete()
    messages.error(request, "Device Delete successfully ")
    return redirect("active_devices")


@login_required(login_url="Login")
def device_export_csv(request):
    response = HttpResponse("text/csv")
    response["Content-Disposition"] = (
        "attachment; filename=Devices Details" + str(datetime.datetime.now()) + ".csv"
    )

    writer = csv.writer(response)
    writer.writerow(["", "Device Serial No.", "Designation", "Password"])
    device_info = Devices.objects.filter(owner=request.user)

    for item in device_info:
        writer.writerow(
            [
                "",
                item.serial_no,
                item.designation,
                item.device_password,
            ]
        )
    return response


def certificate_payment_success(request):
    try:
        session = stripe.checkout.Session.retrieve(request.GET["session_id"])
        plan_id = session.client_reference_id
        user = request.user
        for i in plan_id:
            subsciber_details = Subscriber.objects.get(
                user=user, serial_no=i.id, status="Active"
            )
            subsciber_details.status = "Expire"
            subsciber_details.save()
            Subscriber.objects.create(
                plan=1,
                user=user,
                price=200,
                serial_no=i.id,
                status="Active",
                subsciption_from=datetime.date.today(),
                subsciption_to=datetime.date.today() + relativedelta(years=1),
            )
            return render(request, "payment_success.html")

    except:
        return render(request, "payment_cancel.html")


def find_distance(full_address):
    GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": full_address,
        "sensor": "false",
        "region": "USA",
        "key": "AIzaSyAfIFQFEGJ3snlXb8VnRK06CJMYrUiFppI",
    }

    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    print("res for origin address", res)

    result = res["results"][0]

    origin_latitude = result["geometry"]["location"]["lat"]
    origin_longitude = result["geometry"]["location"]["lng"]
    return origin_latitude, origin_longitude


@login_required(login_url="Login")
def order_device(request):
    if request.method == "POST":
        request.session["no_of_devices"] = request.POST.get("no_of_devices")
        delivery_destination = request.POST.get("delivery_address")

        street = request.POST.get("street_number")
        road = request.POST.get("route")
        city = request.POST.get("City")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        country = request.POST.get("country")
        full_address = delivery_destination + " " + zip_code
        lat, long = find_distance(full_address)
        if not lat and long:
            request.session["address_verified"] = "No"
        else:
            if not lat or long:
                request.session["address_verified"] = "No"
            else:
                request.session["address_verified"] = "Yes"

        request.session["delivery_destination"] = delivery_destination
        request.session["street"] = street
        request.session["road"] = road
        request.session["city"] = city
        request.session["state"] = state
        request.session["zip_code"] = zip_code
        request.session["country"] = country
        request.session["ph_no"] = request.POST.get("ph_no")
        request.session["name"] = request.POST.get("name")
        return redirect("/payments/buy_devices")

    return render(request, "order_device.html")


@login_required(login_url="Login")
def active_devices(request):
    try:
        users = Profile.objects.get(owner=request.user)
        subsciber_details = Subscriber.objects.filter(user=request.user)
        for i in subsciber_details:
            remaining = (i.subsciption_to - datetime.date.today()).days
            if remaining == 0:
                i.status = "Expire"
                i.save()
            else:
                if remaining <= 90:
                    i.status = "Almost Expire"

                    i.save()
    except Exception as e:
        print("line no 357 exception", e)
        users = None
    all_devices = Devices.objects.filter(owner=request.user, status="Un Activated")
    subscriber = Subscriber.objects.filter(user=request.user)
    context = {
        "all_devices_sub": subscriber,
        "user_profile": users,
        "all_devices": all_devices,
    }
    return render(request, "active_devices.html", context)


# this is a hourly dashboard
def dashboard_date(request):
    try:
        sum_of_count_o = 0.0
        total_count_o = 0.0
        max_count_o = 0.0
        sum_of_count_i = 0.0
        sum_of_state_production = 0.0
        sum_of_state_other = 0.0
        median_of_count_o_Array = []
        flag = 0
        pre_date = ""
        def_su = 0
        su_date_label = []
        su_date_value = []
        sc = 0
        scp = 0
        if request.method == "POST":
            device_id = request.POST.get("device_id")
            datestrt = request.POST.get("datestrt")
            dateend = request.POST.get("dateend")
            my_device = Devices.objects.get(device_id=device_id)
        else:
            my_device = Devices.objects.filter(owner=request.user).first()
            datestrt = datetime.date.today()
            dateend = datetime.date.today()
        print(datestrt, dateend)
        devices_details = API_Device_data.objects.filter(
            serial_no=my_device.serial_no,
            device_password=my_device.device_password,
            date__gte=datestrt,
            date__lte=dateend,
        )
        print("devices", devices_details)
        sum_of_count_o_in_production = 0
        sum_of_cadence = 0
        su_up = []
        sp = 0
        pr_value = []
        sp = 0
        so = 0
        ar_value = []
        sco = 0
        sci = 0
        qr_value = []
        oee_value = []
        for data in devices_details:
            if flag == 0:
                pre_date = data.date
                def_su = def_su + (int(data.count_input) - int(data.count_output))
                sp = sp + int(data.count_output)
                sc = sc + float((data.cadence).replace(",", "."))
                sco = sco + int(data.count_output)
                sci = sci + int(data.count_input)
                if data.state == "Production":
                    scp = scp + 1
                    sp = sp + 1
                else:
                    so = so + 1

                flag = -1
            else:
                if pre_date == data.date:
                    def_su = def_su + (int(data.count_input) - int(data.count_output))
                    sp = sp + int(data.count_output)
                    sc = sc + float((data.cadence).replace(",", "."))
                    so = so + 1
                    sco = sco + int(data.count_output)
                    sci = sci + int(data.count_input)
                    if data.state == "Production":
                        scp = scp + 1
                        sp = sp + 1
                    else:
                        so = so + 1
                else:
                    if scp != 0:
                        pr_value.append(format((float(sc) / float(scp)), ".1f"))
                    else:
                        pr_value.append(0)
                    if so != 0:
                        ar_value.append(format((float(sp) / float(so)), ".1f"))
                    else:
                        ar_value.append(0)
                    if sci != 0:
                        qr_value.append(format((float(sco) / float(sci)), ".1f"))
                    else:
                        qr_value.append(0)
                    su_date_label.append(pre_date)
                    pre_date = data.date
                    su_up.append(sp)
                    su_date_value.append(abs(def_su))
                    def_su = 0
                    sc = 0
                    scp = 0
                    so = 0
                    sp = 0
                    sco = 0
                    sci = 0
                    sp = 0
                    def_su = def_su + (int(data.count_input) - int(data.count_output))
                    sp = sp + int(data.count_output)
                    sc = sc + float((data.cadence).replace(",", "."))
                    so = so + 1
                    sco = sco + int(data.count_output)
                    sci = sci + int(data.count_input)
                    if data.state == "Production":
                        scp = scp + 1
                        sp = sp + 1
                    else:
                        so = so + 1
        su_date_label.append(pre_date)
        su_date_value.append(abs(def_su))
        su_up.append(sp)

        if scp != 0:
            pr_value.append(format((float(sc) / float(scp)), ".1f"))
        else:
            pr_value.append(0)
        if so != 0:
            ar_value.append(format((float(sp) / float(so)), ".1f"))
        else:
            ar_value.append(0)

        if sci != 0:
            qr_value.append(format((float(sco) / float(sci)), ".1f"))
        else:
            qr_value.append(0)

        for i in range(0, len(pr_value)):
            oee_value.append(
                float(pr_value[i]) * float(ar_value[i]) * float(qr_value[i])
            )
        for data in devices_details:
            sum_of_cadence = sum_of_cadence + float((data.cadence).replace(",", "."))
            if data.count_output:
                median_of_count_o_Array.append(int(data.count_output))
                if int(max_count_o) < int(data.count_output):
                    max_count_o = int(data.count_output)
                total_count_o = total_count_o + 1
                sum_of_count_o = sum_of_count_o + int(data.count_output)
            if data.count_input:
                sum_of_count_i = sum_of_count_i + int(data.count_input)
            if data.state == "Production":
                sum_of_count_o_in_production = sum_of_count_o_in_production + int(
                    data.count_output
                )
                sum_of_state_production = sum_of_state_production + 1
            else:
                sum_of_state_other = sum_of_state_other + 1
        std_arr = np.array(median_of_count_o_Array)
        try:
            ar = format(
                float(sum_of_state_production) / float(sum_of_state_other), ".2f"
            )
        except:
            ar = 0
        try:
            pr = format(
                ((int(sum_of_cadence) / int(sum_of_count_o_in_production))) * 100, ".2f"
            )
        except:
            pr = 0
        try:
            qr = format(float(sum_of_count_o) / float(sum_of_count_i), ".2f")
        except:
            qr = 0
        try:
            mean = format(float(sum_of_count_o) / float(total_count_o), ".2f")
        except:
            mean = 0
        try:
            mean = format(float(sum_of_count_o) / float(total_count_o), ".2f")
        except:
            mean = 0
        try:
            medium = format(statistics.median(median_of_count_o_Array), ".2f")
        except:
            medium = 0
        try:
            std = format(std_arr.std(), ".2f")
        except:
            std = "Not Available"
        oc = []
        oc_label = []
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="general stop",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="Break",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="Available",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="Waiting for material",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="OFF",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="Convoyeur",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date__gte=datestrt,
                date__lte=dateend,
                state="Meeting",
            ).count()
        )
        oc_label.append("general stop")
        oc_label.append("Break")
        oc_label.append("Available")
        oc_label.append("Waiting for material")
        oc_label.append("OFF")
        oc_label.append("Convoyeur")
        oc_label.append("Meeting")

        context = {
            "su_date_label": su_date_label,
            "su_date_value": su_date_value,
            "oc_label": oc_label,
            "oc": oc,
            "units_produced": sum_of_count_o,
            "Availability_rate": ar,
            "Performance_rate": pr,
            "Quality_rate": qr,
            "oee": format(float(ar) * float(pr) * float(qr), ".2f"),
            "mean": mean,
            "maximun": max_count_o,
            "medium": medium,
            "std": std,
            "all_devices": Devices.objects.filter(owner=request.user, status="Active"),
            "selected": my_device,
            "pr_value": pr_value,
            "ar_value": ar_value,
            "qr_value": qr_value,
            "oee_value": oee_value,
            "st": datestrt,
            "ed": dateend,
            "su_up": su_up,
        }
        print(su_up)
        return render(request, "index2.html", context)
    except Exception as e:
        return render(request, "index2.html")


# this is a daily dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    # users = Profile.objects.get(owner=request.user)
    sum_of_count_o = 0.0
    total_count_o = 0.0
    max_count_o = 0.0
    sum_of_count_i = 0.0
    sum_of_state_production = 0.0
    sum_of_state_other = 0.0
    median_of_count_o_Array = []
    flag = 0
    pre_date = ""
    def_su = 0
    su_date_label = []
    su_date_value = []
    sc = 0
    scp = 0

    if request.method == "POST":
        device_id = request.POST.get("device_id")
        date = request.POST.get("date")
        my_device = Devices.objects.get(device_id=device_id)
    else:
        my_device = Devices.objects.filter(owner=request.user).first()
        date = datetime.date.today()
    devices_details = None
    if my_device:
        devices_details = API_Device_data.objects.filter(
            serial_no=my_device.serial_no,
            device_password=my_device.device_password,
            date=date,
        )
        sum_of_count_o_in_production = 0
        sum_of_cadence = 0
        su_up = []
        sp = 0
        pr_value = []
        sp = 0
        so = 0
        ar_value = []
        sco = 0
        sci = 0
        qr_value = []
        oee_value = []
        for data in devices_details:
            if flag == 0:
                pre_date = data.hours
                def_su = def_su + (int(data.count_input) - int(data.count_output))
                sp = sp + int(data.count_output)
                sc = sc + float((data.cadence).replace(",", "."))
                sco = sco + int(data.count_output)
                sci = sci + int(data.count_input)
                if data.state == "Production":
                    scp = scp + 1
                    sp = sp + 1
                else:
                    so = so + 1

                flag = -1
            else:
                if pre_date == data.hours:
                    def_su = def_su + (int(data.count_input) - int(data.count_output))
                    sp = sp + int(data.count_output)
                    sc = sc + float((data.cadence).replace(",", "."))
                    so = so + 1
                    sco = sco + int(data.count_output)
                    sci = sci + int(data.count_input)
                    if data.state == "Production":
                        scp = scp + 1
                        sp = sp + 1
                    else:
                        so = so + 1
                else:
                    if scp != 0:
                        pr_value.append(format((float(sc) / float(scp)), ".1f"))
                    else:
                        pr_value.append(0)
                    if so != 0:
                        ar_value.append(format((float(sp) / float(so)), ".1f"))
                    else:
                        ar_value.append(0)
                    if sci != 0:
                        qr_value.append(format((float(sco) / float(sci)), ".1f"))
                    else:
                        qr_value.append(0)
                    su_date_label.append(pre_date)
                    pre_date = data.hours
                    su_up.append(sp)
                    su_date_value.append(abs(def_su))
                    def_su = 0
                    sc = 0
                    scp = 0
                    so = 0
                    sp = 0
                    sco = 0
                    sci = 0
                    sp = 0
                    def_su = def_su + (int(data.count_input) - int(data.count_output))
                    sp = sp + int(data.count_output)
                    sc = sc + float((data.cadence).replace(",", "."))
                    so = so + 1
                    sco = sco + int(data.count_output)
                    sci = sci + int(data.count_input)
                    if data.state == "Production":
                        scp = scp + 1
                        sp = sp + 1
                    else:
                        so = so + 1
        su_date_label.append(pre_date)
        su_date_value.append(abs(def_su))
        su_up.append(sp)

        if scp != 0:
            pr_value.append(format((float(sc) / float(scp)), ".1f"))
        else:
            pr_value.append(0)
        if so != 0:
            ar_value.append(format((float(sp) / float(so)), ".1f"))
        else:
            ar_value.append(0)

        if sci != 0:
            qr_value.append(format((float(sco) / float(sci)), ".1f"))
        else:
            qr_value.append(0)

        for i in range(0, len(pr_value)):
            oee_value.append(float(pr_value[i]) * float(ar_value[i]) * float(qr_value[i]))
        for data in devices_details:
            sum_of_cadence = sum_of_cadence + float((data.cadence).replace(",", "."))
            if data.count_output:
                median_of_count_o_Array.append(int(data.count_output))
                if int(max_count_o) < int(data.count_output):
                    max_count_o = int(data.count_output)
                total_count_o = total_count_o + 1
                sum_of_count_o = sum_of_count_o + int(data.count_output)
            if data.count_input:
                sum_of_count_i = sum_of_count_i + int(data.count_input)
            if data.state == "Production":
                sum_of_count_o_in_production = sum_of_count_o_in_production + int(
                    data.count_output
                )
                sum_of_state_production = sum_of_state_production + 1
            else:
                sum_of_state_other = sum_of_state_other + 1
        std_arr = np.array(median_of_count_o_Array)
        try:
            ar = format(float(sum_of_state_production) / float(sum_of_state_other), ".2f")
        except:
            ar = 0
        try:
            pr = format(
                ((int(sum_of_cadence) / int(sum_of_count_o_in_production))) * 100, ".2f"
            )
        except:
            pr = 0
        try:
            qr = format(float(sum_of_count_o) / float(sum_of_count_i), ".2f")
        except:
            qr = 0
        try:
            mean = format(float(sum_of_count_o) / float(total_count_o), ".2f")
        except:
            mean = 0
        try:
            mean = format(float(sum_of_count_o) / float(total_count_o), ".2f")
        except:
            mean = 0
        try:
            medium = format(statistics.median(median_of_count_o_Array), ".2f")
        except:
            medium = 0
        try:
            std = format(std_arr.std(), ".2f")
        except:
            std = "Not Available"
        oc = []
        oc_label = []
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="general stop",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="Break",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="Available",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="Waiting for material",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="OFF",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="Convoyeur",
            ).count()
        )
        oc.append(
            API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date,
                state="Meeting",
            ).count()
        )
        oc_label.append("general stop")
        oc_label.append("Break")
        oc_label.append("Available")
        oc_label.append("Waiting for material")
        oc_label.append("OFF")
        oc_label.append("Convoyeur")
        oc_label.append("Meeting")





        iot_device = API_Device_data.objects.all().order_by("pk")
        # Chart Data
        speed_data = []
        distance_covered_data = []
        num = 0
        for obj in iot_device:
            if obj.count_input:
                speed_data.append({ "x": num, "y": int(obj.count_input) })
                num += 1
        _num = 0
        for obj in iot_device:
            if obj.count_input and obj.count_output:
                data =  int(obj.count_input) - int(obj.count_output)
                if data < 0:
                     data = 0
                distance_covered_data.append(
                    { "x": _num, "y": data }
                )
                _num += 1




        availability_list = []
        quality_list = []
        performance_rate = []
        total_state = 0
        total_state_off = 0
        total_state_production = 0
        total_output = 0
        total_cadence = 0
        for obj in iot_device:
            total_state += 1
            if obj.state == "PRODUCTION":
                total_state_production += 1
            if obj.state == "OFF":
                total_state_off += 1
            
            if obj.count_output:
                total_output += float(obj.count_output)
            if obj.cadence:
                try:
                    total_cadence += float(obj.cadence)
                except Exception as e:
                    total_cadence += float(1)
            
            # Availability rate
            try:
                calculation = (
                    (total_state - total_state_off - total_state_production) / (total_state - total_state_off)
                ) * 100
            except Exception as e:
                print(e)
                calculation = 0
            availability_list.append({ "x": total_state, "y": calculation })
            
            # Quality rate
            _input = obj.count_input
            _output = obj.count_output
            try:
                i_o = (float(_output) / float(_input)) * 100
            except Exception as e:
                i_o = float(100)
            quality_list.append({ "x": total_state, "y": i_o })
            
            # Performance rate
            try:
                performance = (total_output / total_cadence) * 100
            except Exception as e:
                performance = float(1)
            performance_rate.append({ "x": total_state, "y": performance })


        paginator = Paginator(iot_device, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # user data
        state_1 = [
            { "label": "1", "y": 3 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 7 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 9 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 3 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 5 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]
        
        state_2 = [
            { "label": "1", "y": 3 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 3 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 5 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 2 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 8 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]
        
        state_3 = [
            { "label": "1", "y": 31 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 7 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 9 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 3 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 5 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]
        
        production = [
            { "label": "1", "y": 31 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 7 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 9 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 3 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 5 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]
        
        off = [
            { "label": "1", "y": 31 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 7 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 9 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 3 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 5 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]
        
        unknown = [
            { "label": "1", "y": 31 },
            { "label": "2", "y": 6 },
            { "label": "3", "y": 2 },
            { "label": "4", "y": 7 },
            { "label": "5", "y": 3 },
            { "label": "6", "y": 9 },
            { "label": "7", "y": 4 },
            { "label": "8", "y": 6 },
            { "label": "9", "y": 7 },
            { "label": "10", "y": 3 },
            { "label": "11", "y": 2 },
            { "label": "12", "y": 3 },
            { "label": "13", "y": 5 },
            { "label": "14", "y": 6 },
            { "label": "15", "y": 7 },
            { "label": "16", "y": 8 },
            { "label": "17", "y": 5 },
            { "label": "18", "y": 4 },
            { "label": "19", "y": 7 },
            { "label": "20", "y": 8 },
            { "label": "21", "y": 8 },
            { "label": "22", "y": 8 },
            { "label": "23", "y": 8 },
        ]

        context = {
            "su_date_label": su_date_label, 'speed_data': speed_data,
            "su_date_value": su_date_value, "oc_label": oc_label,
            "oc": oc, 'distance_covered_data': distance_covered_data,
            "units_produced": sum_of_count_o, "Availability_rate": ar,
            "Performance_rate": pr, "Quality_rate": qr, "mean": mean,
            "oee": format(float(ar) * float(pr) * float(qr), ".2f"),
            "maximun": max_count_o, "medium": medium, "std": std,
            "all_devices": Devices.objects.filter(owner=request.user, status="Active"),
            "selected": my_device, "pr_value": pr_value, "ar_value": ar_value,
            "qr_value": qr_value, "oee_value": oee_value, "st": date, "ed": "",
            "su_up": su_up, "state_1": state_1, "state_2": state_2, "off": off,
            "state_3": state_3, "production": production, "unknown": unknown,
            "iot_device": page_obj, "availability_list": availability_list,
            'quality_list': quality_list, "performance_rate": performance_rate
        }
        return render(request, "index.html", context)
    return render(request, "index.html")


class DeviceListCreateViewSet(generics.ListCreateAPIView):
    queryset = API_Device_data.objects.all()
    serializer_class = DeviceSerializer


class Device_Details(generics.RetrieveUpdateDestroyAPIView):
    queryset = API_Device_data
    serializer_class = DeviceSerializer


@csrf_exempt
def add_device_api(request):
    if request.method == "GET":
        serial_no = request.GET.get("serial_no")
        device_password = request.GET.get("device_password")
        date = request.GET.get("date")
        time = request.GET.get("time")
        hours = request.GET.get("hours")
        count_input = request.GET.get("count_input")
        count_output = request.GET.get("count_output")
        state = request.GET.get("state")
        cadence = request.GET.get("cadence")
        try:
            API_Device_data.objects.create(
                serial_no=serial_no,
                device_password=device_password,
                date=date,
                time=time,
                hours=hours,
                count_input=count_input,
                count_output=count_output,
                state=state,
                cadence=cadence,
            )
            return HttpResponse(status=200)
        except Exception as e:
            print("Exception while adding is", e)
            return HttpResponse(e)

    return render(request, "plain_text_api_test.html")
