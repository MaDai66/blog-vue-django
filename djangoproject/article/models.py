from django.db import models


class Article(models.Model):
    title = models.TextField()
    content = models.TextField()
    author_id = models.CharField(max_length=120)
    up = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    publish_time = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='article_covers/', blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)