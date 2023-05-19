from django.contrib import admin
from .models import *

# app_models = apps.get_app_config('businessis').get_models()
#
# for model in app_models:
#     admin.site.register(model)

class Price_planAdmin(admin.ModelAdmin):

    list_display = ('id','title','price','highlight_status')

admin.site.register(Price_plan,Price_planAdmin)


class Price_plan_featureAdmin(admin.ModelAdmin):

    list_display = ('subplan','title')

admin.site.register(Price_plan_feature,Price_plan_featureAdmin)



class OrderdevicesAdmin(admin.ModelAdmin):

    list_display = ('id','user_name','email_address','ph_no','delivery_address','number_of_devices','amount','status','created_at')

admin.site.register(Order_devices,OrderdevicesAdmin)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'invoice_id', 'name')


@admin.register(Subscriber)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'price')

