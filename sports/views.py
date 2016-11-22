from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from sports.models import Team, Squad, League, Matchup, Score
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta, timezone
from sports.forms import LeagueForm
from sports.scraper import nba_scores, usable_data, fix_names
from sports.nfl_scraper import nfl_scores, nfl_usable_data
from sports.nhl_scraper import nhl_scores, nhl_usable_data
from sports.tasks import cal
from django.utils import timezone

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        Celtics = Team.objects.get(name='Celtics')
        x = Squad.objects.filter(roster__name='Celtics')
        x = list(x)
        Score.objects.create(team=Celtics, pts=5, time=timezone.now(), tag='http://www.google.com')
        y = Score.objects.get(tag='http://www.google.com')
        y.active_squad.add(*x)

        # cal.delay()
        # items = nhl_usable_data(fix_names(nhl_scores()))
        # for dictionary in items:
            # if dictionary['winner'] == 'NY Giants':
            #     winner = Team.objects.get(name='Giants', sport='f')
            #     loser = Team.objects.get(city=dictionary['loser'], sport='f')
            # elif dictionary['loser'] == 'NY Giants':
            #     winner = Team.objects.get(city=dictionary['winner'], sport='f')
            #     loser = Team.objects.get(name='Giants', sport='f')
            # else:
            # if dictionary['winner'] == 'LA':
            #     winner = Team.objects.get(name='Clippers', sport='k')
            #     loser = Team.objects.get(city=dictionary['loser'], sport='k')
            # elif dictionary['loser'] == 'LA':
            #     winner = Team.objects.get(city=dictionary['winner'], sport='k')
            #     loser = Team.objects.get(name='Clippers', sport='k')
            # elif dictionary['winner'] == 'LA Lakers':
            #     winner = Team.objects.get(name='Lakers')
            #     loser = Team.objects.get(city=dictionary['loser'], sport='k')
            # elif dictionary['loser'] == 'LA Lakers':
            #     winner = Team.objects.get(city=dictionary['winner'], sport='k')
            #     loser = Team.objects.get(name='Lakers')
            # else:
            #     winner = Team.objects.get(city=dictionary['winner'], sport='k')
            #     loser = Team.objects.get(city=dictionary['loser'], sport='k')
            # winner = Team.objects.get(city=dictionary['winner'], sport='h')
            # loser = Team.objects.get(city=dictionary['loser'], sport='h')
            # Score.objects.filter(tag=dictionary['tag']).delete()
            # Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=datetime.now())
            # Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=datetime.now())
        leagues = League.objects.all()
        context['leagues'] = leagues
        return context

class LeagueCreateView(CreateView):
    model = League
    success_url = "/"
    form_class = LeagueForm
    def form_valid(self, form):
        instance = form.save(commit=False)
        return super().form_valid(form)

class LeagueUpdateView(UpdateView):
    model = League
    success_url = "/"
    fields = []
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.live = True
        squads = instance.get_squads
        count = 1
        for squad in squads:
            squad.sched_id = count
            count += 1
            squad.save()
        instance.schedule(squads)
        return super().form_valid(form)

class LeagueDetailView(DetailView):
    model = League
    def get_context_data(self,**kwargs):
        target = League.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        football = Team.objects.filter(sport="f")
        basketball = Team.objects.filter(sport="k")
        squads = Squad.objects.filter(league=self.kwargs['pk'])
        schedule = Matchup.objects.filter(league=self.kwargs['pk'])
        current_games = []
        for game in schedule:
            if game.tues_start < datetime.now(timezone.utc) and game.tues_end > datetime.now(timezone.utc):
                current_games.append(game)
        context['current_games'] = current_games
        context['amount'] = squads.count()
        context['schedule'] = schedule
        context['squads'] = squads
        context['duration'] = target.duration()
        # context['standings'] = sorted(squads, key=lambda t: -t.total_proj)
        return context

class SquadDetailView(DetailView):
    model = Squad
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        target = Squad.objects.get(id=self.kwargs['pk'])
        soccer = Team.objects.filter(sport="s").exclude(squad__league=target.league)
        hockey = Team.objects.filter(sport="h").exclude(squad__league=target.league)
        football = Team.objects.filter(sport="f").exclude(squad__league=target.league)
        basketball = Team.objects.filter(sport="k").exclude(squad__league=target.league)
        context['checker_s'] = target.checker('s')
        context['checker_h'] = target.checker('h')
        context['checker_f'] = target.checker('f')
        context['checker_k'] = target.checker('k')
        context['football'] = football.order_by('-pts_proj')
        context['basketball'] = basketball.order_by('-pts_proj')
        context['hockey'] = hockey.order_by('-pts_proj')
        context['soccer'] = soccer.order_by('-pts_proj')
        context['day'] = datetime.now().weekday
        context['record'] = target.wins()
        return context

class TeamUpdateView(UpdateView):
    model = Team
    fields = []
    def get_success_url(self, **kwargs):
        return "/"
        #return reverse_lazy('squad_detail_view', args=str(self.request.user.squad.id))
    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.squad == self.request.user.squad:
            instance.squad = None
        else:
            instance.squad = self.request.user.squad
        return super().form_valid(form)

class MatchupDetailView(DetailView):
    model = Matchup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Matchup.objects.get(id=self.kwargs['pk'])
        context['home_score'] = round(target.get_squad_score()[0],2)
        context['away_score'] = round(target.get_squad_score()[1],2)
        context['home_squad_teams'] = target.each_team_score()[0][0]
        context['home_squad_scores'] = target.each_team_score()[0][1]
        context['home_squad_sports'] = target.each_team_score()[0][2]
        context['away_squad_teams'] = target.each_team_score()[1][0]
        context['away_squad_scores'] = target.each_team_score()[1][1]
        context['away_squad_sports'] = target.each_team_score()[1][2]
        context['home_record'] = target.home.wins()
        context['away_record'] = target.away.wins()


        return context

class SquadCreateView(CreateView):
    model = Squad
    success_url = "/"
    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        instance.league = League.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

class SquadUpdateView(UpdateView):
    model = Squad
    fields = []
    success_url = "/"
    def form_valid(self, form, **kwargs):
        target = Team.objects.get(id=self.kwargs['sk'])
        instance = form.save(commit=False)
        instance.roster.add(target)
        return super().form_valid(form)

class SquadDropView(UpdateView):
    model = Squad
    fields = []
    success_url = "/"
    def form_valid(self, form, **kwargs):
        target = Team.objects.get(id=self.kwargs['sk'])
        instance = form.save(commit=False)
        instance.roster.remove(target)
        return super().form_valid(form)
