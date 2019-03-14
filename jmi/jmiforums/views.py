from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
from .models import *
from .forum import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def homepage(request):
  if not request.user.is_authenticated:
    return render(request, "jmiforums/login.html", {"message": None})
  context={
            "moderator": Moderator.objects.all,
            "subforum": Subforum.objects.all,
            "user": request.user,
          }
  return render(request, "jmiforums/home.html", context)

def login_view(request):
  username = request.POST["username"]
  password = request.POST["password"]
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    return HttpResponseRedirect(reverse("jmiforums:homepage"))
  else:
    return render(request, "jmiforums/login.html", {"message": "Invalid username/password. "})  

def logout_view(request):
  logout(request)
  return render(request,"jmiforums/login.html", {"message": "Logged Out"})

def subforum(request, subforum_name):
  try:
    subforum = Subforum.objects.get(subforum_name=subforum_name)
  except Subforum.DoesNotExist:
    raise Http404("Subform does not exist")
  
  context={
    'subforum': subforum,
    'moderator': Moderator.objects.all()
  }
  return render(request, "jmiforums/subforum.html", context)

def create(request):
  form = Subforums(request.POST or None)
  if form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('jmiforums:homepage'))

  context = {
    'form' : form
  }

  return render(request, 'jmiforums/createSub.html', context)  



