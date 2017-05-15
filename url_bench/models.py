from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UrlBench(models.Model):

    jira_url = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Url Bench'
        verbose_name_plural = 'Url Bench'