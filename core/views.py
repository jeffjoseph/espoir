from ast import IsNot
from operator import is_not
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile

@login_required(login_url='signin')
def index(request):
    return render(request,'index.html')

def signup(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                messages.info(request,'saved the profile')
                return redirect('signup')
        else:
            messages.info(request,'Passwords Not Mathcing')
            return redirect('signup')
        
    else:
        return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Is Not Valid')
            return redirect('signin')
    else:
        return render(request,'signin.html')

@login_required(login_url='signin') 
def logout(request):
    auth.logout(request)
    return redirect('signin')  

@login_required(login_url='signin') 
def settings(request):
    
    user_profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        print("\n\n\n\n in settings")
        if request.FILES.get('profileimg')==None:
            print("\n\n\n not gettin")
            image=user_profile.profileimg
            bio=request.POST ['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        
        if request.FILES.get('profileimg')!=None:
            print("\n\n\n gettin")
            image=request.FILES.get('profileimg')
            bio=request.POST ['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')
        
        
        
        
    return render(request,'setting.html',{'user_profile': user_profile})