import os, settings, string

def unic(str):
	from django.utils.encoding import smart_unicode
	return smart_unicode(str, encoding='latin1')

def slugyfile(str): #slugify a filename
	from django.template.defaultfilters import slugify
	return "%s.%s" % (slugify(unic(str).rsplit('.', 1)[0]), unic(str).rsplit('.', 1)[1])
	
def slugydir(str):
	from django.template.defaultfilters import slugify
	return slugify(unic(str))
	
def upload_file(ufile, dpath, max_size=None, allowed_ext=None, use_chunks=False):	#uploaded file, destination path
	if max_size:
		if ufile.size > max_size:
			return False, "La taille du fichier est trop importante !"
	if allowed_ext:
		if ufile.name.rsplit('.', 1)[1].lower() not in map(string.lower, allowed_ext):
			return False, "Le fichier dois etre de l'un de ces types : %s" % str(allowed_ext)
	tpath, filename = os.path.split(dpath)
	if not os.access(tpath, os.F_OK):
		#on tente de creer le dossier:
		os.makedirs(tpath, 0775)
		if not os.access(tpath, os.F_OK):
			return False, "le dossier de destination n'existe pas ou n'est pas inscriptible."
	try:
		destination = open(dpath, 'wb')
		if use_chunks:
			for chunk in ufile.chunks():
				destination.write(chunk)
		else:
			destination.write(ufile.read())
	except:
		return False, "Impossible d'envoyer le fichier !"
	destination.close()
	return True, ''

def rtr(request, templ, dict = {}, mimetype=''):
	from django.shortcuts import render_to_response
	from django.template import RequestContext
	return render_to_response(templ, dict, context_instance=RequestContext(request), mimetype=mimetype)
	
def get_lang(request):
	l = request.session.get('django_language')
	if not l: l = 'fr'
	return l
	
def trans(request, text):
	import re
	if not re.match('(<[fr|eng]([^>]*)>){2}', text):
		return text
	else:
		try: f = text.find('<'+get_lang())
		except ValueError: return text
		f2=text.find('>', f)
		return text[f+1+len(get_lang(request)), f2-1]
		
		
#si en mode debug forward le mail aux admins
def my_send_mail(email, txt):
	from django.core.mail import send_mail
	
	subject = 'Contact mariontissotphoto.com : %s' % email
	
	if settings.DEBUG:
		_to = ['robin@revolunet.com']
	else:
		_to = ['marion@mariontissotphoto.com']
		
	send_mail(subject, txt, email, _to)
	
    

