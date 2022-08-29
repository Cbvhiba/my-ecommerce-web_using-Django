from django.db import models

# Create your models here.


class Banners(models.Model):
    img = models.ImageField()