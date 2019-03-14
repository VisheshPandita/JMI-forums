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
  return render(request=request,
                template_name="jmiforums/home.html",
                context={"moderator": Moderator.objects.all, "subforum": Subforum.objects.all})

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



