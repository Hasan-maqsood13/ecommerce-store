from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.mail import send_mail
from django.contrib import messages
from django.core import serializers
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings
from datetime import timedelta
from datetime import datetime
from .models import *
import random
import json
import re

# Create your views here.


@csrf_exempt
def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        errors = {}

        if not email:
            errors['email'] = 'Email is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return JsonResponse({'errors': errors}, status=400)

        # ✅ LOGIN
        if action == 'login':
            try:
                user = Registration.objects.get(email=email)
            except Registration.DoesNotExist:
                return JsonResponse({'errors': {'email': 'Email not found.'}}, status=400)

            if not check_password(password, user.password):
                return JsonResponse({'errors': {'password': 'Incorrect password.'}}, status=400)

            if not user.is_verified:
                return JsonResponse({'errors': {'email': 'Account not verified.'}}, status=400)

            request.session['user_id'] = user.id
            request.session['user_role'] = user.role
            request.session['user_name'] = user.username

            if user.role == 'admin':
                redirect_url = 'admindashboard/'
            else:
                redirect_url = ''

            return JsonResponse({'success': True, 'redirect_url': redirect_url})
         # ✅ SIGNUP
        elif action == 'signup':
            # Check if user already exists
            if Registration.objects.filter(email__iexact=email).exists():
                return JsonResponse({'errors': {'email': 'Email already exists'}}, status=400)

            username = request.POST.get('username', email.split('@')[0])
            user = Registration.objects.create(
                email=email,
                username=username,
                password=make_password(password),
                is_verified=True  # Auto verify
            )

            request.session['user_id'] = user.id
            request.session['user_role'] = user.role
            request.session['user_name'] = user.username

            return JsonResponse({
                'success': True,
                'redirect_url': ''
            })
    return render(request, 'store/home.html', {
        'user_id': request.session.get('user_id'),
        'user_role': request.session.get('user_role'),
        'user_name': Registration.objects.get(id=request.session['user_id']).username if request.session.get('user_id') else ''
    })


def logout(request):
    request.session.flush()
    return redirect('home')


def account(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('home')

    try:
        user = Registration.objects.get(id=user_id)
    except Registration.DoesNotExist:
        return redirect('home')

    context = {
        'user': user,  # Pass full user object
    }
    return render(request, 'store/account.html', context)


def shop(request):
    return render(request, 'store/shop.html')


def about(request):
    return render(request, 'store/about.html')


def contact(request):
    return render(request, 'store/contact.html')


def blog(request):
    return render(request, 'store/blog.html')


def wishlist(request):
    return render(request, 'store/wishlist.html')


def cart(request):
    return render(request, 'store/cart.html')


def checkout(request):
    return render(request, 'store/checkout.html')

def admindashboard(request):
    return render(request, 'biguser/dashboard.html')

def viewcategories(request):
    return render(request, 'biguser/addcategories.html')

def addcategories(request):
    return render(request, 'biguser/addcategories.html')

# E-commerce Frontend page with Email send function in signup.
# @csrf_exempt
# def ecommercefrontend(request):
#     if request.method == 'POST':
#         action = request.POST.get('action')

#         email = request.POST.get('email', '').strip()
#         password = request.POST.get('password', '').strip()

#         errors = {}

#         if not email:
#             errors['email'] = 'Email is required.'
#         if not password:
#             errors['password'] = 'Password is required.'

#         if errors:
#             return JsonResponse({'errors': errors}, status=400)

#         # ✅ LOGIN
#         if action == 'login':
#             try:
#                 user = Registration.objects.get(email=email)
#             except Registration.DoesNotExist:
#                 return JsonResponse({'errors': {'email': 'Email not found.'}}, status=400)

#             if not check_password(password, user.password):
#                 return JsonResponse({'errors': {'password': 'Incorrect password.'}}, status=400)

#             if not user.is_verified:
#                 return JsonResponse({'errors': {'email': 'Account not verified.'}}, status=400)

#             request.session['user_id'] = user.id
#             request.session['user_role'] = user.role

#             if user.role == 'admin':
#                 redirect_url = '/admindashboard/'
#             else:
#                 redirect_url = '/ecommercefrontend/'

#             return JsonResponse({'success': True, 'redirect_url': redirect_url})

#         elif action == 'signup':
#             if Registration.objects.filter(email__iexact=email).exists():
#                 return JsonResponse({'errors': {'email': 'Email already exists'}}, status=400)

#             username = request.POST.get('username', email.split('@')[0])

#             verification_code = str(random.randint(
#                 100000, 999999))  # 6 digit code

#             user = Registration.objects.create(
#                 email=email,
#                 username=username,
#                 password=make_password(password),
#                 is_verified=False,  # abhi verify nahi hua
#                 verification_token=verification_code
#             )

#             # Email bhejna
#             subject = "Your Verification Code"
#             message = f"Hi {username},\n\nYour verification code is: {verification_code}\nPlease enter this code on the verification page to activate your account.\n\nThanks!"
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [email]

#             try:
#                 send_mail(subject, message, from_email,
#                           recipient_list, fail_silently=False)
#             except Exception as e:
#                 print(f"Email sending failed: {e}")

#             return JsonResponse({
#                 'success': True,
#                 'redirect_url': '/verification/'
#             })
#     return render(request, 'ecommercefrontend.html')

# def generate_verification_code():
#     """Generate a random 4-digit numeric code"""
#     return str(random.randint(1000, 9999))

# def email_verification(request):
#     email = request.session.get('user_email')  # saved after signup
#     return render(request, 'verification.html', {'email': email})


# @csrf_exempt
# def verify_code(request):
#     if request.method == 'POST':
#         code = request.POST.get('code')
#         try:
#             user = modelname.objects.get(
#                 verification_token=code, is_verified=False)
#             user.is_verified = True
#             user.save()
#             return JsonResponse({'success': True})
#         except modelname.DoesNotExist:
#             return JsonResponse({'error': 'The code you entered is incorrect.'}, status=400)