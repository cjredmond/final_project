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

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        items = usable_data(fix_names(nba_scores()))
        if items:
            for dictionary in items:
                print(dictionary)
                winner = Team.objects.get(city=dictionary['winner'], sport='k')
                loser = Team.objects.get(city=dictionary['loser'], sport='k')
                Score.objects.filter(tag=dictionary['tag']).delete()
                Score.objects.create(team=winner, pts=dictionary['winner_pts'],tag=dictionary['tag'], time=datetime.now())
                Score.objects.create(team=loser, pts=dictionary['loser_pts'],tag=dictionary['tag'], time=datetime.now())
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
        context['hocket'] = hockey.order_by('-pts_proj')
        context['soccer'] = soccer.order_by('-pts_proj')
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
        home_teams = target.get_team_score()[0]

        context['home_score'] = target.home.score(target)
        context['away_score'] = target.away.score(target)
        context['home_teams'] = home_teams
        context['away_teams'] = target.get_team_score()[1]

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
