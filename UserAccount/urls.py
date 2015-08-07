from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
	url(r'^$', 'UserAccount.views.home', name='home'),
	url(r'^login/', 'UserAccount.views.login', name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
        url(r'^logout/$', 'UserAccount.views.logout', name='logout'),
        url(r'^signup/$', 'UserAccount.views.signup', name='signup'),
	url(r'^activate/(\d{1,25})/$','UserAccount.views.activate',name='activate'),
	url(r'^password_forget/$','UserAccount.views.forget_password'),
   	url(r'^password_forget/(\d{1,5})/$','UserAccount.views.password_reset'),

)
