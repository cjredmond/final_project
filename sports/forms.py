from django import forms
from django.contrib.admin import widgets
from sports.models import League
from django.forms import ModelForm
from django.forms import widgets


class DateInput(forms.DateTimeInput):
    input_type = 'date'


class LeagueForm(ModelForm):
    start_date=forms.CharField()
    end_date=forms.CharField()
    class Meta:
        model = League
        fields = ['name','start_date','end_date']
        # widgets = {
        #     'start': DateInput(),
        #     'end': DateInput(),
        # }
