from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from sports.models import Team, Squad, League, Matchup
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta, timezone


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        leagues = League.objects.all()
        context['now'] = datetime.now
        context['time_a'] = datetime(2018, 9, 16, 0, 0)
        context['time'] = datetime(2012, 9, 16, 0, 0)
        context['leagues'] = leagues
        return context

class LeagueCreateView(CreateView):
    model = League
    success_url = "/"
    fields = ("name","limit")
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
        context = super().get_context_data(**kwargs)
        baseball = Team.objects.filter(sport="b")
        football = Team.objects.filter(sport="f")
        basketball = Team.objects.filter(sport="k")
        squads = Squad.objects.filter(league=self.kwargs['pk'])
        schedule = Matchup.objects.filter(league=self.kwargs['pk'])
        context['schedule'] = schedule
        context['squads'] = squads
        # context['standings'] = sorted(squads, key=lambda t: -t.total_proj)
        return context

class SquadDetailView(DetailView):
    model = Squad
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        target = Squad.objects.get(id=self.kwargs['pk'])
        baseball = Team.objects.filter(sport="b").exclude(squad__league=target.league)
        football = Team.objects.filter(sport="f").exclude(squad__league=target.league)
        basketball = Team.objects.filter(sport="k").exclude(squad__league=target.league)
        context['checker_b'] = target.checker('b')
        context['checker_f'] = target.checker('f')
        context['checker_k'] = target.checker('k')
        context['baseball'] = baseball.order_by('-pts_proj')
        context['football'] = football.order_by('-pts_proj')
        context['basketball'] = basketball.order_by('-pts_proj')
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
        context['home_score'] = target.home_score_calc
        context['away_score'] = target.away_score_calc

        return context

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
