from django import forms

class MovieSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')