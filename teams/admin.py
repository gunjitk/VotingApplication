from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Teams, Members


class TeamAdmin(admin.ModelAdmin):

    list_display = ('team_name', 'company', 'created_at')
    search_fields = ['team_name']
    list_filter = ('team_name', 'company', 'created_at')
    list_per_page = 10


admin.site.register(Teams, TeamAdmin)


class MemberAdmin(admin.ModelAdmin):

    list_display = ('name', 'get_team', 'created_at', 'is_active')
    list_filter = ('name', 'team__team_name', 'created_at', 'is_active')
    search_fields = ['name']
    readonly_fields = ('user', )

    def get_team(self, obj):
        if obj.team:
            return obj.team.team_name
    get_team.short_description = 'Team'
    get_team.admin_order_field = 'team__team_name'

    def save_model(self, request, obj, form, change):
        if request.user != obj.user:
            raise PermissionDenied()
        obj.save()


admin.site.register(Members, MemberAdmin)