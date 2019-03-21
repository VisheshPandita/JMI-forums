from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  age = models.IntegerField()
  university = models.CharField(max_length=100)
  department = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.user.username} Profile"
    
class Moderator(models.Model):
  mod = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  email = models.CharField(max_length=50)

class Subforum(models.Model):
  subforum_name = models.CharField(max_length=50)
  subforum_description = models.TextField(blank=True, null=True)
  users = models.ManyToManyField(User)
  mods = models.ManyToManyField(Moderator)
  sub_date = models.DateTimeField(default=timezone.now)

class Question(models.Model):
  user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  subforum_id = models.ForeignKey(Subforum, on_delete=models.CASCADE)
  ques_text = models.TextField()
  ques_date = models.DateTimeField(default=timezone.now)

class Answer(models.Model):
  user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
  ans_text = models.TextField()
  ans_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
  user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
  comment_text = models.TextField()
  comment_date = models.DateTimeField(default=timezone.now)  