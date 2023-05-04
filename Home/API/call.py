import requests
import base64
from django.shortcuts import render
from django.http import JsonResponse

api_key_pub = 'rayhunboss27@gmail.com',
api_secret_pub = 'A41424344i'
# api_key_pub = '797ZRUYPG47DXH6XTVf29lJI5co6aJpR',
# api_secret_pub = '1kwGh8ScPmKVZnBd'
account_number_pub = "BDllJbs-0001"


def generate_auth_header(api_key, api_secret):
    auth_string = f"{api_key}:{api_secret}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()
    return encoded_auth_string
    auth_header = {"Authorization": f"Basic {encoded_auth_string}"}
    return auth_header

auth = generate_auth_header(api_key_pub, api_secret_pub)
# print(auth)

def get_dhl_rate():
    url = 'https://api.dhl.com/rate'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic KCdyYXlodW5ib3NzMjdAZ21haWwuY29tJywpOkE0MTQyNDM0NGk=',
    }
    data = {
        'getRateRequest': {
            'ClientDetails': {
                'ApplicationID': '1234567890',
                'SiteID': '1234567890',
                'Password': '1234567890',
            },
            'From': {
                'CountryCode': 'US',
                'Postalcode': '90210',
            },
            'BkgDetails': {
                'PaymentCountryCode': 'US',
                'Date': '2022-04-28',
                'ReadyTime': 'PT10H21M',
                'DimensionUnit': 'IN',
                'WeightUnit': 'LB',
                'Pieces': {
                    'Piece': {
                        'PieceID': '1',
                        'Height': '10',
                        'Depth': '10',
                        'Width': '10',
                        'Weight': '1',
                    },
                },
            },
            'To': {
                'CountryCode': 'GB',
                'Postalcode': 'W1B 5TB',
            },
        },
    }
    response = requests.post(url, json=data, headers=headers)
    print(response, "*" * 10)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_dhl_rates_view(request):
    rates = get_dhl_rate()
    print(rates)
    if rates is not None:
        return JsonResponse(rates)
    else:
        return JsonResponse({'error': 'Unable to retrieve rates from DHL API.'})
    # else:
    #     return render(request, 'rate.html')
