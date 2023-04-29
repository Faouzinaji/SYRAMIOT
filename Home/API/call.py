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



# def get_request(request):
# 	url = "https://api-mock.dhl.com/mydhlapi/shipments"

# 	payload = {
# 		"plannedShippingDateAndTime": "2019-08-04T14:00:31GMT+01:00",
# 		"pickup": {
# 			"isRequested": False,
# 			"closeTime": "18:00",
# 			"location": "reception",
# 			"specialInstructions": [
# 				{
# 					"value": "please ring door bell",
# 					"typeCode": "TBD"
# 				}
# 			],
# 			"pickupDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"pickupRequestorDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			}
# 		},
# 		"productCode": "D",
# 		"localProductCode": "D",
# 		"getRateEstimates": False,
# 		"accounts": [
# 			{
# 				"typeCode": "shipper",
# 				"number": "BDllJbs-0001"
# 			}
# 		],
# 		"valueAddedServices": [
# 			{
# 				"serviceCode": "II",
# 				"value": 100,
# 				"currency": "GBP",
# 				"method": "cash",
# 				"dangerousGoods": [
# 					{
# 						"contentId": "908",
# 						"dryIceTotalNetWeight": 12,
# 						"customDescription": "1 package Lithium ion batteries in compliance with Section II of P.I. 9661",
# 						"unCodes": [1234]
# 					}
# 				]
# 			}
# 		],
# 		"outputImageProperties": {
# 			"printerDPI": 300,
# 			"customerBarcodes": [
# 				{
# 					"content": "barcode content",
# 					"textBelowBarcode": "text below barcode",
# 					"symbologyCode": "93"
# 				}
# 			],
# 			"customerLogos": [
# 				{
# 					"fileFormat": "PNG",
# 					"content": "base64 encoded image"
# 				}
# 			],
# 			"encodingFormat": "pdf",
# 			"imageOptions": [
# 				{
# 					"typeCode": "label",
# 					"templateName": "ECOM26_84_001",
# 					"isRequested": True,
# 					"hideAccountNumber": False,
# 					"numberOfCopies": 1,
# 					"invoiceType": "commercial",
# 					"languageCode": "eng",
# 					"languageCountryCode": "br",
# 					"encodingFormat": "png",
# 					"renderDHLLogo": False,
# 					"fitLabelsToA4": False,
# 					"labelFreeText": "string",
# 					"labelCustomerDataText": "string"
# 				}
# 			],
# 			"splitTransportAndWaybillDocLabels": True,
# 			"allDocumentsInOneImage": True,
# 			"splitDocumentsByPages": True,
# 			"splitInvoiceAndReceipt": True,
# 			"receiptAndLabelsInOneImage": True
# 		},
# 		"customerReferences": [
# 			{
# 				"value": "Customer reference",
# 				"typeCode": "CU"
# 			}
# 		],
# 		"identifiers": [
# 			{
# 				"typeCode": "shipmentId",
# 				"value": "1234567890",
# 				"dataIdentifier": "00"
# 			}
# 		],
# 		"customerDetails": {
# 			"shipperDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"receiverDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"buyerDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "buyer@domain.com",
# 					"phone": "+44123456789",
# 					"mobilePhone": "+42123456789",
# 					"companyName": "Customer Company Name",
# 					"fullName": "Mark Companer"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"importerDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"exporterDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"sellerDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"payerDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": [
# 					{
# 						"name": "Russian Bank Name",
# 						"settlementLocalCurrency": "RUB",
# 						"settlementForeignCurrency": "USD"
# 					}
# 				],
# 				"typeCode": "business"
# 			},
# 			"ultimateConsigneeDetails": {
# 				"postalAddress": {
# 					"postalCode": "14800",
# 					"cityName": "Prague",
# 					"countryCode": "CZ",
# 					"provinceCode": "CZ",
# 					"addressLine1": "V Parku 2308/10",
# 					"addressLine2": "addres2",
# 					"addressLine3": "addres3",
# 					"countyName": "Central Bohemia",
# 					"provinceName": "Central Bohemia",
# 					"countryName": "Czech Republic"
# 				},
# 				"contactInformation": {
# 					"email": "that@before.de",
# 					"phone": "+1123456789",
# 					"mobilePhone": "+60112345678",
# 					"companyName": "Company Name",
# 					"fullName": "John Brew"
# 				},
# 				"registrationNumbers": [
# 					{
# 						"typeCode": "VAT",
# 						"number": "CZ123456789",
# 						"issuerCountryCode": "CZ"
# 					}
# 				],
# 				"bankDetails": {
# 					"typeCode": "VAT",
# 					"number": "CZ123456789",
# 					"issuerCountryCode": "CZ"
# 				},
# 				"typeCode": "string"
# 			}
# 		},
# 		"content": {
# 			"packages": [
# 				{
# 					"typeCode": "2BP",
# 					"weight": 22.501,
# 					"dimensions": {
# 						"length": 15.001,
# 						"width": 15.001,
# 						"height": 40.001
# 					},
# 					"customerReferences": [
# 						{
# 							"value": "Customer reference",
# 							"typeCode": "CU"
# 						}
# 					],
# 					"identifiers": [
# 						{
# 							"typeCode": "shipmentId",
# 							"value": "1234567890",
# 							"dataIdentifier": "00"
# 						}
# 					],
# 					"description": "Piece content description",
# 					"labelBarcodes": [
# 						{
# 							"position": "left",
# 							"symbologyCode": "93",
# 							"content": "string",
# 							"textBelowBarcode": "text below left barcode"
# 						}
# 					],
# 					"labelText": [
# 						{
# 							"position": "left",
# 							"caption": "text caption",
# 							"value": "text value"
# 						}
# 					],
# 					"labelDescription": "bespoke label description"
# 				}
# 			],
# 			"isCustomsDeclarable": True,
# 			"declaredValue": 150,
# 			"declaredValueCurrency": "CZK",
# 			"exportDeclaration": {
# 				"lineItems": [
# 					{
# 						"number": 1,
# 						"description": "line item description",
# 						"price": 150,
# 						"quantity": {
# 							"value": 1,
# 							"unitOfMeasurement": "BOX"
# 						},
# 						"commodityCodes": [
# 							{
# 								"typeCode": "outbound",
# 								"value": 851713
# 							}
# 						],
# 						"exportReasonType": "permanent",
# 						"manufacturerCountry": "CZ",
# 						"exportControlClassificationNumber": "US123456789",
# 						"weight": {
# 							"netValue": 10,
# 							"grossValue": 10
# 						},
# 						"isTaxesPaid": True,
# 						"additionalInformation": ["string"],
# 						"customerReferences": [
# 							{
# 								"typeCode": "AFE",
# 								"value": "custref123"
# 							}
# 						],
# 						"customsDocuments": [
# 							{
# 								"typeCode": "972",
# 								"value": "custdoc456"
# 							}
# 						]
# 					}
# 				],
# 				"invoice": {
# 					"number": "12345-ABC",
# 					"date": "2020-03-18",
# 					"signatureName": "Brewer",
# 					"signatureTitle": "Mr.",
# 					"signatureImage": "Base64 encoded image",
# 					"instructions": ["string"],
# 					"customerDataTextEntries": ["string"],
# 					"totalNetWeight": 999999999999,
# 					"totalGrossWeight": 999999999999,
# 					"customerReferences": [
# 						{
# 							"typeCode": "CU",
# 							"value": "custref112"
# 						}
# 					],
# 					"termsOfPayment": "100 days",
# 					"indicativeCustomsValues": {
# 						"importCustomsDutyValue": 150.57,
# 						"importTaxesValue": 49.43
# 					}
# 				},
# 				"remarks": [{"value": "declaration remark"}],
# 				"additionalCharges": [
# 					{
# 						"value": 10,
# 						"caption": "fee",
# 						"typeCode": "freight"
# 					}
# 				],
# 				"destinationPortName": "port details",
# 				"placeOfIncoterm": "port of departure or destination details",
# 				"payerVATNumber": "12345ED",
# 				"recipientReference": "recipient reference",
# 				"exporter": {
# 					"id": "123",
# 					"code": "EXPCZ"
# 				},
# 				"packageMarks": "marks",
# 				"declarationNotes": [{"value": "up to three declaration notes"}],
# 				"exportReference": "export reference",
# 				"exportReason": "export reason",
# 				"exportReasonType": "permanent",
# 				"licenses": [
# 					{
# 						"typeCode": "export",
# 						"value": "license"
# 					}
# 				],
# 				"shipmentType": "personal",
# 				"customsDocuments": [
# 					{
# 						"typeCode": "972",
# 						"value": "custdoc445"
# 					}
# 				]
# 			},
# 			"description": "shipment description",
# 			"USFilingTypeValue": "12345",
# 			"incoterm": "DAP",
# 			"unitOfMeasurement": "metric"
# 		},
# 		"documentImages": [
# 			{
# 				"typeCode": "INV",
# 				"imageFormat": "PDF",
# 				"content": "base64 encoded image"
# 			}
# 		],
# 		"onDemandDelivery": {
# 			"deliveryOption": "servicepoint",
# 			"location": "front door",
# 			"specialInstructions": "ringe twice",
# 			"gateCode": "1234",
# 			"whereToLeave": "concierge",
# 			"neighbourName": "Mr.Dan",
# 			"neighbourHouseNumber": "777",
# 			"authorizerName": "Newman",
# 			"servicePointId": "SPL123",
# 			"requestedDeliveryDate": "2020-04-20"
# 		},
# 		"requestOndemandDeliveryURL": False,
# 		"shipmentNotification": [
# 			{
# 				"typeCode": "email",
# 				"receiverId": "receiver@email.com",
# 				"languageCode": "eng",
# 				"languageCountryCode": "UK",
# 				"bespokeMessage": "message to be included in the notification"
# 			}
# 		],
# 		"prepaidCharges": [
# 			{
# 				"typeCode": "freight",
# 				"currency": "CZK",
# 				"value": 200,
# 				"method": "cash"
# 			}
# 		],
# 		"getTransliteratedResponse": False,
# 		"estimatedDeliveryDate": {
# 			"isRequested": False,
# 			"typeCode": "QDDC"
# 		},
# 		"getAdditionalInformation": [
# 			{
# 				"typeCode": "pickupDetails",
# 				"isRequested": True
# 			}
# 		],
# 		"parentShipment": {
# 			"productCode": "s",
# 			"packagesCount": 1
# 		}
# 	}
# 	headers = {
# 		"content-type": "application/json",
# 		"Message-Reference": "",
# 		"Message-Reference-Date": "",
# 		"Plugin-Name": "",
# 		"Plugin-Version": "",
# 		"Shipping-System-Platform-Name": "",
# 		"Shipping-System-Platform-Version": "",
# 		"Webstore-Platform-Name": "",
# 		"Webstore-Platform-Version": "",
# 		"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJhcGk6Ly84YmIxMjk5ZS1mMWYxLTQzZGItOGNiZC05ZGUzNjNhMDZkZWYiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82MzljNGFjNS1jY2VkLTQ4NzgtOWRlMC1mODgyNjJhNmIzMzQvIiwiaWF0IjoxNjgyNDkzNjEzLCJuYmYiOjE2ODI0OTM2MTMsImV4cCI6MTY4MjQ5NzUxMywiYWlvIjoiRTJaZ1lLZ1JQblBzWWkxclc4VHBpMlpad3MxL0FRPT0iLCJhcHBpZCI6IjlkMzUwODY0LWU1ZTMtNDU4Mi05YmM3LTE4MWZiZjQ0YWI3OCIsImFwcGlkYWNyIjoiMSIsImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzYzOWM0YWM1LWNjZWQtNDg3OC05ZGUwLWY4ODI2MmE2YjMzNC8iLCJvaWQiOiI2MTVlYTc4MC01NjBlLTQ4NmItOWE2NS01YjE5ZTg3MWRkMzUiLCJyaCI6IjAuQVY4QXhVcWNZLTNNZUVpZDRQaUNZcWF6Tko0cHNZdng4ZHREakwyZDQyT2diZTlmQUFBLiIsInN1YiI6IjYxNWVhNzgwLTU2MGUtNDg2Yi05YTY1LTViMTllODcxZGQzNSIsInRpZCI6IjYzOWM0YWM1LWNjZWQtNDg3OC05ZGUwLWY4ODI2MmE2YjMzNCIsInV0aSI6InR1Rnpud1RhUEVPY1hTcVFndW9VQUEiLCJ2ZXIiOiIxLjAifQ.ncFuUis-w6z5qTAdUKUxzqudAAgouYf4Mj4YLQ3zQq4Nd-tJoCSKnaAxcurgU8sUjx9Xa0ylI8BVtVzHEe-Fyf7Jl2eQQ8Ycwf3fRZ_Z_HdLFUYMwY1tAetaS-ZSAYll647CYRBBHBI-UIX1wPQEVn7gffL-XAtrWURF4gJhWPV-trDQ9jrRTI0qGC073EDEH3MTty5u_yN_JSU_QdM0EkhBQkrplYtTGDgLEZ8SiJ5HqPOOn6jX65fcZ0HtA0UYghMBHvvxhFSLInyZnz1uIgvR6OE6IEX-Jtf7qSDMln5o08hJe0Ftmo4qOSZcCVrqaMDtx7ohCTRaXjXjjhqUaA"
# 	}

# 	response = requests.request("POST", url, json=payload, headers=headers)

# 	print(response.text)
# 	return HttpResponse(response.text)


# def get_request(request):
#     url = "https://api.shipengine.com/v1/rates"
#     headers = {
#         'Content-Type': 'application/json',
#         'API-KEY': "TEST_BR8coPZX/fSg8Td4YvUZRQ7oHAXF2y9SRiKbLHesvBY",
#         }
#     body = {
# 	"rate_options": {
# 		"carrier_ids": [
# 			"{{stamps_com}}",
# 			"{{fedex}}",
# 			"{{ups}}"
# 		],
# 		"service_codes": [
# 			"usps_priority_mail",
# 			"fedex_ground",
# 			"ups_ground"
# 		]
# 	},
# 	"shipment": {
# 		"ship_from": {
# 			"name": "John Doe",
# 			"company_name": "Example Corp.",
# 			"address_line1": "4009 Marathon Blvd",
# 			"city_locality": "Austin",
# 			"state_province": "TX",
# 			"postal_code": "78756",
# 			"country_code": "US",
# 			"phone": "512-555-5555"
# 		},
# 		"ship_to": {
# 			"name": "Amanda Miller",
# 			"address_line1": "525 S Winchester Blvd",
# 			"city_locality": "San Jose",
# 			"state_province": "CA",
# 			"postal_code": "95128",
# 			"country_code": "US"
# 		},
# 		"packages": [
# 			{
# 				"weight": {
# 					"value": 17,
# 					"unit": "pound"
# 				},
# 				"dimensions": {
# 					"length": 36,
# 					"width": 12,
# 					"height": 24,
# 					"unit": "inch"
# 				}
# 			}
# 		]
# 	}
# }
#     response = requests.request("POST", url, headers=headers, data=body)
#     print(response.text)
#     return HttpResponse(response.text)

