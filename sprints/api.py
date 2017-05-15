from django.http import HttpResponse
from rest_framework import renderers
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework.decorators import list_route

from sprints.filter import ProjectsFilter, SprintsFilter
from sprints.models import Projects, Sprints
from sprints.serializers import ProjectsSerializer, SprintsSerializer
from sprints.utils import SprintsStore

sprints_store = SprintsStore()


class ProjectsViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectsSerializer
    queryset = Projects.objects.all()
    pagination_class = None
    renderer_classes = (renderers.JSONRenderer, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ProjectsFilter

    @list_route(methods=['patch'])
    def deactivate_project(self, request):
        success = sprints_store.deactivate_project(**request.data)
        if success:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class SprintsViewSet(viewsets.ModelViewSet):

    serializer_class = SprintsSerializer
    queryset = Sprints.objects.all()
    pagination_class = None
    renderer_classes = (renderers.JSONRenderer, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = SprintsFilter

    @list_route(methods=['patch'])
    def deactivate_sprint(self, request):
        success = sprints_store.deactivate_sprint(**request.data)
        if success:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)