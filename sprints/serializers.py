from sprints.models import Projects, Sprints

from rest_framework import serializers

from sprints.utils import SprintsStore
from teams.utils import TeamStore

sprint_store = SprintsStore()
team_store = TeamStore()


class ProjectInfo(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = '__all__'


class SprintInfo(serializers.ModelSerializer):

    class Meta:
        model = Sprints
        fields = '__all__'


class ProjectsSerializer(serializers.Serializer):

    project_name = serializers.CharField(required=True, max_length=50)
    team = serializers.CharField(required=True, max_length=50)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        data["team"] = team_store.get_team_object_or_none(team_name=data.get("team"))
        if not data["team"]:
            raise serializers.ValidationError("Invalid Team")
        return data

    def save(self):
        try:
            instance = sprint_store.create_project(**self.validated_data)
        except Exception as e:
            raise serializers.ValidationError(e.message)
        return instance


class SprintsSerializer(serializers.Serializer):

    sprint_name = serializers.CharField(required=True, max_length=50)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    project = serializers.CharField(required=True, max_length=50)

    def validate(self, data):
        data["project"] = sprint_store.get_project_object_or_none(project_name=data.get("project"))
        if not data["project"]:
            raise serializers.ValidationError("Invalid Project")
        return data

    def save(self):
        try:
            instance = sprint_store.create_sprint(**self.validated_data)
        except Exception as e:
            raise serializers.ValidationError(e.message)
        return instance