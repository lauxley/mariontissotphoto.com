from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    
    (r'^tag/(?P<tag>.*)$', views.taglist),
    (r'^search$', views.search),
    (r'comments/(?P<blog>.*)', views.comments),
    
    (r'^(?P<post>.*)', views.blog),
    (r'^$', views.blog),
)