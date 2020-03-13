# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Pictureurl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='campaign')
    auid = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100)
    image_path = models.TextField()
    details = models.TextField(null=True)
    file_name = models.CharField(max_length=100)
    short_link = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    hyperlink = models.CharField(max_length=220, null=True)
    action = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["-date_created"]

class CSV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='directory')
    auid = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    csv_file_name = models.CharField(max_length=100, null=True)
    csv_path = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name





class AnalyticsManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, Pictureurl):
            obj, created = self.get_or_create(instance=instance)
            obj.count =+ 1
            obj.save()
            return obj.count
        return None


class Analytics (models.Model):
    device = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=250)
    campaign_url = models.ForeignKey(Pictureurl, editable=False, on_delete=models.CASCADE)
    timestamps = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    objects = AnalyticsManager()

    def __str__(self):
        return self.count

# class Client:
#     browser =


class FacebookStatus(models.Model):

    class Meta:
        verbose_name_plural = 'Facebook Statuses'
        ordering = ['publish_timestamp']

    STATUS = (
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    )
    status = models.CharField(max_length=255,
        choices=STATUS, default=STATUS[0][0])
    publish_timestamp = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=255)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.message