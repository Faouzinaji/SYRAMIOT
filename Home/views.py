import csv
import requests
import datetime
from django.contrib import messages, auth
from django.db.models import FloatField, Count, Q
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Sum
from authentication.models import Profile
from payment_methods.models import Subscriber
from .models import *
from payment_methods.models import *

# Create your views here.
import stripe
from dateutil.relativedelta import relativedelta
import datetime
from .serializers import *
from rest_framework import generics
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
        email = request.POST.get("email")
        sr_no = request.POST.get("serial_number")
        password = request.POST.get("password")

        if not designation:
            messages.error(request, "Designation is required")
            return redirect("add_device", context)
        if not email:
            messages.error(request, "Email is required")
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
                email=email
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
        email = request.POST.get("email")
        sr_no = request.POST.get("serial_number")
        password = request.POST.get("password")

        try:
            device_details.serial_no = sr_no
            device_details.designation = designation
            device_details.email = email
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


class Overview(View):
    template_name = 'overview.html'
    def get(self, request):
        all_devices = Devices.objects.filter(owner=request.user, status="Active")
        last_state_list = []
        production_list = []
        scraped_list = []
        oee_rate = []
        for data in all_devices:
            state = API_Device_data.objects.filter(
                serial_no=data.serial_no,
                device_password=data.device_password,
            )
            if state:
                last_state_list.append(state.last().state)
                production_list.append(state.last().count_input)
                if not state.last().count_input:
                    _input = 0
                else:
                    _input = int(state.last().count_input)
                if not state.last().count_output:
                    _output = 0
                else:
                    _output = int(state.last().count_output)
                scraped_list.append(_input - _output)
                total_state = 0
                total_state_off = 0
                total_state_production = 0
                total_output = 0
                total_cadence = 0
                for obj in state:
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
                        calculation_data = (
                            (total_state - total_state_off - total_state_production) / (total_state - total_state_off)
                        )
                    except Exception as e:
                        print(e)
                        calculation_data = 0
                    
                    # Quality rate
                    _input = obj.count_input
                    _output = obj.count_output
                    try:
                        i_o_data = (float(_output) / float(_input))
                    except Exception as e:
                        i_o_data = float(1)
                    
                    # Performance rate
                    try:
                        performance_data = (total_output / total_cadence)
                    except Exception as e:
                        performance_data = float(1)

                    # OEE
                    data = (calculation_data * i_o_data * performance_data) * 100
                    oee_rate.append(round(data))

        all_devices = zip(
            all_devices, last_state_list, production_list,
            scraped_list, oee_rate
        )
        context = {
            "all_devices": all_devices,
        }
        return render(request, self.template_name, context)


# this is a daily dashboard
def dashboard_date(request):
    try:
        device_id = request.GET.get("device_id")
        datestrt = request.GET.get("datestrt")
        dateend = request.GET.get("dateend")
        if device_id:
            my_device = Devices.objects.get(device_id=device_id)
        else:
            my_device = Devices.objects.filter(owner=request.user).first()
        if not datestrt:
            datestrt = datetime.date.today() - datetime.timedelta(days=7)
        if not dateend:
            dateend = datetime.date.today()
        devices_details = API_Device_data.objects.filter(
            serial_no=my_device.serial_no,
            device_password=my_device.device_password,
            date__gte=datestrt,
            date__lte=dateend,
        )
        _devices_details = devices_details

        all_date_list = []
        for obj in devices_details:
            if obj.date:
                all_date_list.append(obj.date)
        all_date_set = set(all_date_list)
        # MTBF Charts
        mtbf_list = []
        mttr_list = []
        total_state = 0

        mtbf = 0
        mttr = 0



        for date in all_date_set:
            all_state = devices_details.filter(date__lte=date).order_by('date')
            all_state = all_state.exclude(state__icontains="Off").count()
            all_mtbf = devices_details.filter(mtbf__icontains="1", date=date).count()
            try:
                summary = (all_state / all_mtbf) / 60
            except Exception as e:
                print(e)
                summary = 0
            mtbf += summary
            mtbf_list.append({ "label": date, "y": summary })

            # MTTR
            all_mtbf = devices_details.filter(
                mtbf__icontains="1", date__lte=date
            ).count()
            all_mttr = devices_details.filter(
                mttr__icontains="1", date__lte=date
            ).count()

            try:
                summary_mttr = (all_mttr / all_mtbf) / 60
            except Exception as e:
                print(e)
                summary_mttr = 0
            total_state += 1
            mttr += summary_mttr
            mttr_list.append({ "label": date, "y": summary_mttr })


        # Chart Data
        speed_data = []
        units_produced_list = []

        scraped_unit = 0
        units_produced = 0
        for obj in devices_details.distinct('date'):
            count_input = _devices_details.filter(date=obj.date).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
            count_output = _devices_details.filter(date=obj.date).annotate(as_float=Cast('count_output', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
            
            if count_input:
                units_produced_list.append({ "label": obj.date, "y": int(count_input) })
                units_produced += int(count_input)
            else:
                units_produced_list.append({ "label": obj.date, "y": 0 })
                units_produced += 0

            if count_input and count_output:
                _adata =  int(count_input) - int(count_output)
                if _adata < 0:
                    _adata = 0
                speed_data.append({ "label": obj.date, "y": _adata })
                scraped_unit += _adata
            else:
                speed_data.append({ "label": obj.date, "y": 0 })
                scraped_unit += 0
            _adata = 0
        stop_label_list = []
        breakdown_label_list = []

        availability_list = []
        quality_list = []
        performance_rate = []
        oee_rate = []
        
        total_state = 0
        total_state_off = 0
        total_state_production = 0
        total_output = 0
        total_cadence = 0

        _availability_rate = 0
        _quality_rate = 0
        _performance_rate = 0
        _oee = 0
        for obj in devices_details.distinct('date'):

            total_state = _devices_details.count()
            total_state_production = _devices_details.filter(state__icontains="PRODUCTION").count()
            total_state_off = _devices_details.filter(state__icontains="OFF").count()
            _total_cadence = _devices_details.filter(state__icontains="PRODUCTION")
            total_cadence = _total_cadence.annotate(as_float=Cast('cadence', FloatField())).aggregate(Sum('as_float'))['as_float__sum']

            # Availability rate
            try:
                calculation_data = (
                    (total_state - total_state_off - total_state_production) / (total_state - total_state_off)
                )
                calculation = calculation_data
            except Exception as e:
                print(e)
                calculation = 0
                calculation_data = 0
            _availability_rate += calculation
            availability_list.append({ "label": obj.date, "y": calculation })
            
            # Quality rate
            _input = obj.count_input
            _output = obj.count_output
            try:
                i_o_data = (int(_output) / int(_input))
                i_o = i_o_data
            except Exception as e:
                i_o = 100
                i_o_data = 1
            _quality_rate += i_o
            quality_list.append({ "label": obj.date, "y": i_o })
            
            # Performance rate
            try:
                performance_data = (total_output / total_cadence)
                performance = performance_data
            except Exception as e:
                performance = 1
                performance_data = 1
            _performance_rate += performance
            performance_rate.append({ "label": obj.date, "y": performance })

            # OEE
            data = (calculation_data * i_o_data * performance_data)
            oee_rate.append({ "label": obj.date, "y": data})
            _oee += data

            # State occurrences Stop
            if obj.state and obj.state.title() == "Stop" and obj.stop and obj.stop.title() not in stop_label_list:
                stop_label_list.append(obj.stop.title())

            # State occurrences Breakdown
            if obj.state and obj.state.title() == "Breakdown" and obj.stop and obj.stop.title() not in breakdown_label_list:
                breakdown_label_list.append(obj.stop.title())
        # Stop
        datapoints = []
        num = 0
        total_stop = 0
        for data in stop_label_list:
            label_count = devices_details.filter(
                stop__icontains=data, state__icontains="Stop"
            ).count()
            total_stop += label_count
            datapoints.append({"label": data, "y": label_count, "color": f"#17{num}EA2" }),
            num += 2
        # Breakdown
        breakdown_datapoints = []
        total_breakdown = 0
        num2 = 0
        for data in breakdown_label_list:
            label_count = devices_details.filter(
                stop__icontains=data, state__icontains="Breakdown"
            ).count()
            total_breakdown += label_count
            breakdown_datapoints.append({ "label": date, "label": data, "color": f"#17{num2}EA2" }),
            num2 += 1

        # Test 2
        all_type = []; date_list = []
        for data in devices_details:
            if data.state and data.state.title() not in all_type:
                all_type.append(data.state.title())

            if data.date and data.date not in date_list:
                date_list.append(data.date)

        data_in_min_list = []
        
        for label in all_type:
            count = 0
            label_list = []
            for date in date_list:
                count += 1
                single_line = devices_details.filter(state__icontains=label, date=date).count()
                data_dic = {'label': date, 'y': single_line}
                label_list.append(data_dic)
            data_in_min_list.append(label_list)
        data_in_min = {}
        for key in all_type:
            for value in data_in_min_list:
                data_in_min[key] = value
                data_in_min_list.remove(value)
                break
        

        try:
            _performance_rate = round(_performance_rate / len(date_list))
        except Exception as e:
            print(e)
            _performance_rate = 0
        try:
            _availability_rate = round(_availability_rate / len(date_list))
        except Exception as e:
            print(e)
            _availability_rate = 0
        try:
            _quality_rate = round(_quality_rate / len(date_list))
        except Exception as e:
            print(e)
            _quality_rate = 0
        try:
            _oee = round(_oee)
        except Exception as e:
            print(e)
            _oee = 0

        context = {
            "mtbf_list": mtbf_list, "mttr_list": mttr_list,
            "oee": _oee, "units_produced": units_produced,
            "all_devices": Devices.objects.filter(owner=request.user, status="Active"),
            "selected": my_device, "availability_rate": _availability_rate,
            "st": datestrt, "quality_rate": _quality_rate,
            "ed": dateend, "scraped_unit": 0, "rate_performance": _performance_rate,
            "mtbf": mtbf,
            "mttr": mttr,
            'data_in_min': data_in_min, "total_breakdown": total_breakdown,
            "total_stop": total_stop, "scraped_unit": scraped_unit,
            "datapoints": datapoints, "breakdown_datapoints": breakdown_datapoints,
            "speed_data": speed_data, "units_produced_list": units_produced_list,
            "availability_list": availability_list, "quality_list": quality_list,
            "performance_rate": performance_rate, "oee_rate": oee_rate,
            "date_list": date_list
        }
        return render(request, "index2.html", context)
    except Exception as e:
        return render(request, "index2.html")


# this is a daily dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('Login')

    device_id = request.GET.get("device_id")
    date = request.GET.get("date")
    if device_id:
        my_device = Devices.objects.get(device_id=device_id)
    else:
        my_device = Devices.objects.filter(owner=request.user).first()
    if not date:
        date = datetime.date.today()
    devices_details = None
    if my_device:
        devices_details = API_Device_data.objects.filter(
            serial_no=my_device.serial_no,
            device_password=my_device.device_password,
            date=date,
        )

        # Chart Data
        product_unit = []
        scraped_unit_list = []
        scraped_unit = 0
        _product_unit = 0

        # product_unit
        for obj in devices_details.distinct('hours'):

            if obj.count_input:
                _data = API_Device_data.objects.filter(
                    serial_no=my_device.serial_no,
                    device_password=my_device.device_password,
                    date=date, hours=obj.hours
                ).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']

                product_unit.append({ "label": obj.hours, "y": int(_data) })
                _product_unit += int(_data)

        # scraped_unit
        for obj in devices_details.distinct('hours'):
            if obj.count_input and obj.count_output:
                # data =  int(obj.count_input) - int(obj.count_output)
                _input = API_Device_data.objects.filter(
                    serial_no=my_device.serial_no,
                    device_password=my_device.device_password,
                    date=date, hours=obj.hours
                ).annotate(as_float=Cast('count_input', FloatField())).aggregate(Sum('as_float'))['as_float__sum']

                _output = API_Device_data.objects.filter(
                    serial_no=my_device.serial_no,
                    device_password=my_device.device_password,
                    date=date, hours=obj.hours
                ).annotate(as_float=Cast('count_output', FloatField())).aggregate(Sum('as_float'))['as_float__sum']
                
                data =  int(_input) - int(_output)
                if data < 0:
                     data = 0
                scraped_unit_list.append(
                    { "label": obj.hours, "y": data }
                )
                scraped_unit += data

        stop_label_list = []
        breakdown_label_list = []

        availability_list = []
        quality_list = []
        performance_rate = []
        oee_rate = []

        total_state = 0
        total_state_off = 0
        total_state_production = 0
        total_output = 0
        total_cadence = 0
        _oee = 0
        _availability = 0
        _quality = 0
        _performance = 0
        for obj in devices_details.distinct('hours'):
            api_device = API_Device_data.objects.filter(
                serial_no=my_device.serial_no,
                device_password=my_device.device_password,
                date=date, hours=obj.hours
            )
            total_state = api_device.count()
            total_state_production = api_device.filter(state__icontains="PRODUCTION").count()
            total_state_off = api_device.filter(state__icontains="OFF").count()
            _total_cadence = api_device.filter(state__icontains="PRODUCTION")
            total_cadence = _total_cadence.annotate(as_float=Cast('cadence', FloatField())).aggregate(Sum('as_float'))['as_float__sum']

            # Availability rate
            try:
                calculation_data = (
                    (total_state - total_state_off - total_state_production) / (total_state - total_state_off)
                )
                # .85 * 100
                calculation = round(calculation_data)
            except Exception as e:
                print(e)
                calculation = 0
                calculation_data = 0
            _availability += calculation
            availability_list.append({ "label": obj.hours, "y": calculation })

            # Quality rate
            _input = obj.count_input
            _output = obj.count_output
            try:
                i_o_data = (float(_output) / float(_input))
                i_o = (round(i_o_data))
            except Exception as e:
                i_o = float(100)
                i_o_data = float(1)
            _quality += round(i_o)
            quality_list.append({ "label": obj.hours, "y": i_o })
            
            # Performance rate
            try:
                performance_data = (total_output / total_cadence)
                performance = round(performance_data)
            except Exception as e:
                performance = float(1)
                performance_data = float(1)
            _performance += round(performance)
            performance_rate.append({ "label": obj.hours, "y": performance })

            # OEE
            data = (calculation_data * i_o_data * performance_data)
            oee_rate.append({ "label": obj.hours, "y": round(data)})
            _oee += round(data)

            # State occurrences Stop
            if obj.state and obj.state.title() == "Stop" and obj.stop and obj.stop.title() not in stop_label_list:
                stop_label_list.append(obj.stop.title())

            # State occurrences Breakdown
            if obj.state and obj.state.title() == "Breakdown" and obj.stop and obj.stop.title() not in breakdown_label_list:
                breakdown_label_list.append(obj.stop.title())
        
        asa = zip(devices_details, availability_list, quality_list, performance_rate, oee_rate)


        # Stop
        datapoints = []
        num = 0
        total_stop = 0
        for data in stop_label_list:
            label_count = devices_details.filter(
                stop__icontains=data, state__icontains="Stop"
            ).count()
            total_stop += label_count
            datapoints.append({"label": data, "y": label_count, "color": f"#17{num}EA2" }),
            num += 2
        # Breakdown
        breakdown_datapoints = []
        total_breakdown = 0
        num2 = 3
        for data in breakdown_label_list:
            label_count = devices_details.filter(
                stop__icontains=data, state__icontains="Breakdown"
            ).count()
            total_breakdown += label_count
            breakdown_datapoints.append({ "y": label_count, "label": data, "color": f"#17{num2}EA2" }),
            num2 += 3

        # Test 2
        all_type = []
        time_list = []
        for data in devices_details:
            if data.state and data.state.title() not in all_type:
                all_type.append(data.state.title())

            if data.hours and data.hours not in time_list:
                time_list.append(data.hours)

        data_in_min_list = []
        for label in all_type:
            count = 0
            label_list = []
            for hours in time_list:
                count += 1
                single_line = devices_details.filter(state__icontains=label, hours=hours).count()
                data_dic = {'label': hours, 'y': single_line}
                label_list.append(data_dic)
            data_in_min_list.append(label_list)
        data_in_min = {}
        for key in all_type:
            for value in data_in_min_list:
                data_in_min[key] = value
                data_in_min_list.remove(value)
                break
        try:
            _performance = round(_performance / len(time_list))
        except Exception as e:
            print(e)
            _performance = 0
        try:
            _availability = round(_availability / len(time_list))
        except Exception as e:
            print(e)
            _availability = 0
        try:
            _quality = round(_quality / len(time_list))
        except Exception as e:
            print(e)
            _quality = 0
        on_to_twt = []
        for i in range(0, 24):
            on_to_twt.append(i)
        context = {
            'product_unit': product_unit, 'scraped_unit_list': scraped_unit_list,
            "all_devices": Devices.objects.filter(owner=request.user, status="Active"),
            "selected": my_device, "st": date, "units_produced": _product_unit, 
            'breakdown_datapoints': breakdown_datapoints, "oee": _oee,
            "availability_list": availability_list,
            'quality_list': quality_list, "performance_rate": performance_rate,
            'datapoints': datapoints, "oee_rate": oee_rate,
            'data_in_min': data_in_min, "total_breakdown": total_breakdown,
            "total_stop": total_stop, "scraped_unit": scraped_unit,
            "mtbf": devices_details.filter(mtbf="1", hours="").count(),
            "mttr": devices_details.filter(mttr="1").count(),
            "devices_details": devices_details.distinct('hours'), "asa": asa, 
            'all_type': all_type, "date": date,
            "availability_rate": _availability, "quality_rate": _quality,
            "performance": _performance, "on_to_twt": on_to_twt
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
