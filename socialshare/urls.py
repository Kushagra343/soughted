from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
       (r'^app$','socialshare.views.app_verification'),
       (r'^start/','socialshare.views.user_token'),
       (r'^g/','socialshare.views.google_login'),
       (r'^g1/','socialshare.views.google_authenticate'),	
       )
	
	
