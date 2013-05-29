from django.http import Http404
from django.shortcuts import render_to_response
from django.db.models import Q

from models import Blog, Tag

def blog(request, post=None):
    if not post:
        try: blog = Blog.objects.all().order_by('-id')[0]
        except IndexError: blog = None
    else:
        try: blog = Blog.objects.get(slug=post)
        except Blog.DoesNotExist: blog = None
        
    if blog:
        tagz = blog.tags.all()
        photoz = blog.photos.all()
    else:
        tagz = None
        photoz = None
    
    return render_to_response('blog/blog.html', {'blog':blog, 'tagz' : tagz, 'photoz' : photoz})

def taglist(request, tag):
    try:
        mtag = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        raise Http404
    blogz = mtag.blog_set.all()
    return render_to_response('blog/blogz.html', { 'blogz' : blogz, 'tagz' : Tag.objects.all() })
    
def search(request):
    if request.method=='POST':
        if 'search' in request.POST:
            blogz = Blog.objects.distinct().all()
            mots = request.POST['search'].split(' ')
            for mot in mots:
                if mot != '':
                    blogz = blogz.filter(Q(description__contains=mot) | Q(tags__name=mot) | Q(title__contains=mot))
        else:
            blogz = Blog.objects.all()
    else:
        raise Http404
    return render_to_response('blog/blogz.html', { 'blogz' : blogz, 'tagz' : Tag.objects.all(), 'search' : request.POST['search'] })

def comments(request, blog):
    if blog != '':
        try: blog = Blog.objects.get(slug=blog)
        except Blog.DoesNotExist: 
            raise Http404
    
    return render_to_response('blog/comments.html', {'blog' : blog})