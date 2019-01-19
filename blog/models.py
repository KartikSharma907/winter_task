from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    first_name = models.CharField(max_length = 40, null="True", default="")
    last_name = models.CharField(max_length = 40, null="True", default="")
    following = models.ManyToManyField(User, related_name="following")
    dob = models.DateField(default = datetime.date.today)
    #gender_choice = (('M',"Male"),('F',"Female"),('O',"Other"))
    #gender = models.CharField(max_length=1,choices=gender_choice,default=None)
    def __str__(self):
        # __str__ overrides the default names of the objects of this class
        # Overriding it gives a more human friendly name of the objects of this class.
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_published = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_published']

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    #If related_name is not used, django automatically uses the name of the model
    # with the suffix _set
    #So using related_name makes further syantax bit cleaner and less clunky.

    def __str__(self):
        return self.comment
