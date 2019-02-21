from django.shortcuts import render
from django.http import HttpResponse
from .models import Moderator

# Create your views here.
def homepage(request):
  return render(request=request,
                template_name="jmiforums/home.html",
                context={"moderator": Moderator.objects.all})
