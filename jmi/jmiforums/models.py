from django.db import models
from django.utils import timezone

# Create your models here.
class Subforum(models.Model):
  subforum_id = models.AutoField(primary_key=True)
  subforum_name = models.CharField(max_length=50)
  ques_count = models.IntegerField()

  def __str__(self):
    return self.subforum_name

class Moderator(models.Model):
  mod_id = models.AutoField(primary_key=True)
  email = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  age = models.IntegerField()
  university = models.CharField(max_length=100)
  department = models.CharField(max_length=50)
  created = models.DateTimeField("Created on", default=timezone.now())
  subforum_id = models.ForeignKey(Subforum, on_delete=models.CASCADE, related_name='moderatorOf')

  def __str__(self):
    return self.username

class User(models.Model):
  user_id = models.AutoField(primary_key=True)
  email = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  age = models.IntegerField()
  university = models.CharField(max_length=100)
  department = models.CharField(max_length=50)
  created = models.DateTimeField("Created on", default=timezone.now())
  
  def __str__(self):
    return self.username
 
 
class Question(models.Model):
  ques_id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_question')
  subforum_id = models.ForeignKey(Subforum, on_delete=models.CASCADE, related_name='subforum_question')
  ques_text = models.TextField()

class Answer(models.Model):
  ans_id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answer')
  subforum_id = models.ForeignKey(Subforum, on_delete=models.CASCADE, related_name='subforum_answer')
  ans_text = models.TextField()

class Comment(models.Model):
  comment_id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
  subforum_id = models.ForeignKey(Subforum, on_delete=models.CASCADE, related_name='subforum_comment')
  comment_text = models.TextField()    