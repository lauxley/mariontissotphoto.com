from django.contrib import admin

from mariontissotphoto.main.models import Gallery, Photo, Film

class GalleryAdmin(admin.ModelAdmin):
	exclude = ('dir_name', )
	
	class Meta:
		model = Gallery

class PhotoAdmin(admin.ModelAdmin):
	
	# def save_model(self, request, obj, form, change):
		#super(PhotoAdmin, self).save_model(request, obj, form, change)
		# form.save_m2m()
		# obj.save()
	
	class Meta:
		model = Photo
	
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Film)