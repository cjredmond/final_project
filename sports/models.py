from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import csv
from datetime import datetime, timedelta, timezone

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
        ##-JoelTaddei
        if self.weekly_matchup:
            weeks = self.duration() // timedelta(days=7)

            with open('6teams.csv') as infile:
                reader = csv.reader(infile)
                for i,row in enumerate(reader):
                    Matchup.objects.create(league=self,week=row[0], home=squads.get(sched_id=row[1]),
                    away=squads.get(sched_id=row[2]))
                    if i == weeks*3:
                        break

    @property
    def get_squads(self):
        return self.squad_set.all()


SPORTS = [('f', 'football'), ('b', 'baseball'), ('k', 'basketball'), ('h', 'hockey'), ('s', 'soccer')]
class Team(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    logo = models.FileField(null=True,blank=True)
    sport = models.CharField(max_length=1,choices=SPORTS)
    pts_last = models.IntegerField()
    pts_proj = models.IntegerField()

    def __str__(self):
        return self.name

class Score(models.Model):
    pts = models.FloatField(null=True)
    team = models.ForeignKey(Team)
    time = models.DateTimeField(auto_now_add=True)

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
        print(teams)
        count = 0
        for team in teams:
            if team.sport == sport:
                count += 1
        if count > 2:
            return False
        return True

class Matchup(models.Model):
    league = models.ForeignKey(League)
    week = models.IntegerField()
    home = models.ForeignKey(Squad, related_name='home')
    away = models.ForeignKey(Squad, related_name='away')

    def __str__(self):
        return (str(self.home) + " vs " + str(self.away))

    @property
    def home_score_calc(self):
        home_roster = self.home.roster.all()
        score = 0
        for x in home_roster:
            score += x.week_1
        return score
    def away_score_calc(self):
        away_roster = self.away.roster.all()
        score = 0
        for x in away_roster:
            score += x.week_1
        return score

    def winner(self):
        if home_score >= away_score:
            return home
        return away

class PayLeague(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField()
    player = models.ManyToManyField('auth.User')
    live = models.BooleanField(default=False)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.name)
