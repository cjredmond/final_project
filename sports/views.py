from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from sports.models import Team, Squad, League
from django.urls import reverse, reverse_lazy


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        leagues = League.objects.all()
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
