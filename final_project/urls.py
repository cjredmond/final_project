from django.conf.urls import url, include
from django.contrib import admin
from sports.views import UserCreateView, IndexView, LeagueCreateView, LeagueUpdateView, \
                         LeagueDetailView, SquadDetailView, TeamUpdateView, MatchupDetailView, \
                         SquadUpdateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^league/(?P<pk>\d+)/start/$', LeagueUpdateView.as_view(), name="league_update_view"),
    url(r'^league/create/$', LeagueCreateView.as_view(), name="league_create_view"),
    url(r'^league/(?P<pk>\d+)/home/$', LeagueDetailView.as_view(), name='league_detail_view'),
    url(r'^squad/(?P<pk>\d+)/$', SquadDetailView.as_view(), name="squad_detail_view"),
    #url(r'^team/(?P<pk>\d+)/update/$', TeamUpdateView.as_view(), name='team_update_view'),
    url(r'^matchup/(?P<pk>\d+)/$', MatchupDetailView.as_view(), name='matchup_detail_view'),
    url(r'^roster/(?P<pk>\d+)/update/$', SquadUpdateView.as_view(), name='squad_update_view'),

]
