from django.db import models


class Navigation(models.Model):
    category = models.CharField(max_length=120)