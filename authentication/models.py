from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Phone No')

    picture = models.ImageField(upload_to='ProfileImages', blank=True, verbose_name='Photo')

    user_selected_timezone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Timezones')
    user_register_at_his_timezones = models.CharField(max_length=70, blank=True, null=True, verbose_name='Register Timezones')

    gender = models.CharField(max_length=25, blank=True, null=True, verbose_name='Gender')
    profession = models.CharField(max_length=25, blank=True, null=True)
    otp = models.CharField(max_length=25, blank=True, null=True, verbose_name='OTP')
    address = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Address 1')
    address2 = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Address 2')
    city = models.CharField(max_length=2500, blank=True, null=True, verbose_name='City')
    state = models.CharField(max_length=2500, blank=True, null=True, verbose_name='State')
    zip_code = models.CharField(max_length=2500, blank=True, null=True, verbose_name='Zip Code')
    changed_default_password = models.CharField(max_length=500, blank=True, default='No', null=True, verbose_name='Changed Default Password?')
    confirmation_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name='Compensation Rate')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated At')


    class Meta:
        verbose_name = 'User Profile'



