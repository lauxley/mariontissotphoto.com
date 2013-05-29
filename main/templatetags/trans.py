from django import template
import re
register = template.Library()
from mariontissotphoto.utils import trans


def do_trans(parser, token):
	try:
		tag_name, val = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
	template_trans(val)
register.tag('trans', do_trans)
	
class template_trans(template.Node):
	def __init__(self, val):
		self.val = val
		
	def render(self, context):
		return trans(request,str(self.val))
