from django.db import models

from mariontissotphoto.main.models import Photo

class Tag(models.Model):
    name = models.CharField(max_length='50')
    
    def __unicode__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length='50', null=False, blank=False)
    slug = models.CharField(max_length='50', null=False, blank=True)
    date = models.DateTimeField(auto_now=True)
    photos = models.ManyToManyField(Photo)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    description = models.TextField()
    
    def __unicode__(self):
        return self.title
    
    def get_url(self):
        return '/blog/%s' % self.slug
    
    def get_absolute_url(self):
        return self.get_url()
    
    def next(self):
        try:
            next = Blog.objects.filter(id__gt=self.id).order_by('id')[0]
        except IndexError, Blog.DoesNotExist:
            next = None
        return next
    
    def previous(self):
        try:
            next = Blog.objects.filter(id__lt=self.id).order_by('-id')[0]
        except IndexError, Blog.DoesNotExist:
            next = None
        return next
        
    def save(self, force_insert=False,force_update=False):
        from django.template.defaultfilters import slugify
        self.slug = slugify(self.title)
        super(Blog, self).save(force_insert, force_update)
        