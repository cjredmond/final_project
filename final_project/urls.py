from django.conf.urls import url, include
from django.contrib import admin
from sports.views import UserCreateView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
]
