from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class Subforums(forms.ModelForm):
    class Meta:
        model = Subforum
        fields = [
            'subforum_name',
            'subforum_description'
        ]

class Questions(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'ques_text'
        ]        

class Answers(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'ans_text'
        ] 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'university', 'department']

    # def save(self, commit=True):
    #     user = super(ProfileForm, self).save(commit=False)
    #     user.age = self.cleaned_data['age']
    #     user.university = self.cleaned_data['university']
    #     user.department = self.cleaned_data['department']

    #     if commit:
    #         user.save()

    #     return user    

class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
