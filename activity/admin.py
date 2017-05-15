from django.contrib import admin
from django.core.exceptions import PermissionDenied

from activity.adminForm import ActivityAdminForm
from .models import ActivityBoard

# Register your models here.
from sprints.models import Sprints


class ActivityAdmin(admin.ModelAdmin):

    list_display = ('get_member', 'remark')
    list_filter = ('modified_at',)
    search_fields = ['modified_at']
    form = ActivityAdminForm

    def get_queryset(self, request):
        return super(ActivityAdmin, self).get_queryset(request).filter(sprint__is_active=True)

    def get_changeform_initial_data(self, request):
        return {'member': request.user.members,
                'sprint': Sprints.get_active_sprint()}

    def get_member(self, obj):
        return obj.member.name
    get_member.short_description = 'Member'
    get_member.admin_order_field = 'member__name'

    def get_sprint(self, obj):
        return obj.sprint.sprint_name
    get_sprint.short_description = 'Sprint'
    get_sprint.admin_order_field = 'sprint__sprint_name'

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("member") and request.user != form.cleaned_data.get("member").user:
            raise PermissionDenied()
        obj.save()

    def delete_model(self, request, obj):
        if request.user != obj.member:
            raise PermissionDenied()

admin.site.register(ActivityBoard, ActivityAdmin)