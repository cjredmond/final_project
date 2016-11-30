from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from sports.models import Team, Squad, League, Matchup, Score, Draft, Clock
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta, timezone
from sports.forms import LeagueForm
from sports.scraper import nba_scores, usable_data, fix_names
from sports.nfl_scraper import nfl_scores, nfl_usable_data
from sports.nhl_scraper import nhl_scores, nhl_usable_data
from sports.soccer_api import soccer, soccer_scorer
from sports.tasks import cal
from django.utils import timezone

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class IndexView(TemplateView):
    template_name = "index.html"
    # soccer = soccer_scorer(soccer())

    # for dictionary in soccer:
    #     x = Team.objects.filter(city=dictionary['winner'])
    #     if x:
    #         winner = Team.objects.get(city=dictionary['winner'])
    #         squads = list(Squad.objects.filter(roster__name=winner.name))
    #         Score.objects.create(team=winner, pts=dictionary['winner_score'],tag=str(dictionary['winner'] + dictionary['loser']), time=timezone.now())
    #         current = Score.objects.get(team=winner, tag=str(dictionary['winner'] + dictionary['loser']))
    #         current.active_squad.add(*squads)
    #         current.save()
    #     y = Team.objects.filter(city=dictionary['loser'])
    #     if y:
    #         loser = Team.objects.get(city=dictionary['loser'])
    #         squads = list(Squad.objects.filter(roster__name=winner.name))
    #         Score.objects.create(team=loser, pts=dictionary['loser_score'], tag=str(dictionary['winner'] + dictionary['loser']), time=timezone.now())
    #         current = Score.objects.get(team=loser, tag=str(dictionary['winner'] + dictionary['loser']))
    #         current.active_squad.add(*squads)
    #         current.save()


    def get_context_data(self):
        context = super().get_context_data()
        leagues = League.objects.all()
        context['leagues'] = leagues
        return context

class LeagueCreateView(CreateView):
    model = League
    success_url = "/"
    form_class = LeagueForm
    def form_valid(self, form):
        instance = form.save(commit=False)
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        instance.start = datetime.strptime(start + ' 00:00:00', '%d %B, %Y %H:%M:%S')
        instance.end = datetime.strptime(end + ' 00:00:00', '%d %B, %Y %H:%M:%S')
        instance.limit = 6
        return super().form_valid(form)


class LeagueUpdateView(UpdateView):
    model = League
    fields = []
    success_url = "/"
    # def get_success_url(self, **kwargs):
    #     target = League.objects.get(id=self.kwargs['pk'])
    #     return ('draft_view', args=str(target.draft.id))
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
        context['teams_ready'] = Team.objects.filter(squad__league=target).count()
        context['current_games'] = current_games
        context['amount'] = squads.count()
        context['schedule'] = schedule
        context['squads'] = squads
        context['duration'] = target.duration()
        context['standings'] = sorted(squads, key=lambda t: -t.wins())
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
        # context['football'] = sorted(football, key=lambda t: -t.total_points())
        # context['basketball'] = sorted(basketball, key=lambda t: -t.total_points())
        # context['hockey'] = sorted(hockey, key=lambda t: -t.total_points())
        # context['soccer'] = sorted(soccer, key=lambda t: -t.total_points())
        context['football'] = football
        context['basketball'] = basketball
        context['hockey'] = hockey
        context['soccer'] = soccer
        context['day'] = datetime.now().weekday
        context['wins'] = target.wins()
        context['losses'] = target.losses()
        return context

class MatchupDetailView(DetailView):
    model = Matchup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Matchup.objects.get(id=self.kwargs['pk'])
        context['test'] = target.get_home_info()
        context['home_score'] = target.get_home_score
        context['away_score'] = round(target.get_away_score(),3)
        context['home_squad_teams'] = target.get_home_info()[0]
        context['home_squad_scores'] = target.get_home_info()[1]
        context['home_squad_sports'] = target.get_home_info()[2]
        context['away_squad_teams'] = target.get_away_info()[0]
        context['away_squad_scores'] = target.get_away_info()[1]
        context['away_squad_sports'] = target.get_away_info()[2]
        context['home_record'] = target.home.wins()
        context['away_record'] = target.away.wins()
        current = target.week
        if Matchup.objects.filter(week=current+1, home=self.request.user.squad):
            context['next_week'] = Matchup.objects.get(week=current+1, home=self.request.user.squad)
        if Matchup.objects.filter(week=current+1, away=self.request.user.squad):
            context['next_week'] = Matchup.objects.get(week=current+1, away=self.request.user.squad)
        if Matchup.objects.filter(week=current-1, home=self.request.user.squad):
            context['last_week'] = Matchup.objects.get(week=current-1, home=self.request.user.squad)
        if Matchup.objects.filter(week=current-1, away=self.request.user.squad):
            context['last_week'] = Matchup.objects.get(week=current-1, away=self.request.user.squad)


        return context

class SquadCreateView(CreateView):
    model = Squad
    success_url = "/"
    fields = ('name', 'logo')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

class SquadUpdateView(UpdateView):
    model = Squad
    fields = []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Team.objects.get(id=self.kwargs['sk'])
        context['target'] = target
        return context
    def get_success_url(self, **kwargs):
        target = Squad.objects.get(id=self.kwargs['pk'])
        return reverse('squad_detail_view', args=(str(target.id),))
    def form_valid(self, form, **kwargs):
        target = Team.objects.get(id=self.kwargs['sk'])
        instance = form.save(commit=False)
        instance.roster.add(target)
        return super().form_valid(form)

class SquadDraftView(UpdateView):
    model = Squad
    fields = []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Team.objects.get(id=self.kwargs['sk'])
        context['target'] = target
        return context
    def get_success_url(self, **kwargs):
        target = Squad.objects.get(id=self.kwargs['pk'])
        return reverse('draft_view', args=str(target.league.draft.id))
    def form_valid(self, form, **kwargs):
        target = Team.objects.get(id=self.kwargs['sk'])
        instance = form.save(commit=False)
        instance.roster.add(target)
        clock = Clock.objects.get(id=1)
        clock.time=60
        clock.save()
        return super().form_valid(form)

class SquadDropView(UpdateView):
    model = Squad
    fields = []
    success_url = "/"
    def get_success_url(self, **kwargs):
        target = Squad.objects.get(id=self.kwargs['pk'])
        return reverse('draft_view', args=str(target.league.draft.id))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Team.objects.get(id=self.kwargs['sk'])
        context['target'] = target
        return context
    def form_valid(self, form, **kwargs):
        target = Team.objects.get(id=self.kwargs['sk'])
        instance = form.save(commit=False)
        instance.roster.remove(target)
        return super().form_valid(form)

class DraftView(DetailView):
    model = Draft
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = Draft.objects.get(id=self.kwargs['pk'])
        squads = target.league.squad_set.all()
        dt = timedelta(seconds=10)
        start = target.start
        clock = Clock.objects.get(id=1)
        soccer = Team.objects.filter(sport="s").exclude(squad__league=target.league)
        hockey = Team.objects.filter(sport="h").exclude(squad__league=target.league)
        football = Team.objects.filter(sport="f").exclude(squad__league=target.league)
        basketball = Team.objects.filter(sport="k").exclude(squad__league=target.league)
        context['football'] = sorted(football, key=lambda t: -t.total_points())[:20]
        context['basketball'] = sorted(basketball, key=lambda t: -t.total_points())[:20]
        context['hockey'] = sorted(hockey, key=lambda t: -t.ppg())[:20]
        context['soccer'] = sorted(soccer, key=lambda t: -t.total_points())[:20]
        counter = Team.objects.filter(squad__league=target.league).count()
        context['checker_s'] = self.request.user.squad.checker('s')
        context['checker_h'] = self.request.user.squad.checker('h')
        context['checker_f'] = self.request.user.squad.checker('f')
        context['checker_k'] = self.request.user.squad.checker('k')
        context['counter'] = counter
        context['pick'] = counter + 1
        context['active'] = target.whos_pick(counter+1)
        context['next'] = target.whos_pick(counter+2)
        context['third'] = target.whos_pick(counter+3)
        context['fourth'] = target.whos_pick(counter+4)
        context['fifth'] = target.whos_pick(counter+5)
        context['sixth'] = target.whos_pick(counter+6)
        context['clock'] = clock
        if clock.time == 0:
            squad = target.whos_pick(counter+1)
            if squad.checker('h'):
                squad.roster.add(sorted(hockey, key=lambda t: -t.ppg())[0])
                squad.save()
            elif squad.checker('k'):
                squad.roster.add(sorted(basketball, key=lambda t: -t.total_points())[0])
                squad.save()
            else:
                squad.roster.add(football[0])
                squad.save()
            clock.time = 60
            clock.save()
        return context

class SquadJoinView(UpdateView):
    model = Squad
    fields = []
    def get_success_url(self, **kwargs):
        target = League.objects.get(id=self.kwargs['sk'])
        return reverse('league_detail_view', args=str(target.id))
    def form_valid(self, form, **kwargs):
        instance = form.save(commit=False)
        squad = Squad.objects.get(id=self.kwargs['pk'])
        league = League.objects.get(id=self.kwargs['sk'])
        instance.league = league
        return super().form_valid(form)

class RulesView(TemplateView):
    template_name = 'rules.html'
