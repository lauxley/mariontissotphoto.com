from django.contrib.syndication.feeds import Feed
from mariontissotphoto.blog.models import Blog

class blogEntries(Feed):
    title = "Photo blog de Marion Tissot"
    link = "/blog"
    description = "Photo blog de Marion tissot."

    def items(self):
        return Blog.objects.order_by('-date')[:10]