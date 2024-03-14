from django import forms
from career.models import Career
from exam.models import Stage

class CandidateForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    career = forms.ModelChoiceField(Career.objects.all())
    stage = forms.ModelChoiceField(Stage.objects.all())