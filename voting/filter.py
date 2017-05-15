import django_filters

from voting.models import Booth, Votes


class BoothFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Booth
        fields = '__all__'


class VotingFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Votes
        fields = '__all__'