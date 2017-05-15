from celery.task import periodic_task
from datetime import timedelta

from django.db.models.aggregates import Count

from voting.models import VoteSummary, Votes, Booth, QuarterSummary
from annoying.functions import get_object_or_None
from votr import celeryconfig
from celery import Celery

app = Celery('tasks')
app.config_from_object(celeryconfig)


@periodic_task(run_every=timedelta(seconds=10))
def update_vote_summary():
    active_booth = get_object_or_None(Booth, is_active=1)
    if active_booth:
        votes = Votes.objects.filter(booth=active_booth)
    else:
        return
    votes = votes.values('candidate_id').annotate(
        total_votes = Count('candidate_id')
    ).values('total_votes', 'candidate_id', 'booth__sprint__id')
    vote_summary_list = []
    for vote in votes:
        vote_summary_list.append(VoteSummary(**{'total_votes': vote.get('total_votes'),
                                                'candidate_id': vote.get('candidate_id'),
                                                'sprint_id': vote.get('booth__sprint__id')}))
    VoteSummary.objects.bulk_create(vote_summary_list)

#
# @periodic_task(run_every=timedelta(seconds=10))
# def update_quarter_summary():
#     active_quarter = get_object_or_None(QuarterSummary, is_active=1)
#     if active_quarter:
#         sprints = active_quarter.booth_set.filter().values_list('sprint_id', flat=True)
#     else:
#         return
#     votes = votes.values('candidate_id').annotate(
#         total_votes=Count('candidate_id')
#     ).values('total_votes', 'candidate_id', 'booth__sprint__id')
#     vote_summary_list = []
#     for vote in votes:
#         vote_summary_list.append(VoteSummary(**{'total_votes': vote.get('total_votes'),
#                                                 'candidate_id': vote.get('candidate_id'),
#                                                 'sprint_id': vote.get('booth__sprint__id')}))
#     VoteSummary.objects.bulk_create(vote_summary_list)
