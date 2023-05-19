from django.db import models
from authentication.models import *
# from payment_methods.models import Price_plan

# Create your models here.

class Devices(models.Model):
    device_id = models.AutoField(primary_key=True, unique=True)
    inv_id = models.ForeignKey(
        "payment_methods.Invoice", on_delete=models.CASCADE, null=True, blank=True,
        related_name="inv_id"
    )
    serial_no = models.PositiveIntegerField( blank=True, null=True, verbose_name='Serial No')
    designation = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Designation')
    device_password = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Password')
    status =  models.CharField(default='Un Activated',max_length=50,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='User')
    email = models.EmailField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated At')

    # def __str__(self):
    #     return self.serial_no

    class Meta:
        verbose_name = 'My Device'
    
    # @property
    # def get_vat(self):
    #     price = self.subscriber_set.all().last()
    #     print(int(price.price) * 20/ 100, "*" * 10, price.price)
    #     return int(price.price) * 20 / 100

    # @property
    # def total(self):
    #     price = self.subscriber_set.all().last()
    #     # print(int(price.price), int(self.get_vat), "*" * 100)
    #     return int(price.price) + int(self.get_vat)


class API_Device_data(models.Model):
    device_id = models.AutoField(primary_key=True, unique=True)
    serial_no = models.CharField( max_length=2500,blank=True, null=True, verbose_name='Serial No')
    device_password = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Password')
    date = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Date')
    time = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Time')
    hours = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Hours')
    count_input = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Count Input')
    count_output = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Count Output')
    state = models.CharField(max_length=2500, blank=True, null=True, verbose_name='State')
    cadence = models.CharField(max_length=2500, blank=True, null=True, verbose_name='cadence')
    stop = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='stop'
    )
    mtbf = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='MTBF'
    )
    mttr = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='MTTR'
    )

    # def __str__(self):
    #     return self.device_id

    class Meta:
        verbose_name = 'My IOT Device Date'


class APIKey(models.Model):
    api_name = models.CharField(max_length=255)
    api_code = models.CharField(max_length=255, unique=True)
    api_secret = models.TextField(null=True, blank=True)
    api_key = models.TextField(null=True, blank=True)
    api_auth = models.TextField(null=True, blank=True)
    account_sid = models.TextField(null=True, blank=True)
    publish_key = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.api_name


class FromAddress(models.Model):
    name = models.CharField(max_length=255)
    street1 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
