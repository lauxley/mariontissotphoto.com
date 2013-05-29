from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User

class SiteLogin:
    "This middleware requires a login for every view"
    def process_request(self, request):
        #print request.path , request.user.is_anonymous()
        if request.user.is_anonymous():
            #print request.path
            if request.path != '/admin/':
                return HttpResponseRedirect('/admin/?next=%s' % request.path)
            else:
                if request.method == 'POST':
                    username = request.POST['username']
                    password = request.POST['password']
                    # FIXME 
                  #  if username=='demo':
                        #user = User.objects.get(username='demo')
                        #user = authenticate(username='demo', password=user.password)
                        #request.user = user
                   # else:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            #return HttpResponse("logged")
                            return HttpResponseRedirect(request.GET.get('next', '/'))
                            
                            # Redirect to a success page.
                        else:
                            #return HttpResponse("not active")
                            return HttpResponseRedirect('/admin/?next=%s' % request.GET.get('next', ''))
                            # Return a 'disabled account' error message
                    else:
                        # Return an 'invalid login' error message.
                        return HttpResponseRedirect('/admin/?next=%s' % request.GET.get('next', ''))
                else:
                    pass 
                    # return to login template from urls.py
                