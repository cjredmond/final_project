from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import csv
from datetime import datetime, timedelta
from django.utils import timezone
from operator import itemgetter

class League(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField()
    player = models.ManyToManyField('auth.User')
    live = models.BooleanField(default=False)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.name)

    def duration(self):
        duration = self.end - self.start
        return duration

    def schedule(self,squads):
        ##https://github.com/taddeimania/tfb/tree/master/utility/schedules
        ##-CSV from JoelTaddei
        weeks = self.duration() // timedelta(days=7)
        dt = self.start
        while dt.weekday() != 1:
            dt += timedelta(days=1)

        with open('6teams.csv') as infile:
            reader = csv.reader(infile)
            for i,row in enumerate(reader):
                start_day = dt
                end_day = dt + timedelta(days=7)
                Matchup.objects.create(league=self,week=row[0], home=squads.get(sched_id=row[1]),
                away=squads.get(sched_id=row[2]), tues_start=start_day, tues_end=end_day)
                if i % 3 == 2 or i == 2:
                    dt = dt + timedelta(days=7)
                if i == (weeks*3) - 1:
                    break

    @property
    def get_squads(self):
        return self.squad_set.all()


SPORTS = [('f', 'football'), ('k', 'basketball'), ('h', 'hockey'), ('s', 'soccer')]
class Team(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50,blank=True,null=True)
    logo = models.FileField(null=True,blank=True)
    sport = models.CharField(max_length=1,choices=SPORTS)
    pts_last = models.IntegerField()
    pts_proj = models.IntegerField()

    def __str__(self):
        if self.sport == 's':
            return self.city
        return self.name

    def week_score(self,matchup):
        group = self.get_scores
        total = 0
        for score in group:
            if score.time > matchup.tues_start and score.time < matchup.tues_end:
                total = total + score.pts
        return total

    @property
    def get_scores(self):
        return self.score_set.all()
    def total_points(self):
        return round(sum(score.pts for score in self.get_scores),3)
    def rank(self):
        teams = Team.objects.filter(sport=self.sport)
        ranked = sorted(teams, key=lambda t: -t.total_points())
        ranked = [i for i, x in enumerate(ranked) if x == self]
        ranked = str(ranked).replace("[","").replace("]","")
        return int(ranked) + 1
    def owned_per(self):
        l = League.objects.all().count()
        t = Squad.objects.filter(roster=self).count()
        return t/l * 100
    def ppg(self):
        g = Score.objects.filter(team=self).count()
        t = float(self.total_points())
        if g:
            return round(t/g,2)
        return 0



class Squad(models.Model):
    user = models.OneToOneField('auth.User')
    name = models.CharField(max_length=40)
    league = models.ForeignKey(League)
    sched_id = models.IntegerField(null=True,blank=True)
    roster = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return self.name

    def checker(self, sport):
        teams = self.roster.all()
        count = 0
        for team in teams:
            if team.sport == sport:
                count += 1
        if count > 2:
            return False
        return True

    def score(self, matchup):
        start = matchup.tues_start
        end = matchup.tues_end
        all_scores = []
        current_scores = []
        for team in self.roster.all():
            all_scores.append(team.score_set.all())
        for group in all_scores:
            for score in group:
                if score.time > start and score.time < end:
                    current_scores.append(score)
        result = 0
        for score in current_scores:
            result = result + score.pts
        return round(result,3)

    def wins(self):
        games = Matchup.objects.filter(away=self) | Matchup.objects.filter(home=self)
        wins = 0
        loss = 0
        for game in games:
            if game.win == self:
                wins += 1
            elif not game.win:
                pass
            else:
                loss += 1
        return wins,loss


class Score(models.Model):
    pts = models.FloatField(default=0)
    team = models.ForeignKey(Team)
    time = models.DateTimeField(null=True)#auto_now_add=True
    tag = models.URLField()
    game_time = models.CharField(default='(FINAL)',max_length=50)
    active_squad = models.ManyToManyField(Squad, blank=True)

    def __str__(self):
        return str(self.team) + ' ' + str(self.pts)

    def is_current(self, matchup):
        if self.time > matchup.tues_start and self.time < matchup.tues_end:
            return True
        return False

class Matchup(models.Model):
    league = models.ForeignKey(League)
    week = models.IntegerField()
    home = models.ForeignKey(Squad, related_name='home')
    away = models.ForeignKey(Squad, related_name='away')
    tues_start = models.DateTimeField(null=True)
    tues_end = models.DateTimeField(null=True)

    def __str__(self):
        return (str(self.home) + " vs " + str(self.away))

    def get_home_info(self):
        teams = self.home.roster.all()
        team_names = [team.name for team in teams]
        score_sets = [team.score_set.all() for team in teams]
        team_scores = []
        for team in score_sets:
            total = 0
            for score in team:
                if score.is_current(self) and self.home in list(score.active_squad.all()):
                    total += score.pts
            team_scores.append(round(total,3))
        team_sport = [team.sport for team in teams]
        all_info = [team_names,team_scores,team_sport]
        return all_info

    def get_away_info(self):
        teams = self.away.roster.all()
        team_names = [team.name for team in teams]
        score_sets = [team.score_set.all() for team in teams]
        team_scores = []
        for team in score_sets:
            total = 0
            for score in team:
                if score.is_current(self) and self.away in list(score.active_squad.all()):
                    total += score.pts
            team_scores.append(round(total,3))
        team_sport = [team.sport for team in teams]
        all_info = [team_names,team_scores,team_sport]
        return all_info

    @property
    def win(self):
        while timezone.now() > self.tues_end:
            if self.get_home_score() >= self.get_away_score():
                return self.home
            return self.away

    def get_home_score(self):
        group = Score.objects.filter(active_squad=self.home)
        total = sum([score.pts for score in group])
        return total

    def get_away_score(self):
        group = Score.objects.filter(active_squad=self.away)
        total = sum([score.pts for score in group])
        return total

class Draft(models.Model):
    league = models.OneToOneField(League)
    start = models.DateTimeField(auto_now_add=True)

    def get_squads(self):
        return self.league.get_squads
    def whos_pick(self, pick):
        squads = list(self.get_squads())
        squad_1_numbers = [squads[0],[1,12,13,24,25,36,37,48,49]]
        squad_2_numbers = [squads[1],[2,11,14,23,26,35,38,47,50]]
        squad_3_numbers = [squads[2],[3,10,15,22,27,34,39,46,51]]
        squad_4_numbers = [squads[3],[4,9,16,21,28,33,40,45,52]]
        squad_5_numbers = [squads[4],[5,8,17,20,29,32,41,44,53]]
        squad_6_numbers = [squads[5],[6,7,18,19,30,31,42,43,54]]
        pick_list = [squad_1_numbers, squad_2_numbers, squad_3_numbers, squad_4_numbers, squad_5_numbers, squad_6_numbers]
        for group in pick_list:
            if pick in group[1]:
                return group[0]
