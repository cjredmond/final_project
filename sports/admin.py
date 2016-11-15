from django.contrib import admin

from sports.models import Team, Squad, League, Matchup, PayLeague
admin.site.register(Team)
admin.site.register(Squad)
admin.site.register(League)
admin.site.register(Matchup)
admin.site.register(PayLeague)
