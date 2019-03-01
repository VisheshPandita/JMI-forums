from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Moderator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def homepage(request):
  return render(request=request,
                template_name="jmiforums/home.html",
                context={"moderator": Moderator.objects.all})

def register(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, "New Account Created")
      login(request, user)

      return redirect("jmiforums:homepage")
    else:
      for msg in form.error_messages:
        print(form.error_messages[msg])


  form = UserCreationForm
  return render(request,
                "jmiforums/register.html",
                context={"form":form})