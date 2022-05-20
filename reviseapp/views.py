from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Registration, Movies, contact
import math, random
from django.db.models import Q
import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from requests.packages import urllib3
import requests
from itertools import chain
from django.core.mail import send_mail
urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'


def Index(request):
    return render(request, 'index.html')


def Login(request):
    if request.method == 'POST':
        login_email = request.POST['username']
        login_password = request.POST['password']
        user = authenticate(username=login_email, password=login_password)
        if Registration.objects.filter(email=login_email).exists() and user is not None:
            login(request, user)
            return redirect('Dashboard')
        else:
            messages.error(request, "Try Again: Incorrect Username or password")
            return redirect('Login')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST' or request.FILES:
        username = request.POST['username']
        phone = request.POST['phone']
        language = request.POST['language']
        genre = request.POST['genre']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['repassword']
        if password != re_password:
            messages.error(request, "Enter Password Doesn't match. Try Again...")
            return redirect('signup')
        if len(password) < 6:
            messages.error(request, "Entered Password is weak. Try Again...")
            return redirect('signup')
        if len(username) < 4:
            messages.error(request, "Use Valid Name. Try Again...")
            return redirect('signup')
        if Registration.objects.filter(email = email).exists():
            messages.error(request, "User Already Exist...")
            return redirect('Login')
        data = Registration(username=username, email=email, phone_number = phone, language = language, genre = genre)
        data.save()
        user = User.objects.create_user(username=email, password=password)
        user.is_active = False
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        send_mail(
            'Revise Advice OTP Verification',
            'Thank you, For Registering in Revise Advice your OTP is ' + OTP +'\n\nUsername: '+ email +'\nPassword: '+ password,
            'from@example.com',
            [email],
            fail_silently=True,
        )
        mail = str(OTP)+email
        user.save()
        return render(request, 'register_otp.html', {'username': mail})
    return render(request, 'regestration.html')


def register_otp(request):
    if request.method == "POST":
        access = request.POST['secure']
        email = request.POST['username']
        if access == email[:4]:
            user = User.objects.get(username= email[4:])
            user.is_active = True
            user.save()
            messages.error(request, "User Registered Successfully...")
            return render(request, 'index.html')
        else:
            messages.error(request, "Wrong OTP Try Again...")
            return render(request, 'register_otp.html', {'username': email})


@login_required
def Dashboard(request):
    username = request.user.username
    user = Registration.objects.get(email=username)
    genre = user.genre.split(",")
    language = ["hindi", "english"]
    for language_user in language:
        for data in genre:
            movies = Movies.objects.filter(Q(genre__icontains=data) | Q(language=language_user))
    return render(request, 'dashboard.html', {'top': movies})


@login_required
def Category(request, genre):
    username = request.user.username
    user = Registration.objects.get(email=username)
    language = user.language.split(",")
    for language_user in language:
        movie = Movies.objects.filter(Q(genre__icontains=genre) | Q(language=language_user))
    return render(request, 'category.html', {'movie': movie, 'genre': genre})


@login_required
def view(request, sno):
    id = Movies.objects.get(sno=sno)
    for genre in id.genre.split(","):
        next = Movies.objects.filter(Q(genre__icontains= genre) | Q(language=id.language))
    next = next.exclude(sno = sno)
    return render(request,'videoplayer.html', {'movie': id, "next": next[:3]})


@login_required
def profile(request):
    username = request.user.username
    register = Registration.objects.get(email=username)
    return render(request, "profile.html", {'profile': register})


def Contact(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        message = request.POST['message']
        contact_detail = contact(name= name, email=email, phone_number=number, message=message)
        contact_detail.save()
        messages.success(request, "Our Team Will Contact You Shortly...")
        return redirect('Dashboard')
    return render(request, "contact.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect('Login')
