from django.db import models
from django.utils import timezone
import uuid
from datetime import datetime
from django.contrib.auth.models import User



class TaskStatus(models.TextChoices):
    TODO = 'Todo'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'

class ProjectStatus(models.TextChoices):
    UPCOMING = 'Upcoming'
    ONGOING = 'Ongoing'
    DONE = 'Done'
class Priority(models.TextChoices):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'LOW'

class Project(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    desc = models.TextField()
    Owner = models.ForeignKey(User,on_delete=models.CASCADE)
    creation_date = models.DateField(default=timezone.now)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.UPCOMING)

    def save(self, *args, **kwargs):
        
        if self.start_date and self.start_date < datetime.now().date():
            self.status = ProjectStatus.ONGOING
        super().save(*args, **kwargs)

class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=100)
    # You can define Todo, InProgress, and Done as separate models if needed

    def __str__(self):
        return self.name

class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=30,unique=True,default="")
    assigned = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_tasks',default=1)
    reporter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_tasks',default=1)
    desc = models.TextField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TODO)
    priority = models.CharField(max_length=20,null=True,choices=Priority.choices)

    def set_status(self, status):
        self.status = status



class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
