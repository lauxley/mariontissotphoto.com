# Create your views here.
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from mariontissotphoto.main.models import Gallery, Photo
from mariontissotphoto.utils import rtr

class AdminFormGallery(forms.Form):
	name = forms.CharField()
	#name_eng = forms.CharField()
	parent = forms.ModelChoiceField(Gallery.objects.filter(parent__isnull=True), required=False)
	
class AdminFormPhoto(forms.Form):
	file = forms.ImageField()
	description = forms.CharField(max_length=500)
	#description_eng = forms.CharField(max_length=500)
	parent = forms.ModelChoiceField(Gallery.objects.filter(parent__isnull=False))
	
def admin(request):
	from mariontissotphoto.utils import upload_file, slugyfile
	if request.method == 'POST':
		rp = request.POST
		rf = request.FILES
		if 'newgallery' in rp:
			try: pg = Gallery.objects.get(pk=int(rp['parent']))
			except (Gallery.DoesNotExist,ValueError): pg = None
			g = Gallery(
				name = rp['name'],
				parent = pg
			)
			g.save()
		elif 'newphoto' in rp:
			try: pg = Gallery.objects.get(pk=int(rp['parent']))
			except (Gallery.DoesNotExist,ValueError): pg = None
			p = Photo( 
				description = rp['description'],
				gallery = pg
				)
			
			p.file = slugyfile(rf['file'])
			p.save()
			
			#creation du thumbnail
			from PIL import Image
			import os
			try: fname = slugyfile(rf['file'].name.split('/')[-1])
			except IndexError: fname = slugyfile(rp['file'].name)
			
			img = Image.open(rf['file']).convert('RGB')
			if not os.access(p.get_path(), os.W_OK):
				os.makedirs(p.get_path())
			img.save(p.get_upload_path())
			
			size=(100, 100)
			img = Image.open(p.get_upload_path()).convert('RGB')
			img.thumbnail(size, Image.ANTIALIAS)
			path = os.path.join(p.get_path(), 'thumbnails')
			if not os.access(path, os.W_OK):
				os.makedirs(path)
			ipath = os.path.join(path,fname)
			img.save(ipath)
			
			size =(400,400)
			img = Image.open(p.get_upload_path()).convert('RGB')
			img.thumbnail(size, Image.ANTIALIAS)
			path = os.path.join(p.get_path(), 'bigs')
			if not os.access(path, os.W_OK):
				os.makedirs(path)
			ipath = os.path.join(path,fname)
			img.save(ipath)

	formgallery = AdminFormGallery()
	formphoto = AdminFormPhoto()
	
	tree = []
	rootg = Gallery.objects.filter(parent=None)
	for gal in rootg:
		gal.childs = Gallery.objects.filter(parent=gal)
		for child in gal.childs:
			child.photos = Photo.objects.filter(gallery=child)
		gal.photos = Photo.objects.filter(gallery=gal)
		tree.append(gal)

	return rtr(request, 'admin/admin.html', {'gallery' : tree, 'formgallery' : formgallery, 'formphoto' : formphoto})
	
def del_gallery(request, gal_id):
	return HttpResponseRedirect('/admin')
	
def del_photo(request, gal_id):
	return HttpResponseRedirect('/admin')