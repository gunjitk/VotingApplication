from rest_framework import renderers
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework.decorators import list_route
from rest_framework.response import Response

from voting.filter import BoothFilter, VotingFilter
from voting.models import Booth, Votes, VotingParams
from voting.serializers import BoothSerializer, VotingSerializer, ParameterSerializer
from voting.utils import BoothStore

booth_store = BoothStore()

class BoothViewSet(viewsets.ModelViewSet):

    serializer_class = BoothSerializer
    queryset = Booth.objects.all()
    pagination_class = None
    renderer_classes = (renderers.JSONRenderer, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = BoothFilter

    @list_route(methods=['patch'])
    def deactivate_booth(self, request):
        success = booth_store.deactivate_booth(**request.data)
        if success:
            return Response(data="Deactivated", status=200)
        else:
            return Response(data="Deactivate Failed", status=400)


class VotingViewSet(viewsets.ModelViewSet):

    serializer_class = VotingSerializer
    queryset = Votes.objects.all()
    pagination_class = None
    renderer_classes = (renderers.JSONRenderer, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = VotingFilter

    @list_route(methods=['delete'])
    def deactivate_vote(self, request):
        success = booth_store.deactivate_vote(**request.data)
        if success:
            return Response(data="Deactivated", status=200)
        else:
            return Response(data="Deactivate Failed", status=400)

    @list_route(methods=['get'])
    def get_polls(self, request):
        return Response(data=booth_store.get_polling_result(**request.data), status=200)

class ParameterViewSet(viewsets.ModelViewSet):

    serializer_class = ParameterSerializer
    queryset = VotingParams.objects.all()
    pagination_class = None
    renderer_classes = (renderers.JSONRenderer, )
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)