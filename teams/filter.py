import django_filters

from teams.models import Teams, Members


class TeamFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Teams
        fields = '__all__'


class MemberFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Members
        fields = '__all__'