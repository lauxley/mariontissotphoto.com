import zipfile
import os.path
from PIL import Image

from django.conf import settings
from django.http import Http404, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from mariontissotphoto.utils import rtr,my_send_mail
from mariontissotphoto.main.models import Gallery, Photo, Film

# Create your views here.

def accueil(request, lang=None):
    #if lang: request.session['django_language'] = lang
    #si la langue a pas été choisie, on passe par la 1ere page
    #if 'django_language' in request.session:
    
    photos = Photo.objects.filter(chosen=True).order_by("-id")[:3]
    return rtr(request, 'main/accueil.html', {'photos':photos})
    #else:
    #	return rtr(request, 'main/langchoice.html')

def gallery(request, gal=None):
    try: _gallery = Gallery.objects.get(dir_name = gal)
    except Gallery.DoesNotExist: _gallery = Gallery.objects.all().order_by('id')[0]
    galleries = Gallery.objects.filter(private=False).order_by('id')
    photos = Photo.objects.filter(gallery=_gallery).order_by('id')
    films = Film.objects.filter(gallery=_gallery).order_by('id')
    if not _gallery in galleries:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login?next=%s' % _gallery.get_absolute_url())
        if not request.user.id in _gallery.allowed.filter().values_list('id', flat=True) and not request.user.is_superuser:
            return HttpResponseRedirect('/')
    try:
        first = photos[0]
    except IndexError:
        first = None
    
    return rtr(request, 'main/gallery.html', {'gallery' : _gallery, 'galleries' : galleries, 'photos' : photos, 'films' : films, 'first' : first})

# def photoView(request, photo):
    # if 'HTTP_REFERER' not in request.META or request.META['HTTP_REFERER'] == '':
        # return HttpResponse('ou pas.')
    # else:            
        # try:
            # p = open(os.path.join(settings.MEDIA_ROOT, 'photo', photo), 'rb')
        # except IOError:
            # raise Http404
        # else:
            # image = p.read()
            # p.close()
            
        # return HttpResponse(image, status=200, content_type="image/jpeg")
    
def bio(request):
	return rtr(request, 'main/bio.html')
	
from django import forms
class Contact(forms.Form):
	email = forms.EmailField(label="Votre email", widget=forms.TextInput(attrs={'size':'40'}))
	msg = forms.CharField(label='Message', widget=forms.Textarea())
	
def contact(request):
	
	if request.method=="POST":
		rp = request.POST
		form = Contact(rp)
		if form.is_valid():
			my_send_mail(rp['email'], rp['msg'])
			return HttpResponseRedirect('/sucessmail')
	
	form = Contact()
	
	return rtr(request, 'main/contact.html', {'form' : form} )
	
def successmail(request):
	return rtr(request, 'main/sucessmail.html')
    
class UploadZipForm(forms.Form):
    file = forms.FileField()
    gallery = forms.ChoiceField(choices=[(g.id, g.name) for g in Gallery.objects.all()])

def uploadzip(request):
    if not request.user.is_superuser:
        raise Http404
    if request.method == "POST":
    
        zfobj = zipfile.ZipFile(request.FILES['file'])
        
        for name in zfobj.namelist():
            dirpath = os.path.join(settings.MEDIA_ROOT, 'photo')
            imgpath = os.path.join(dirpath, name)
            
            try:
                outfile = open(imgpath, 'wb')
            except IOError:
                pass
            else:
                outfile.write(zfobj.read(name))
                outfile.close()
                
                img = Image.open(imgpath)
                size=(80, 80)
                img.thumbnail(size, Image.ANTIALIAS)
                img.save(os.path.join(settings.MEDIA_ROOT, 'thumbnails', name))
                #img.close()
                
                gal = Gallery.objects.get(pk=request.POST['gallery'])
                
                p = Photo(file='photo/%s' % name, thumbnail='thumbnails/%s' % name)
                p.save()
                p.gallery.add(gal)
            
        form = UploadZipForm(request.POST, request.FILES)
    else:
        form = UploadZipForm()
    
    return rtr(request, 'main/uploadzip.html', {'form' : form})
