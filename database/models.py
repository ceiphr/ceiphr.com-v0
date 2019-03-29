from django.db import models
from django.utils.text import slugify
from sorl.thumbnail import ImageField
import datetime

# Header metadata and slogan options (randomized in views.py)
class Metadata(models.Model):
    slogan = models.CharField(default="", max_length=100)
    desc = models.CharField(default="", max_length=300)

class Article(models.Model):
    title = models.CharField(default="", max_length=255)
    preview = models.CharField(default="", max_length=200)
    slug = models.SlugField(blank=True)
    image = ImageField(upload_to='articles/%Y/%m/%d')
    content = models.TextField(default="", max_length=20000)
    modified = models.DateField(default=datetime.date.today) 
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs) 
    class Meta:
        ordering = ['-modified']
    def __str__(self):
        return 'Article: ' + self.title

class Project(models.Model):
    title = models.CharField(default="", max_length=50)
    summary = models.CharField(default="", max_length=100)
    image = ImageField(upload_to='img/projects/')
    link = models.CharField(default="", max_length=50)
    published = models.DateField(default=datetime.date.today)
    class Meta:
        ordering = ['-published']
    def __str__(self):
        return 'Project: ' + self.title

class Event(models.Model):
    title = models.CharField(default="", max_length=50)
    desc = models.CharField(default="", max_length=400)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    image = ImageField(upload_to='img/events/')
    link = models.CharField(default="", max_length=100)
    class Meta:
        ordering = ['-end_date']
    def __str__(self):
        return 'Event: ' + self.title

class Skill(models.Model):
    title = models.CharField(default="", max_length=50)
    experience = models.IntegerField(default=0)
    last_used = models.IntegerField(default=0)   
    class Meta:
        ordering = ['-experience']
    def __str__(self):
        return 'Skill: ' + self.title

class SocialLink(models.Model):
    title = models.CharField(default="", max_length=50)
    url = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    class Meta:
        ordering = ['-priority']
    def __str__(self):
        return 'Link: ' + self.title

# User details
class Detail(models.Model):
    legal_name = models.CharField(default="", max_length=50)
    user_name = models.CharField(default="", max_length=50)
    phone = models.CharField(default="", max_length=50)
    email = models.CharField(default="", max_length=50)
    def __str__(self):
        return 'Detail: ' + self.legal_name

# Documents served from media/documents/...
class Document(models.Model):
    document_name = models.CharField(default="", max_length=50)
    document = models.FileField(upload_to='documents/')
    def __str__(self):
        return 'Document: ' + self.document_name