from django.conf.urls.defaults import *
from mariontissotphoto.main import models
import views

urlpatterns = patterns('',
    (r'^fr$', views.accueil, {'lang' : 'fr'}),
    (r'^eng$', views.accueil, {'lang' : 'eng'}),
    (r'^$', views.accueil),

    (r'^gallery/(?P<gal>.+)/$', views.gallery),
    (r'^gallery$', views.gallery),
    #(r'^photo/(?P<photo>.+)$', views.photoView),

    (r'^bio$', views.bio),
    (r'^contact$', views.contact),

    (r'^uploadzip$', views.uploadzip),

    (r'^sucessmail$', views.successmail),
)