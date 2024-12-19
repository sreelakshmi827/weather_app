from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
import requests
import datetime
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
load_dotenv()
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        errors={}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CustomUser.objects.filter(email=email).exists():
            errors["email"]="email already registered"
            #messages.error(request, 'Email is already taken')
            #return render(request,'signup.html')
            print('email already taken')
            return redirect('signup') 
                                                            
        if password==confirm_password:
            user=CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password) 
            user.save()
            return redirect('signin')
        else:   
            errors["confirm_password"]="password do not match"
            # return render(request,'signup.html')
            if errors:
                return render(request,'signup.html',{'errors':errors})
    return render(request,'signup.html')


def signin_view(request):
    if request.method == 'POST': 
        errors={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('weather')
        else:
            errors['user']='user not found'
            #messages.error(request, 'wrong password')
            return redirect('signin')
    return render(request,'signin.html')
def logout_view(request):
    logout(request)
    return redirect('signin')

def home_view(request):
    return render(request,'home.html')

@login_required(login_url='signin')
def weather_view(request):
    errors={}

    if 'city' in request.POST:
        city=request.POST.get('city')
    else:
        city='calicut' 
    APP_ID=os.getenv('APP_ID')     

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}" 
    PARAMS = {'units': 'metric'} #temp in celsius

    try:
        data=requests.get(url,params=PARAMS).json()
        description = data['weather'][0]['description'] 
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today() 

        context={
            'description':description,
            'icon':icon,
            'temp':temp,
            'day':day,
            'city':city,
            'exception_occured': False,
        }
        return render(request,'weather.html',context)  
    
    except KeyError:
        exception_occured =True
        errors['weather']='enentered data is not available to API'
        #messages.error(request,'entered data is not available to API')
        day = datetime.date.today()
    return render(request,'weather.html', {
        'description':'clear sky',
        'icon':'01d',
        'temp':25,
        'day':day,
        'city':'calicut',
        'exception_occured':exception_occured,

    })    
    #return render(request,'weather.html')
