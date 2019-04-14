from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
from .forum import *
from django.contrib.auth.forms import( UserCreationForm,
                                        UserChangeForm,
                                        PasswordChangeForm)
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import RedirectView, ListView
from django.urls import reverse,reverse_lazy
from django.db import transaction, DatabaseError

# Create your views here.
def homepage(request):
  if not request.user.is_authenticated:
    return render(request, "jmiforums/login.html", {"message": None})
  context={
            "moderator": Moderator.objects.all,
            "subforum": Subforum.objects.all,
            "questions": Question.objects.all,
            "user": request.user,
          }
  return render(request, "jmiforums/home.html", context)


class PostListView(ListView):
  model = Question
  template_name = 'jmiforums/home.html'            #jmiforums/question_list.html
  context_object_name = 'questions'
  ordering = ['-date_posted']
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context={
            "moderator": Moderator.objects.all,
            "subforum": Subforum.objects.all,
            "questions": Question.objects.all,
          }
      return context


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
  if request.method == 'POST':
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("jmiforums:homepage"))
    else:
      return render(request, "jmiforums/login.html", {"message": "Invalid username/password. "})
  else:
    return render(request, 'jmiforums/login.html')

def logout_view(request):
  logout(request)
  return render(request,"jmiforums/login.html", {"message": "Logged Out"})

def subforum(request, subforum_name):
  try:
    subforum = Subforum.objects.get(subforum_name=subforum_name)
    sub_id = Subforum.objects.get(subforum_name=subforum_name)
  except Subforum.DoesNotExist:
    raise Http404("Subform does not exist")

  context={
    'subforum': subforum,
    'moderator': Moderator.objects.all(),
    'question': Question.objects.filter(subforum_id_id=sub_id).values()
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
      return redirect('jmiforums:profile')
    else:
      return redirect('jmiforums:profile')

  else:
    form = PasswordChangeForm(user=request.user)
    args = {'form': form}
    return render(request, 'jmiforums/change_password.html', args)

@login_required
def question(request, subforum_name):
  form = Questions(request.POST or None)
  if form.is_valid():
    question = form.save(commit=False)
    question.user_id = User.objects.get(pk=request.user.pk)
    question.subforum_id = Subforum.objects.get(subforum_name=subforum_name)
    question.save()
    return HttpResponseRedirect('/%s/' %subforum_name)

  context = {
    'form' : form,
  }

  return render(request, 'jmiforums/question.html', context)

@login_required
def instant_question(request):
  form = Instant_questions(request.POST or None)
  if form.is_valid():
    question = form.save(commit=False)
    question.user_id = User.objects.get(pk=request.user.pk)
    question.save()
    return HttpResponseRedirect('/%s/' %question.subforum_id)

  context = {
    'form' : form,
  }

  return render(request, 'jmiforums/instant_question.html', context)

@login_required
def view_question(request, subforum_name, ques_id):
    ques = Question.objects.get(pk=ques_id)
    ans = Answer.objects.filter(ques_id=ques_id).values()
    com = Comment.objects.filter(ques_id=ques_id).values()
    form = Answers(request.POST or None)
    form2 = Comments(request.POST or None)
    if form.is_valid():
      answer = form.save(commit=False)
      answer.user_id = User.objects.get(pk=request.user.pk)
      answer.ques_id = Question.objects.get(pk=ques_id)
      answer.save()
      return HttpResponseRedirect("/{subforum_name}/{ques_id}/view".format(subforum_name=subforum_name, ques_id=ques_id))

    if form2.is_valid():
      comment = form.save(commit=False)
      comment.user_id = User.objects.get(pk=request.user.pk)
      comment.ques_id = Question.objects.get(pk=ques_id)
      comment.save()
      return HttpResponseRedirect("/{subforum_name}/{ques_id}/view".format(subforum_name=subforum_name, ques_id=ques_id))

    context = {
      'ques': ques,
      'subforum_name': subforum_name,
      'ans': ans,
      'com': com,
      'form': form,
      'form2': form2,
    }
    return render(request, 'jmiforums/view_question.html', context)

# @login_required
# def answer(request, subforum_name, ques_id):
#   form = Answers(request.POST or None)
#   if form.is_valid():
#     answer = form.save(commit=False)
#     answer.user_id = User.objects.get(pk=request.user.pk)
#     answer.ques_id = Question.objects.get(pk=ques_id)
#     answer.save()
#     return HttpResponseRedirect("/{subforum_name}/{ques_id}/view".format(subforum_name=subforum_name, ques_id=ques_id))

#   context = {
#     'form' : form,
#   }

#   return render(request, 'jmiforums/answer.html', context)

# @login_required
# class upvote(RedirectView):
#   def get_redirect_url(self, *args, **kwargs):
#     slug = self.kwargs.get('slug')
#     print(slug)
#     obj = get_object_or_404(Post, slug=slug)
#     return obj.get_absolute_url()
