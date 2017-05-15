from django.contrib import admin
from django.contrib import messages

from sprints.adminForm import SprintsAdminForm
from sprints.models import Projects, Sprints, SprintSummary


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('project_name', 'team', 'start_date')
    search_fields = ['project_name']

admin.site.register(Projects, ProjectAdmin)


class SprintAdmin(admin.ModelAdmin):

    list_display = ('sprint_name', 'created_at', 'is_active', 'start_date', 'end_date')
    search_fields = ['sprint_name']


admin.site.register(Sprints, SprintAdmin)


class SprintSummaryAdmin(admin.ModelAdmin):

    list_display = ('sprint_name', 'assignee', 'ticket', 'issue_type', 'points', 'reporter', 'ticket_desc', 'due_date', 'status')
    search_fields = ['ticket', 'assignee', 'due_date', 'status', 'issue_type', 'reporter']
    readonly_fields = ('sprint_name', 'assignee', 'ticket', 'ticket_desc', 'points', 'due_date', 'status', 'issue_type',
                       'reporter')
    list_filter = ('assignee', 'issue_type', 'status')
    form = SprintsAdminForm

    def save_model(self, request, obj, form, change):

        if self.get_winner(obj):
            messages.info(request, "Winner till now is "+self.get_winner(obj))
        obj.save()

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(SprintSummaryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super(SprintSummaryAdmin, self).get_queryset(request).filter().order_by('-points')

admin.site.register(SprintSummary, SprintSummaryAdmin)