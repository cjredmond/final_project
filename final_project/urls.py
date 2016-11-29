from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from sports.views import UserCreateView, IndexView, LeagueCreateView, LeagueUpdateView, \
                         LeagueDetailView, SquadDetailView, MatchupDetailView, \
                         SquadUpdateView, SquadDropView, SquadCreateView, DraftView, \
                         SquadDraftView, SquadJoinView
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^create_user/$', UserCreateView.as_view(), name="user_create_view"),
    url(r'^$', IndexView.as_view(), name="index_view"),
    url(r'^league/(?P<pk>\d+)/start/$', LeagueUpdateView.as_view(), name="league_update_view"),
    url(r'^league/create/$', LeagueCreateView.as_view(), name="league_create_view"),
    url(r'^league/(?P<pk>\d+)/home/$', LeagueDetailView.as_view(), name='league_detail_view'),
    url(r'^squad/(?P<pk>\d+)/$', SquadDetailView.as_view(), name="squad_detail_view"),
    url(r'^matchup/(?P<pk>\d+)/$', MatchupDetailView.as_view(), name='matchup_detail_view'),
    url(r'^roster/(?P<pk>\d+)/add/(?P<sk>\d+)/$', SquadUpdateView.as_view(), name='squad_update_view'),
    url(r'^roster/(?P<pk>\d+)/draft/(?P<sk>\d+)/$', SquadDraftView.as_view(), name='squad_draft_view'),
    url(r'^roster/(?P<pk>\d+)/drop/(?P<sk>\d+)/$', SquadDropView.as_view(), name='squad_drop_view'),
    #url(r'^squad/(?P<pk>\d+)/create/$', SquadCreateView.as_view(), name='squad_create_view'),
    url(r'^squad/create/$', SquadCreateView.as_view(), name='squad_create_view'),
    url(r'^draft/(?P<pk>\d+)/$', DraftView.as_view(), name='draft_view'),
    url(r'^league/(?P<pk>\d+)/join/(?P<sk>\d+)/$', SquadJoinView.as_view(), name='league_join_view'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
