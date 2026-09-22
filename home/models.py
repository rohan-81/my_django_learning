from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title=models.CharField(max_length=200,null=False,blank=False)
    
    def __str__(self):
        return f"{self.title} --> (user : {self.user.username})"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, blank=True, null=True )
    email= models.EmailField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    age=models.IntegerField(null=True, blank=True)
    gender=models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True,max_length=300)


    def __str__(self):
        return f"{self.user.username}'s Profile"


