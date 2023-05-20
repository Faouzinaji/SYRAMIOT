import datetime
from django.db import models
from dateutil.relativedelta import relativedelta
from authentication.models import User
from Home.models import *
from authentication.models import *


def _get_inv_sl(num):
    today = datetime.date.today()
    year = today.strftime("%Y")
    num = num + 1
    if num > 999999:
        return f"Invoice N° {year}-{num}"
    if num > 99999:
        return f"Invoice N° {year}-0{num}"
    if num > 9999:
        return f"Invoice N° {year}-00{num}"
    if num > 999:
        return f"Invoice N° {year}-000{num}"
    if num > 99:
        return f"Invoice N° {year}-0000{num}"
    if num > 0:
        return f"Invoice N° {year}-00000{num}"


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
    
    @property
    def get_vat(self):
        price = self.subscriber_set.all().last()
        return int(price.price) * 20 / 100

    @property
    def total(self):
        price = self.subscriber_set.all().last()
        return int(price.price) + int(self.get_vat)


class Price_plan_feature(models.Model):
    subplan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)

    # def __str__(self):
    #     return self.title
    class Meta:
        verbose_name = 'Plan Features'


class Subscriber(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True,verbose_name='User'
    )
    plan = models.ForeignKey(Price_plan, on_delete=models.CASCADE, null=True)
    serial_no = models.ForeignKey(
        Devices, on_delete=models.CASCADE, null=True, verbose_name='Serial No.'
    )
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


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    invoice_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=25, null=True, blank=True)
    vat = models.CharField(max_length=25, null=True, blank=True)
    total_amount = models.CharField(max_length=25, null=True, blank=True)

    def save(self, *args, **kwargs):
        invoice_id = self.invoice_id
        if not invoice_id:
            total = Invoice.objects.all().count()
            inv = _get_inv_sl(total)
            self.invoice_id = inv
        if not self.end_date:
            self.end_date = datetime.date.today() + relativedelta(years=1)
        super(Invoice, self).save(*args, **kwargs)
