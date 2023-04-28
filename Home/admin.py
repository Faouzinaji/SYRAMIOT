from django.contrib import admin
from .models import *

# Register your models here.
class DevicesAdmin(admin.ModelAdmin):

    list_display = ('device_id','serial_no','designation','owner')
admin.site.register(Devices,DevicesAdmin)
admin.site.register(API_Device_data)
