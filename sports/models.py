from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import csv

class League(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField()
    players = models.ManyToManyField('auth.User')
    live = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def schedule(self,squads):
        with open('6teams.csv') as infile:
            reader = csv.reader(infile)
            for row in reader:
                Matchup.objects.create(week=row[0], home=squads.get(sched_id=row[1]),
                away=squads.get(sched_id=row[2]))

    @property
    def get_squads(self):
        return self.squad_set.all()


@receiver(post_save, sender=League)
def create(**kwargs):
    created = kwargs['created']
    instance = kwargs['instance']
    teams = Team.objects.filter(league=None)
    for team in teams:
        Team.objects.create(city=team.city, name=team.name, league=instance, sport=team.sport, pts_last=team.pts_last, pts_proj=team.pts_proj)

class Squad(models.Model):
    user = models.OneToOneField('auth.User')
    name = models.CharField(max_length=40)
    league = models.ForeignKey(League)
    sched_id = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name
    @property
    def total_proj(self):
        teams = self.team_set.all()
        score = 0
        for team in teams:
            score = score + team.pts_proj
        return score


    def checker(self, sport):
        teams = self.team_set.all()
        count = 0
        for team in teams:
            if team.sport == sport:
                count += 1
        if count > 2:
            return False
        return True


SPORTS = [('f', 'football'), ('b', 'baseball'), ('k', 'basketball')]
class Team(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    squad = models.ForeignKey(Squad,null=True,blank=True)
    league = models.ForeignKey(League,null=True,blank=True)
    logo = models.FileField(null=True,blank=True)
    sport = models.CharField(max_length=1,choices=SPORTS)
    pts_last = models.IntegerField()
    pts_proj = models.IntegerField()
    #base = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Matchup(models.Model):
    week = models.IntegerField()
    home = models.ForeignKey(Squad, related_name='home')
    away = models.ForeignKey(Squad, related_name='away')

    def __str__(self):
        return (str(self.home) + " vs " + str(self.away))
