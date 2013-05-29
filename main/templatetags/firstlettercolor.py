from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def firstlettercolor(val, color="red"):
	return mark_safe('<font id="'+val+'" color="'+color+'">'+val[0]+'</font>'+val[1:])
firstlettercolor.is_safe = True
	


