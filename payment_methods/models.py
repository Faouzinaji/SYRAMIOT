from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import User
from authentication.models import User
from Home.models import *

from authentication.models import *


PLAN_CHOICES = (
    ("device", "Device"),
    ("certificate", "Certificate"),
)

class Price_plan(models.Model):
    title = models.CharField(max_length=150)
    plan_choice = models.CharField(
        max_length=255, choices=PLAN_CHOICES, default="device", unique=True
    )
    price = models.IntegerField()
    highlight_status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Price Plan'


class Price_plan_feature(models.Model):
    subplan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)

    # def __str__(self):
    #     return self.title
    class Meta:
        verbose_name = 'Plan Features'


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,verbose_name='User')
    plan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)
    serial_no = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True,verbose_name='Serial No.')
    price = models.CharField(max_length=50)
    subsciption_from = models.DateField(verbose_name='Subscription From')
    subsciption_to = models.DateField(verbose_name='Subscription To')
    status = models.CharField(default='Expire',max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = 'Certificates'


class Order_devices(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user_name = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Full Name')
    email_address = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Email')
    ph_no = models.BigIntegerField( blank=True, null=True, verbose_name='Phone No')
    delivery_address = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Device Delivery Address')
    street_number = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Street No.')
    route = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Route')
    city = models.CharField(max_length=2500, blank=True, null=True, verbose_name='City')
    state = models.CharField(max_length=2500, blank=True, null=True, verbose_name='State')
    zip_code = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Zip Code')
    country = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Country')
    address_verified = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Address Verified by Google?')

    number_of_devices = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Number Of Devices')
    amount = models.BigIntegerField( blank=True, null=True, verbose_name='Total Paid Amount')
    status =  models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name = 'Order-Devices-Details'