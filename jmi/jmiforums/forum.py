from django import forms
from .models import Subforum

class Subforums(forms.ModelForm):
    class Meta:
        model = Subforum
        fields = [
            'subforum_name',
            'subforum_description'
        ]