from django.db import models



class Company(models.Model):
  name = models.CharField(max_length=200)
  bio = models.TextField(max_length=250,null=True, blank=True)

  def __str__(self):
    return self.name
    


class Advocate(models.Model):
  username = models.CharField(max_length=200)
  bio=models.TextField(max_length=500, null=True, blank=True)

  def __str__(self):
    return self.username
  

