"""votr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import RedirectView

from teams import urls as team_urls
from sprints import urls as sprint_urls
from voting import urls as voting_urls
from activity import urls as activity_urls
from login import urls as login_urls

from .views import app_view

from .adminForms import AuthenticationForm

admin.autodiscover()
admin.site.login_form = AuthenticationForm

urlpatterns = [
    url(r'^app$', app_view),
    url(r'^$', RedirectView.as_view(url='/polls')),
    url(r'^team/', include(team_urls)),
    url(r'^sprint/', include(sprint_urls)),
    url(r'^booth/', include(voting_urls)),
    url(r'^activity/',include(activity_urls)),
    url(r'^login/', include(login_urls)),

    url(r'^polls/', admin.site.urls)
]

admin.site.site_header = 'Sprint Pollings'