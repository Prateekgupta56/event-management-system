from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

class Event(models.Model):
    event_name=models.CharField(max_length=100)
    event_start_date=models.DateTimeField(default=timezone.now)
    event_desc=models.TextField()
    event_end_date=models.DateTimeField()
    event_location=models.TextField()
    teacher = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True, blank=True, related_name="created_events")


    def __str__(self):
      return  self.event_name



class Profile(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True )
      profile_name=models.CharField(max_length=100, unique=True)
      profile_email=models.EmailField()
      profile_password=models.CharField(max_length=128)
      PROFILE_ROLES = [ ('Teacher', 'teacher'), ('Student', 'student') ]
      profile_role = models.CharField(max_length=7, choices=PROFILE_ROLES)
      
      def __str__(self):
        return  self.profile_name




class StudentEventRegistration(models.Model):
    event=models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participant_event')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    course = models.CharField(max_length=50)
    year = models.IntegerField()
    date_added=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
