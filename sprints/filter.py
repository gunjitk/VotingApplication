import django_filters

from sprints.models import Sprints, Projects


class SprintsFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Sprints
        fields = '__all__'


class ProjectsFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Projects
        fields = '__all__'