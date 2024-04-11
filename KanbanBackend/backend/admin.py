# admin.py

from django.contrib import admin
from .models import Project, Board,Task

admin.site.register(Project)
admin.site.register(Board)
admin.site.register(Task)