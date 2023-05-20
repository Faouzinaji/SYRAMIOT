import stripe
import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.generic import View
from .models import *
from Home.models import APIKey

from Home.API import get_easypost_rates


def checkout(request):
    if request.method == 'POST':
        sr_no_devices = request.POST.getlist('id[]')
        device = Devices.objects.filter(device_id__in=sr_no_devices)
        price = Price_plan.objects.get(plan_choice="certificate")
        total_amount = 0
        for obj in device:
            total_amount += price.price
        request.session['sr_no_devices'] = sr_no_devices
        vat = (total_amount * 20) / 100
        context = {
            'sr_no_devices': sr_no_devices, 'price': price, "vat": vat,
            'no_of_items': total_amount, 'device': device,
            "total_amount": int(total_amount + vat)

        }
        return render(request, 'checkout.html', context)


def checkout_page(request):

    sr_no_devices = request.session.get('sr_no_devices')
    device = Devices.objects.filter(device_id__in=sr_no_devices)
    price = Price_plan.objects.get(plan_choice="certificate")
    total_amount = 0
    for obj in device:
        total_amount += price.price
    vat = (total_amount * 20) / 100
    context = {
        'sr_no_devices': sr_no_devices, 'price': price, "vat": vat,
        'no_of_items': total_amount, 'device': device,
        "total_amount": int(total_amount + vat)
    }
    return render(request, 'checkout.html', context)


def checkout_session(request, billing_id):
    stripe_api = APIKey.objects.get(api_code='stripe')
    stripe.api_key = stripe_api.api_secret
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'SYRAM Web System',
                },
                'unit_amount': billing_id * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{request.build_absolute_uri("/")}'+'payments/payment_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=f'{request.build_absolute_uri("/")}payments/payment_cancel',
        client_reference_id=billing_id
    )

    return redirect(session.url, code=303)


def checkout_session_for_buy_devices(request):
    no_of_devices = int(request.session.get('no_of_devices'))
    # data
    delivery_destination = request.session["delivery_destination"]
    street = request.session["street"]
    road = request.session["road"]
    city = request.session["city"]
    state = request.session["state"]
    zip_code = request.session["zip_code"]
    country = request.session["country"]
    ph_no = request.session["ph_no"]
    name = request.session["name"]
    rate = get_easypost_rates(name, street, city, state, zip_code, country, ph_no)
    rate = rate[0]
    item = Price_plan.objects.get(plan_choice='device')
    stripe_api = APIKey.objects.get(api_code='stripe')
    stripe.api_key = stripe_api.api_secret
    _rate = float(rate) * 100
    _rate = int(_rate)
    # print(customer)
    session = stripe.checkout.Session.create(
        shipping_options=[
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": _rate, "currency": "usd"},
                    "display_name": "Next day air",
                    "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": 1},
                    "maximum": {"unit": "business_day", "value": 1},
                    },
                }
            },
        ],
            payment_method_types=['card'],
            line_items=[
            {
                'name': 'SYRAM Web System',
                'description': f'Product quantity {no_of_devices} and amount {item.price}',
                'amount': item.price * 100,
                'currency': 'usd',
                'quantity': no_of_devices,
            },
            ],
            mode='payment',

            success_url=f'{request.build_absolute_uri("/")}'+'payments/order_payment_success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=f'{request.build_absolute_uri("/")}payments/payment_cancel',

            client_reference_id=no_of_devices,
        )

    context = {
        'price': item.price,
        'total': float(item.price * no_of_devices) + float(rate),
        'sub_total': float(item.price * no_of_devices),
        'url': session.url, 'no_of_devices': no_of_devices,
        'delivery_destination': delivery_destination,
        'street': street,
        'road': road,
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'country': country,
        'ph_no': ph_no,
        'name': name,
        'rate': rate
    }
    return render(request, 'overview.html', context)
    # return redirect(session.url, code=200)



def stripe_buy_devices_payment_success(request):
    # try:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        delivery_destination  = request.session.get('delivery_destination')
        street  = request.session.get('street')
        road  = request.session.get('road')
        city  = request.session.get('city')
        state  = request.session.get('state')
        zip_code  = request.session.get('zip_code')
        country  = request.session.get('country')
        address_verified  = request.session.get('address_verified')
        ph_no = request.session.get('ph_no')
        name = request.session.get('name')
        amount_paid = request.session.get('amount_paid')
        no_of_devices = session.client_reference_id
        Order_devices.objects.create(
                    user_name=name,
                    email_address=request.user,
                    ph_no=int(ph_no),
                    amount = int(amount_paid),
                    delivery_address=delivery_destination,
                    street_number=street,
                    route=road,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    country=country,
                    address_verified=address_verified,
                    number_of_devices=str(no_of_devices),
                    status="Paid"
                )
        return render(request, 'payment_success.html')
    # except Exception as e:
    #     print('line no 98 exception:', e)
    #     return render(request, 'payment_cancel.html')


def stripe_payment_success(request):
    try:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        plan_id = session.client_reference_id
        plan = Price_plan.objects.get(plan_choice="certificate")
        user = request.user
        sr_no_devices = request.session.get('sr_no_devices')

        all_email = []
        total_device = Devices.objects.filter(device_id__in=sr_no_devices).count()
        invoice = Invoice.objects.create(user=user)
        price = int(plan.price) * total_device
        vat = price * (20 * total_device) / (100 * total_device)
        _total_amount = price + vat
        invoice.amount = price
        invoice.vat = vat
        invoice.total_amount = _total_amount
        invoice.save()

        for  i in sr_no_devices:
            obj_device = Devices.objects.get(device_id=i)
            obj_device.status = "Active"
            obj_device.inv_id = invoice
            if obj_device.email not in all_email:
                all_email.append(obj_device.email)
            obj_device.save()

            Subscriber.objects.create(
                plan=plan,
                user=user,
                serial_no=obj_device,
                price=plan.price,
                status='Active',
                subsciption_from=datetime.date.today(),
                subsciption_to=datetime.date.today() + relativedelta(years=1)

            )

        obj_device = Devices.objects.filter(device_id__in=sr_no_devices)
        _user = User.objects.get(pk=request.user.pk)
        context = {
            "invoice": invoice, "total_amount": _total_amount, "price": plan,
            "sub_total": int(plan.price) * obj_device.count() , "total_vat": vat,
            "qt": obj_device.count(), "obj_device": obj_device,
            "user": _user
        }
        
        current_site = get_current_site(request)
        mail_subject = f'Invoice'
        message = render_to_string('invoice.html', {
            'domain': current_site.domain,
            "invoice": invoice, "total_amount": _total_amount, "price": plan,
            "sub_total": int(plan.price) * obj_device.count() , "total_vat": vat,
            "Show": False, "user": _user
        })
        email = EmailMultiAlternatives(
            mail_subject, message, to=all_email
        )
        email.attach_alternative(message, "text/html")
        email.send()
        print("Mail Sent Success =====================")

        return render(request, 'payment_success.html', context)
    except Exception as e:
        print('exception in stripe success is:',e)
        sr_no_devices = request.session.get('sr_no_devices')
        plan = Price_plan.objects.get(plan_choice="certificate")
        invoice = Invoice.objects.all().last()
        obj_device = Devices.objects.filter(device_id__in=sr_no_devices)
        context = {
            "obj_device": obj_device,  "price": plan, "invoice": invoice,
            "sub_total": int(plan.price) * obj_device.count() , 
        }
        return render(request, 'payment_success.html', context)


class PaymentHistory(View):
    def get(self, request):
        invoice = Invoice.objects.filter(user=request.user)
        return render(request, "history.html", {"invoice": invoice})


class InvoiceView(View):
    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        price = Price_plan.objects.get(plan_choice = "certificate")
        sub_total = 0
        total_vat = 0
        for obj in invoice.inv_id.all():
            sub_total += price.price
            total_vat += int(price.price) * 20 / 100
        total_amount = sub_total + total_vat
        _user = User.objects.get(pk=request.user.pk)
        context = {
            "invoice": invoice, "total_amount": total_amount, "price": price,
            "sub_total": sub_total, "total_vat": total_vat, "Show": True,
            "user": _user
        }
        return render(request, "invoice.html", context)
        




def payment_cancel(request):
    return render(request, 'payment_cancel.html')