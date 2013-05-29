import os
from PIL import Image

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Gallery(models.Model):
	name = models.CharField(max_length=30, unique=True)
	dir_name = models.CharField(max_length=30)

	private = models.BooleanField()
	allowed = models.ManyToManyField(User)
	#parent = models.ForeignKey('Gallery', blank=True, null=True)
	
	def __unicode__(self):
		return self.dir_name
	
	# def _rec_path(self):
		# if self.parent:
			# return os.path.join(self.parent._rec_path(), self.dir_name)
		# else:
			# return self.dir_name

	def get_gpath(self):
		return os.path.join(settings.MEDIA_ROOT, 'photo', self.dir_name)

	# def _rec_url(self):
		# if self.parent:
			# return '%s/%s' % (self.parent._rec_url(), self.dir_name)
		# else:
			# return self.dir_name
	def get_absolute_url(self):
		return '/gallery/%s' % self.dir_name
	
	def get_url(self):
		return '/static/photo/%s' % self.dir_name
	
	def save(self, force_insert=None, force_update=None):
		from mariontissotphoto.utils import slugydir
		self.dir_name = slugydir(self.name)
		super(Gallery, self).save(force_insert=force_insert, force_update=force_update)
		# if not os.access(self.get_gpath(), os.W_OK):
			# os.mkdir(self.get_gpath())

# def get_upload_path(instance, filename):
	# from mariontissotphoto.utils import slugyfile
	# return os.path.join(instance.get_path(), slugyfile(filename))

class Film(models.Model):
    file = models.FileField(upload_to = 'film')
    thumbnail = models.ImageField(upload_to = 'thumbnails', help_text='80 de largeur max !')
    description = models.CharField(max_length=500, null=True, blank=True)
    gallery = models.ManyToManyField(Gallery)
    
    def __unicode__(self):
        return self.file.name
        
    def get_path(self):	
        #return self.gallery.get_gpath()
        return os.path.join(settings.MEDIA_ROOT, 'film')

    def get_thumb(self):
        return '/static/%s' %  self.thumbnail
        
    def get_url(self):
        return '/static/%s' % self.file
    
class Photo(models.Model):
	file = models.ImageField(upload_to = 'photo', help_text='720x600 max !')
	thumbnail = models.ImageField(upload_to = 'thumbnails', help_text='80 de largeur max !', null=True, blank=True)
	description = models.CharField(max_length=500, null=True, blank=True)
	gallery = models.ManyToManyField(Gallery)
	chosen = models.BooleanField(default=False, help_text='apparait dans l\'accueil')  #apparait dans l'accueil
	
	def __unicode__(self):
		return self.file.name
		
	def get_path(self):	
		#return self.gallery.get_gpath()
		return os.path.join(settings.MEDIA_ROOT, 'photo')
	
	def get_thumb(self):
		return '/static/%s' %  self.thumbnail
		
	def get_big(self):
		url, f = self.get_url().rsplit('/', 1)
		return '%s/bigs/%s' % (url, f)
		
	def get_upload_path(self):
		#gpath = self.gallery.get_gpath()
		return os.path.join(settings.MEDIA_ROOT, 'photo', str(self.file)) #, self.gallery.get_gpath(), str(self.file))
		
	def get_url(self):
		#return '%s/%s' % (self.gallery.get_url(), self.file)
		return '/static/%s' % self.file
	
	def get_gallery(self):
		return self.gallery.filter(private=False)[0]

