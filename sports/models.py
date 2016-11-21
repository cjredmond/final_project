from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import csv
from datetime import datetime, timedelta
from django.utils import timezone

class League(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField()
    player = models.ManyToManyField('auth.User')
    live = models.BooleanField(default=False)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    weekly_matchup = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def duration(self):
        duration = self.end - self.start
        return duration

    def schedule(self,squads):
        ##https://github.com/taddeimania/tfb/tree/master/utility/schedules
        ##-CSV from JoelTaddei
        if self.weekly_matchup:
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
                    print(i)
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



class Score(models.Model):
    pts = models.FloatField(default=0)
    team = models.ForeignKey(Team)
    time = models.DateTimeField(null=True)#auto_now_add=True
    tag = models.URLField()
    #game_time = models.CharField(default='(FINAL)',max_length=50)

    def __str__(self):
        return str(self.team) + ' ' + str(self.pts)

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
        return result

    def wins(self):
        games = Matchup.objects.filter(away=self) | Matchup.objects.filter(home=self)
        wins = 0
        loss = 0
        for game in games:
            if game.win == self:
                wins += 1
            else:
                loss += 1
        return wins,loss


class Matchup(models.Model):
    league = models.ForeignKey(League)
    week = models.IntegerField()
    home = models.ForeignKey(Squad, related_name='home')
    away = models.ForeignKey(Squad, related_name='away')
    tues_start = models.DateTimeField(null=True)
    tues_end = models.DateTimeField(null=True)

    def __str__(self):
        return (str(self.home) + " vs " + str(self.away))

    def get_squad_score(self):
        home_scores = []
        away_scores = []
        for team in self.home.roster.all():
            for score in team.score_set.all():
                if score.time > self.tues_start and score.time < self.tues_end:
                    home_scores.append(score)
        for team in self.away.roster.all():
            for score in team.score_set.all():
                if score.time > self.tues_start and score.time < self.tues_end:
                    away_scores.append(score)
        home_total = 0
        away_total = 0
        for score in home_scores:
            home_total = home_total + score.pts
        for score in away_scores:
            away_total = away_total + score.pts
        return (home_total, away_total)
    def each_team_score(self):
        home_teams = self.home.roster.all()
        away_teams = self.away.roster.all()
        home_list = []
        away_list = []
        home_team = []
        home_pts = []
        away_team = []
        away_pts = []
        home_sports = []
        away_sports = []
        for team in home_teams:
            home_team.append(team)
            home_pts.append(round(team.week_score(self),3))
            home_sports.append(team.sport)
        for team in away_teams:
            away_team.append(team)
            away_pts.append(round(team.week_score(self),3))
            away_sports.append(team.sport)
        away_list.append(away_teams)
        away_list.append(away_pts)
        away_list.append(away_sports)
        home_list.append(home_teams)
        home_list.append(home_pts)
        home_list.append(home_sports)

        return home_list,away_list
    @property
    def win(self):
        while timezone.now() > self.tues_end:
            if self.get_squad_score()[0] > self.get_squad_score()[1]:
                print("Home")
                return self.home
            print("Away")
            return self.away
