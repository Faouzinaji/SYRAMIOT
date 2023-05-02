import easypost
from django.http import JsonResponse
from Home.models import APIKey, FromAddress

def get_easypost_rates(name, street, city, state, zip_code, country, phone):
    api = APIKey.objects.get(api_code='cost')
    from_address = FromAddress.objects.get(is_active=True)
    print(from_address.name, from_address.street1, from_address.city)
    easypost.api_key = api.api_key
    from_address = easypost.Address.create(
        name=from_address.name,
        street1=from_address.street1,
        city=from_address.city,
        state=from_address.state,
        zip=from_address.zip,
        country=from_address.country,
        phone=from_address.phone
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

