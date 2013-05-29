from django.conf.urls.defaults import *
from django.conf import settings
#from mariontissotphoto import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.contrib import admin
admin.autodiscover()

from mariontissotphoto.feeds.feeds import blogEntries

feeds = {
    'blog': blogEntries,
}

urlpatterns = patterns('',
	(r'^', include('mariontissotphoto.main.urls')),
    
    (r'^admin/(.*)', admin.site.root),
	#(r'admin', include('admin.urls')),
	
    (r'^blog/?', include('mariontissotphoto.blog.urls')),
    (r'comments', include('django.contrib.comments.urls')),
    
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
	(r'^accounts/login/?$', 'django.contrib.auth.views.login'),
	(r'^accounts/logout/?$', 'django.contrib.auth.views.logout'),

	#A MODIFIER EN PROD !!
	(r'^static/(?P<path>.*)$',
        'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT },
    ),
)
