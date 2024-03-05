from django import forms

class UplaoadFileForm(forms.Form):
    file=forms.FileField()