from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
import facebook
import urllib
import urllib2
import json
import random

# google app details
google_client_id = '796645511249-tlfgn500o4tglgepp1m82tb41flstn9i.apps.googleusercontent.com'
google_client_secret= 'L-D3hYe5AWwo8SkqvQ8N85if'
google_redirect_uri = "http://localhost:8000/social/g1"
# facebook app details
app_id ='633658320043143'
app_secret = '3d65ab8b848b79c213ab7bcd14862061'
post_login_url = "http://localhost:8000/social/start/"

passw= "I52uUKoM4mZnZnBMPgTI6srdWwv"

#facebook verify app 
def app_verification(request):
 auth_url = ("http://www.facebook.com/dialog/oauth?" +
                               "client_id=" + app_id +
                               "&redirect_uri=" + post_login_url +
                              "&scope=email")
 return redirect(auth_url)

#facebook genrating access token 
def user_token(request):
 data = request.GET.get('code','')
 code_url = ("https://graph.facebook.com/oauth/access_token?" +
                               "client_id=" + app_id +
 			       "&client_secret=" + app_secret +  	
                               "&redirect_uri=" + post_login_url +
                               "&code=" + data)
 usock = urllib2.urlopen(code_url)
 data = usock.read()
 usock.close()
 acs_token = str(data).strip('access_token=')
 length = len(acs_token)-16
 acs_token = acs_token[0:length]
 graph = facebook.GraphAPI(acs_token)
 profile = graph.get_object("me")
 if not(is_username_exist(profile['email'])):
    	user = User.objects.create_user(profile['email'],profile['email'],password = passw)
 user = auth.authenticate(username=profile['email'],password=passw)
 if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('user:home'))
 else:
            return HttpResponseRedirect(reverse('user:login'))
 

def google_login(request):
    token_request_uri = "https://accounts.google.com/o/oauth2/auth"
    response_type = "code"
    client_id = google_client_id
    redirect_uri = google_redirect_uri
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri = token_request_uri,
        response_type = response_type,
        client_id = client_id,
        redirect_uri = redirect_uri,
        scope = scope)
    return HttpResponseRedirect(url)

def google_authenticate(request):
    login_failed_url = '/'
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('{loginfailed}'.format(loginfailed = login_failed_url))

    access_token_uri = 'https://accounts.google.com/o/oauth2/token'
    redirect_uri = google_redirect_uri
    params = urllib.urlencode({
        'code':request.GET['code'],
        'redirect_uri':redirect_uri,
        'client_id':google_client_id,
        'client_secret':google_client_secret,
        'grant_type':'authorization_code'
    })
    url_request = urllib2.Request(access_token_uri,params)
    response = urllib2.urlopen(url_request)
    data = response.read()
    token_data = json.loads(data)
    url = "https://www.googleapis.com/oauth2/v1/userinfo?access_token="+token_data['access_token']
    response = urllib2.urlopen(url).read()
    data = json.loads(response) 
    if not(is_username_exist(data['email'])):
    	user = User.objects.create_user(data['email'],data['email'],password = passw)
    user = auth.authenticate(username=data['email'],password=passw)
    if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('user:home'))
    else:
            return HttpResponseRedirect(reverse('user:login'))
  


#Helper Function

def is_username_exist(username):
    if User.objects.filter(username=username).count():
        return True
    return False


