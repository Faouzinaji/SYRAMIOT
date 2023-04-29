import easypost
from django.http import JsonResponse

def get_easypost_rates(name, street, city, state, zip_code, country, phone):
    easypost.api_key = 'EZTKb8008cfa378e4000994fe79f1db345b4agufqsD0IDXy4wjFWVF61w'
    from_address = easypost.Address.create(
        name='John Doe',
        street1='123 Main St',
        city='New York',
        state='NY',
        zip='10001',
        country='US',
        phone='555-555-5555'
    )
    to_address = easypost.Address.create(
        name=name,
        street1=street,
        city=city,
        state=state,
        zip=zip_code,
        country=country,
        phone=phone
    )
    parcel = easypost.Parcel.create(
        length=10.0,
        width=10.0,
        height=10.0,
        weight=1.0,
    )
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
    )
    rates = shipment.rates
    print(rates)
    if len(rates) > 0:
        return [rate.rate for rate in rates]
    else:
        return None


def get_rates(request):
    name = "Rayhan"
    street = "" 
    city = "Dhaka"
    state = ""
    zip_code = "1216"
    country = "BD"
    phone = "01710152004"
    rates = get_easypost_rates(name, street, city, state, zip_code, country, phone)
    if rates is not None:
        return JsonResponse({'rates': rates})
    else:
        return JsonResponse({'error': 'Unable to retrieve rates from EasyPost API.'})

