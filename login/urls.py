from django.conf.urls import url


from .views import LoginView

## urlpatterns <<--- dedicated name
urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
]