from django.contrib import admin

# Register your models here.
from url_bench.models import UrlBench


class UrlAdmin(admin.ModelAdmin):

    list_display = ('jira_url', 'host', 'created_at')

admin.site.register(UrlBench, UrlAdmin)