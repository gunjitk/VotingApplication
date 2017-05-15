from __future__ import unicode_literals

from django.db import models

# Create your models here.

from sprints.models import Sprints
from teams.models import Members


class ActivityBoard(models.Model):

    sprint = models.ForeignKey(Sprints)
    member = models.ForeignKey(Members)
    remark = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.remark

    class Meta:
        verbose_name = 'Activity Board'
        verbose_name_plural = 'Activity Board'