from django.contrib import admin

from mariontissotphoto.blog.models import Blog, Tag

class BlogAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Blog,  BlogAdmin)
admin.site.register(Tag)