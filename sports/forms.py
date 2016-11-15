from django import forms
from django.contrib.admin import widgets
from sports.models import League
from django.forms import ModelForm
from django.forms import widgets


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class LeagueForm(ModelForm):

    class Meta:
        model = League
        fields = ['name', 'limit', 'start', 'end', 'weekly_matchup']
        widgets = {
            'start': DateInput(),
            'end': DateInput(),
        }
