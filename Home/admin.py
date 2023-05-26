from django.contrib import admin
from .models import *

# Register your models here.
class DevicesAdmin(admin.ModelAdmin):

    list_display = ('device_id','serial_no','designation','owner')
admin.site.register(Devices,DevicesAdmin)


@admin.register(API_Device_data)
class API_Device_dataAdmin(admin.ModelAdmin):
    list_display = (
        'device_id','serial_no','device_password','state', 'stop', 'cadence',
        'date', 'time', 'count_input', 'count_output'
    )

    search_fields = ('date', 'serial_no', 'state')
    list_filter = ('hours', )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'api_secret')


@admin.register(FromAddress)
class FromAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'street1', 'is_active')
