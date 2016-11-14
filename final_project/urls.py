from django.conf.urls import url, include
from django.contrib import admin
from sports.views import UserCreateView, IndexView, LeagueCreateView, LeagueUpdateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^league/(?P<pk>\d+)/start/$', LeagueUpdateView.as_view(), name="league_update_view"),
    url(r'^league/create/$', LeagueCreateView.as_view(), name="league_create_view"),
]
