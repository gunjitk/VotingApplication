from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.views.generic import RedirectView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'login/index.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            request.session.set_expiry(86400)
            login(request, user)
            return HttpResponseRedirect('/team/members/' + str(user.id))
        else:
            return render(request, 'login/index.html')
