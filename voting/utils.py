from django.db.models import Count
from django.utils import timezone

from voting.models import Booth, VotingParams, Votes


class BoothStore(object):

    def create_booth(self, **kwargs):
        try:
            return Booth.objects.create(**kwargs)
        except Exception:
            raise Exception("Integrity Error")

    def create_vote(self, **kwargs):
        try:
            return Votes.objects.create(**kwargs)
        except Exception:
            raise Exception("Integrity Error")

    def get_booth_object_or_none(self, **kwargs):
        try:
            booth = Booth.objects.get(**kwargs)
        except Booth.DoesNotExist:
            return None
        return booth

    def get_vote_object_or_none(self, **kwargs):
        try:
            vote = Votes.objects.get(**kwargs)
        except Votes.DoesNotExist:
            return None
        return vote


    def deactivate_booth(self, **kwargs):
        booth = self.get_booth_object_or_none(**kwargs)
        if booth:
            booth.is_active = False
            booth.end_date = timezone.now()
            booth.save()
            return True
        else:
            return False

    def get_parameter_object_or_none(self, **kwargs):
        try:
            param = VotingParams.objects.get(**kwargs)
        except Exception:
            return None
        return param

    def deactivate_vote(self, **kwargs):

        vote = self.get_vote_object_or_none(**kwargs)
        if vote:
            vote.delete()
            return True
        else:
            return False

    def create_parameter(self, **kwargs):
        try:
            return VotingParams.objects.create(**kwargs)
        except Exception:
            raise Exception("Integrity Error")

    def already_voted(self, **kwargs):
        return Votes.objects.filter(**kwargs).exists()

    def get_polling_result(self, **kwargs):
        return Votes.objects.filter(**kwargs).values("candidate__name").\
            annotate(vote_count=Count("id"))