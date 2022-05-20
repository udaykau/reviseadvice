from django.db import models


# Create your models here.
class Registration(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=30)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)


class Movies(models.Model):
    sno = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='media/movies', null=True, blank=True)
    name = models.CharField(max_length=100)
    short_description = models.TextField(max_length=50000)
    language = models.CharField(max_length=100)
    rating = models.CharField(max_length=30)
    genre = models.CharField(max_length=1000)
    releasing_date = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)


# Create your models here.
class contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    message = models.CharField(max_length=3000)
    date = models.DateTimeField(auto_now=True)

