from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Essentials", {"fields" : ["email", "username", "password", "age", "created"]}),
    ("Non-essentials", {"fields" : ["university", "department"]})
  ]

class QuestAdmin(admin.ModelAdmin):
  formfield_overrides = {
    models.TextField: {'widget': TinyMCE()}
  }


admin.site.register(Moderator, UserAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subforum)
admin.site.register(Question, QuestAdmin)