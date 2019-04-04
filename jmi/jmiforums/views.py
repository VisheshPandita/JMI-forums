from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import *
from .forum import *
from django.contrib.auth.forms import( UserCreationForm, 
                                        UserChangeForm,
                                        PasswordChangeForm)
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import transaction, DatabaseError

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

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if form.is_valid() and profile_form.is_valid():
      try:
        with transaction.atomic():
          user = form.save()
          profile = profile_form.save(commit=False)
          profile.user = user
          profile.save()
      except DatabaseError:
        pass    

      username = form.cleaned_data.get('username')
      messages.success(request, f'Account Created for {username}!')
      return redirect('jmiforums:homepage')
  else:
    form = UserRegisterForm()
    profile_form = ProfileForm()
  return render(request, 'jmiforums/register.html', {"form":form, "profile_form": profile_form,})

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

@login_required
def create(request):
  form = Subforums(request.POST or None)
  if form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('jmiforums:homepage'))

  context = {
    'form' : form
  }

  return render(request, 'jmiforums/createSub.html', context)  

@login_required
def profile(request):
  args = {'user': request.user}
  return render(request, 'jmiforums/profile.html', args)

@login_required
def edit_profile(request):
  if request.method == 'POST':
    form = EditProfile(request.POST, instance=request.user)

    if form.is_valid():
      form.save()
      return redirect("jmiforums:profile")
  else:
    form = EditProfile(instance=request.user)
    args = {'form': form}
    return render(request, 'jmiforums/edit_profile.html', args)

@login_required
def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(data=request.POST, user=request.user)

    if form.is_valid():
      form.save()
      update_session_auth_hash(request, form.user)
      return redirect('jmiforums:change_password')
    else:
      return redirect('jmiforums:change_password')

  else:
    form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'jmiforums/change_password.html', args)    

