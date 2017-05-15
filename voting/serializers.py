from rest_framework import serializers
from sprints.utils import SprintsStore
from teams.utils import TeamStore
from voting.models import Booth, Votes
from voting.utils import BoothStore

booth_store = BoothStore()
sprint_store = SprintsStore()
team_store = TeamStore()

class BoothInfo(serializers.ModelSerializer):

    class Meta:
        model = Booth
        fields = '__all__'


class VotingInfo(serializers.ModelSerializer):

    class Meta:
        model = Votes
        fields = '__all__'


class BoothSerializer(serializers.Serializer):

    sprint = serializers.CharField(required=True, max_length=50)
    booth_name = serializers.CharField(required=True, max_length=50)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        data["sprint"] = sprint_store.get_sprints_object_or_none(sprint_name=data.get("sprint"))
        if not data["sprint"]:
            raise serializers.ValidationError("Invalid Sprint")
        return data

    def save(self):
        try:
            instance = booth_store.create_booth(**self.validated_data)
        except Exception as e:
            raise serializers.ValidationError(e.message)
        return instance


class VotingSerializer(serializers.Serializer):

    booth = serializers.CharField(required=True, max_length=50)
    candidate = serializers.CharField(required=True)
    voter = serializers.CharField(required=True)
    parameter = serializers.CharField(required=True)
    comments = serializers.CharField(required=False, max_length=200)

    def validate(self, data):
        data["booth"] = booth_store.get_booth_object_or_none(booth_name=data.get("booth"))
        data["parameter"] = booth_store.get_parameter_object_or_none(parameter_name=data.get("parameter"))
        data["candidate"] = team_store.get_member_object_or_none(name=data.get("candidate"))
        data["voter"] = team_store.get_member_object_or_none(name=data.get("voter"))
        if not data["booth"]:
            raise serializers.ValidationError("Invalid Booth")
        if not data["parameter"]:
            raise serializers.ValidationError("Invalid Parameter")
        if not data["voter"]:
            raise serializers.ValidationError("Invalid Voter")
        if not data["candidate"]:
            raise serializers.ValidationError("Invalid Candidate")
        if booth_store.already_voted(booth=data["booth"], parameter=data["parameter"], voter=data["voter"].name):
            raise serializers.ValidationError("Already Voted For %s Parameter" % (data["parameter"].parameter_name))
        return data

    def save(self):
        try:
            instance = booth_store.create_vote(**self.validated_data)
        except Exception as e:
            raise serializers.ValidationError(e.message)
        return instance


class ParameterSerializer(serializers.Serializer):

    parameter_name = serializers.CharField(required=True, max_length=50)
    comments = serializers.CharField(required=True)

    def save(self):
        try:
            instance = booth_store.create_parameter(**self.validated_data)
        except Exception as e:
            raise serializers.ValidationError(e.message)
        return instance