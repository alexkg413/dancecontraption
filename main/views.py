from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from google.appengine.api import users

from main.models import Dance
from main.forms import DanceForm

def index(request):

    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(dest_url="/")
      logout_url = None
    else:
      login_url = None
      logout_url = users.create_logout_url("/")

    dances = Dance.objects.all() 

    return render_to_response('main/index.html', {'dances':dances,'user':user,
                                                  'login_url':login_url,
						  'logout_url':logout_url})

def dance(request, id):
    dance = Dance.objects.get(pk=id)

    return render_to_response('main/dance.html', {'dance':dance})

def dance_add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DanceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    name = form.cleaned_data['name']
	    dance = Dance(name=name)
	    dance.save()
	return HttpResponseRedirect('/') # Redirect after POST

    return render_to_response('main/dance_add.html', {})
