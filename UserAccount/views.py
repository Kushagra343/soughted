from django.contrib.auth.decorators import login_required
import json
import random
import hashlib
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth 
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import UserModel

def is_username_exist(username):
    if User.objects.filter(username=username).count():
        return True
    return False

 
def signup(request):
    if request.method == "GET":
        return render(request,'UserAccount/register.html')
    elif request.method == "POST":
	if UserModel.objects.filter(model_username=request.POST.get('username')).count():
		UserModel.objects.get(model_username=request.POST.get('username')).delete()	
        if not(is_username_exist(request.POST.get('username'))):
	    activation_key = str(random.randint(10000,99999))
            obj=UserModel(model_username=request.POST.get('username',''),model_password=request.POST.get('password',''),model_activation_key=activation_key)
	    obj.save()
	    send_mail('Verificationmail','Please use this link to activate your account:http://127.0.0.1:8000/user/activate/%s'% activation_key,'kushagra343@gmail.com',[request.POST.get('username','')],fail_silently=False)
	    messages.add_message(request, messages.INFO, 'Form Submitted. Please check your e-mail for verfication mail')			
            return HttpResponseRedirect(reverse('user:login'))
        else:
	    messages.add_message(request, messages.INFO, 'User Already exists. Please use different UserName')
            return HttpResponseRedirect(reverse('user:signup'))
 

def activate(request,offset):
  if UserModel.objects.filter(model_activation_key=offset).count()==0:
	return HttpResponseRedirect(reverse('user:home'))
  obj=UserModel.objects.get(model_activation_key=offset)	
  if User.objects.filter(username=obj.model_username).count()==0:
    user = User.objects.create_user(username = obj.model_username, password = obj.model_password)
    user.save()
    messages.add_message(request, messages.INFO, 'Account created Please Login')
  return HttpResponseRedirect(reverse('user:login'))



def login(request):
    if request.user.is_authenticated():
     return HttpResponseRedirect(reverse('user:home')) 
    elif request.method == "GET":
        return render(request,'UserAccount/login.html')
    elif request.method=="POST":
        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('user:home'))
        else:
            messages.add_message(request, messages.INFO, 'Username or Password is incorrect')
            return HttpResponseRedirect(reverse('user:login'))

def logout(request):
  auth.logout(request)
  return render(request,'UserAccount/login.html')



def forget_password(request):
 if request.method=='POST': 
  user_name = request.POST.get('username', False)
  if UserModel.objects.filter(model_username=user_name).count():
    obj=UserModel.objects.get(model_username=user_name)
    obj.model_activation_key=str(random.randint(10000,99999)) 
    obj.save()			
    send_mail('Password Reset Link','Please use this link to reset your password:http://127.0.0.1:8000/user/password_forget/%s'% obj.model_activation_key,'kushagra343@gmail.com',[user_name],fail_silently=False)
    messages.add_message(request, messages.INFO, 'Please Check your Email for Password Reset Link')
    return HttpResponseRedirect(reverse('user:login'))
  else:
   messages.add_message(request, messages.INFO, 'The username you entered does not exist.')
   return render(request,'UserAccount/password_forget.html')
 else: 
  return render(request,'UserAccount/password_forget.html') 

def password_reset(request,offset):
 if request.method=='POST':
  obj=UserModel.objects.get(model_activation_key=offset)
  user = User.objects.get(username=obj.model_username)
  user.set_password(request.POST.get('password1',''))
  user.save()
  messages.add_message(request, messages.INFO, 'Please Use your new password to login')	
  return HttpResponseRedirect(reverse('user:login'))
 else:
  return render(request,'UserAccount/password_reset.html')
@login_required(login_url='/user/login/')
def home(request):
 return render(request,'UserAccount/home.html')
