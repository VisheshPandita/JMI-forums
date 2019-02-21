from django.db import models
from django.utils import timezone

# Create your models here.
class Moderator(models.Model):
  email = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  age = models.IntegerField()
  university = models.CharField(max_length=100)
  department = models.CharField(max_length=50)
  created = models.DateTimeField("Created on", default=timezone.now())
  
  def __str__(self):
    return self.username

class User(models.Model):
  email = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  age = models.IntegerField()
  university = models.CharField(max_length=100)
  department = models.CharField(max_length=50)
  created = models.DateTimeField("Created on", default=timezone.now())
  
  def __str__(self):
    return self.username
 
class Subforum(models.Model):
  subforum_name = models.CharField(max_length=50)
  ques_count = models.IntegerField()
  arti_count = models.IntegerField()
 
class Question(models.Model):
  user_id = models.IntegerField()
  subforum_id = models.IntegerField()
  ques_text = models.TextField()
