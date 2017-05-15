from django.contrib import admin
# Register your models here.
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Count

from voting.adminForm import VoteAdminForm
from voting.models import Votes, VotingParams, Booth, VoteSummary, QuarterSummary
from operator import or_
from django.db.models import Q


class VoteAdmin(admin.ModelAdmin):

    list_display = ('get_candidate', 'get_voter', 'get_parameter', 'get_booth', 'get_winner', 'comments')
    list_filter = ('voter__name', 'booth__booth_name', 'created_at')
    list_per_page = 10
    search_fields = ['voter__name']
    form = VoteAdminForm

    def changelist_view(self, request, extra_context=None):

        if not request.user.is_superuser:
            self.list_display = ('get_voter', 'get_candidate', 'get_parameter', 'get_booth', 'comments')
        else:
            self.list_display = ('get_candidate', 'get_voter', 'get_parameter', 'get_booth', 'get_winner', 'comments')
        return super(VoteAdmin, self).changelist_view(request, extra_context)

    def get_changeform_initial_data(self, request):
        active_booth = None
        voter = None
        if hasattr(request.user, "members"):
            voter = request.user.members
        active_booths = Booth.objects.filter(is_active=1)
        if active_booths:
            active_booth = active_booths.first()
        return {'voter': voter, 'booth': active_booth}

    def save_model(self, request, obj, form, change):
        if request.user != form.cleaned_data.get("voter").user:
            raise PermissionDenied()
        # if self.get_winner(obj):
        #     messages.info(request, "Winner till now is "+self.get_winner(obj))
        obj.save()

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return super(VoteAdmin, self).get_queryset(request).filter(booth__is_active=True, voter__user=request.user)
        else:
            return super(VoteAdmin, self).get_queryset(request).filter(booth__is_active=True)

    def get_candidate(self, obj):
        return obj.candidate.name
    get_candidate.short_description = 'Candidate'
    get_candidate.admin_order_field = 'candidate__name'

    def get_voter(self, obj):
        return obj.voter.name
    get_voter.short_description = 'Voter'
    get_voter.admin_order_field = 'voter__name'

    def get_booth(self, obj):
        return obj.booth.booth_name
    get_booth.short_description = 'Booth'
    get_booth.admin_order_field = 'booth__booth_name'

    def get_parameter(self, obj):
        return obj.parameter.parameter_name
    get_parameter.short_description = 'Parameter'
    get_parameter.admin_order_field = 'parameter__parameter_name'

    def get_winner(self, obj):
        dict_list = Votes.objects.filter(booth=obj.booth).values("candidate__name"). \
            annotate(vote_count=Count("id"))
        if dict_list:
            seq = max(dict_list, key=lambda x: x['vote_count'])
            return seq.get("candidate__name")
    get_winner.short_description = 'Winner'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(VoteAdmin, self).get_search_results(
            request, queryset, search_term)
        search_words = search_term.split()
        if search_words:
            q_objects = [Q(**{field + '__icontains': word})
                         for field in self.search_fields
                         for word in search_words]
            queryset |= self.model.objects.filter(reduce(or_, q_objects))
        return queryset, use_distinct

admin.site.register(Votes, VoteAdmin)


class BoothAdmin(admin.ModelAdmin):

    list_display = ('booth_name', 'start_date', 'end_date', 'is_active')
    search_fields = ['booth_name']
    list_filter = ('booth_name', 'created_at')
    list_per_page = 10

admin.site.register(Booth, BoothAdmin)


class ParamAdmin(admin.ModelAdmin):

    list_display = ('parameter_name', 'comments')
    search_fields = ['parameter_name']
    list_filter = ('parameter_name', 'created_at')
    list_per_page = 10

admin.site.register(VotingParams, ParamAdmin)


class VoteSummaryAdmin(admin.ModelAdmin):

    list_display = ('sprint', 'candidate', 'total_votes')
    search_fields = ['sprint', 'candidate']
    list_filter = ('sprint', 'candidate')
    list_per_page = 10

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(VoteSummaryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return VoteSummary.objects.filter().order_by('-total_votes')

admin.site.register(VoteSummary, VoteSummaryAdmin)


class QuarterAdmin(admin.ModelAdmin):

    list_display = ('quarter_name', 'current_winner', 'total_votes')
    search_fields = ['quarter_name', 'current_winner']
    list_filter = ('quarter_name', 'current_winner', 'total_votes')
    list_per_page = 10
    readonly_fields = ['current_winner', 'total_votes']


admin.site.register(QuarterSummary, QuarterAdmin)