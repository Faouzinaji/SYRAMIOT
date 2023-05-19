import pytz
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
from django.contrib import auth,messages

from django.conf import settings

# from Home.decorators import allowed_users
from .models import *
# from Home.models import *

from django.core.mail import send_mail, EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_otp(request, user, user_email, otp):
    pass

 
def Login(request):
    ''' This is the login method '''
    if request.method == 'POST':
        email = request.POST.get('email')
        Password = request.POST.get('password')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('Login')
        if not Password:
            messages.error(request, 'Password is required')
            return redirect('Login')
        x=User.objects.filter(email=email).first()
        print(x)

        user = Profile.objects.filter(owner=x).first()

        if x is None:
            messages.error(request,'No User found with this Email')
            return render(request, 'Login.html')
        else:
            user = auth.authenticate(username=email, password=Password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request,'Account is not activated')
            else:
                messages.warning(request, 'Invalid ID or password')
                return redirect('Login')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'Login.html')


def login_otp(request):
    mobile = request.session['mobile']
    Username = request.session['Username']
    Password = request.session['Password']
    if not mobile:
        messages.error(request, 'Phone No is required')
        return redirect('Login')

    if request.method == 'POST':
        otp = request.POST.get('2facode')
        if not otp:
            messages.error(request, 'OTP required')
            return redirect('login_otp')
        profile = Profile.objects.filter(phone=mobile).first()
        if otp == profile.otp:
            get_user = User.objects.get(username=Username)
            get_user.is_active = True
            get_user.save()
            user = auth.authenticate(username=Username, password=Password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
             messages.warning(request, 'Invalid ID or password')
             return redirect('Login')

        else:
            messages.error(request,'Invalid OTP,please try again')
            return render(request, 'Login_otp.html')

    return render(request, 'Login_otp.html')



def Sign_Up(request):

    if request.method == 'POST':
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        Email = request.POST.get('email')
        country_code = request.POST.get('country_code')
        char1 = '('
        char2 = ')'
        mystr = country_code
        perfect_country_code=mystr[mystr.find(char1) + 1: mystr.find(char2)]
        Phone_no_input = request.POST.get('phone')
        Phone_no = perfect_country_code+Phone_no_input
        Password = request.POST.get('password')
        username = Email
        if not f_name:
            messages.error(request, 'First Name is required')
            return redirect('Sign_up')
        if not l_name:
            messages.error(request, 'Last Name is required')
            return redirect('Sign_up')
        if not Email:
            messages.error(request, 'Email is required')
            return redirect('Sign_up')
        if not Phone_no:
            messages.error(request, 'Phone is required')
            return redirect('Sign_up')
        if not Password:
            messages.error(request, 'Password is required')
            return redirect('Sign_up')
        # try:
        if not User.objects.filter(username=username).exists():
            if not Profile.objects.filter(phone=Phone_no):
                otp = random.randint(100000,999999)
                current_site = get_current_site(request)
                mail_subject = 'Verification Code'
                message = render_to_string('otp_email_template.html', {
                    'first_name': f_name,
                    'last_name': l_name,
                    'domain': current_site.domain,
                    'otp': otp
                })
                all_email = ['adnanrafique340@gmail.com']
                to_email = Email
                all_email.append(to_email)
                email = EmailMultiAlternatives(
                    mail_subject, message, to=all_email
                )
                email.attach_alternative(message, "text/html")
                email.send()
                print("mail send successfully")
                user = User.objects.create_user(
                    first_name=f_name, last_name=l_name, email=Email,
                    username=username, password=Password, is_active=False
                )
                profile = Profile.objects.create(
                    owner=user, phone=Phone_no, otp=otp
                )
                user.save()
                profile.save()
                messages.info(request, 'Account Created Successfully.')
                
                request.session['mobile'] = Phone_no
                request.session['Username'] = Email
                request.session['Password'] = Password
                return redirect('login_otp')
            else:
                messages.info(request,
                                'User is already exist against this Phone No ')
                return redirect('Sign_up')
        else:
            messages.info(request, 'User is already exist against this Email.')
            return redirect('Sign_up')
        # except Exception as e:
        #     print(e, "*" * 10)
        #     messages.info(request, 'Ops something happens unwanted.Contact admin.')
        #     return redirect('Sign_up')
    else:
        return render(request, 'Sign_Up.html')


def Logout(request):
    logout(request)
    messages.info(request,'You have been Logged Out')
    return redirect('Login')


def forget_password(request):
    if request.method == 'POST':
        Username = request.POST.get('un')
        if not Username:
            messages.error(request, 'Email is required')
            return redirect('forget_password')

        user=User.objects.filter(username=Username).first()
        print(user)

        profile= Profile.objects.filter(owner=user).first()
        if user is None:
            messages.error(request,'User not found with this Email')
            return render(request, 'forget-password.html')

        otp = random.randint(100000,999999)
        profile.otp=otp
        profile.save()
        current_site = get_current_site(request)
        mail_subject = 'Verification Code'
        message = render_to_string('otp_email_template.html', {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'domain': current_site.domain,
            'otp': otp
        })
        all_email = []
        to_email = user.email
        all_email.append(to_email)
        email = EmailMultiAlternatives(
            mail_subject, message, to=all_email
        )
        email.attach_alternative(message, "text/html")
        email.send()
        print("mail send successfully")
        request.session['mobile'] = profile.phone
        request.session['Username'] = Username
        return redirect('reset_password')
    return render(request,'forget-password.html')


def reset_password(request):
    mobile = request.session['mobile']
    Username = request.session['Username']
    if request.method == 'POST':
        otp = request.POST.get('2facode')
        profile = Profile.objects.filter(phone=mobile).first()
        if otp == profile.otp:

             request.session['Username'] = Username
             messages.success(request, 'Verification code match successfully')
             return redirect('update_password')
        else:
            messages.error(request,'Invalid OTP,please try again')
            return render(request, 'reset_password_otp.html')

    return render(request, 'reset_password_otp.html')


def update_password(request):
    Username = request.session['Username']
    if request.method == 'POST':
        users = User.objects.get(username=Username)
        new_password = request.POST.get('new_password')
        if len(new_password)!=0:
            users.set_password(new_password)
            users.save()
            messages.info(request, 'Password updated successfully,Please Login with New Set Password')
            return redirect('Login')
    else:
        return render(request,'update_password.html')
