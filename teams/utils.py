from teams.models import Teams, Members


class TeamStore(object):

    def create_team(self, **kwargs):
        try:
            return Teams.objects.create(**kwargs)
        except Exception:
            raise Exception("Integrity Error")

    def create_members(self, team, member_data):
        member_list = []
        for member in member_data:
            member_list.append(
                Members(team=team, **member)
            )
        return Members.objects.bulk_create(member_list)

    def get_team_object_or_none(self, **kwargs):
        try:
            team = Teams.objects.get(**kwargs)
        except Teams.DoesNotExist:
            return None
        return team

    def get_member_object_or_none(self, **kwargs):
        try:
            member = Members.objects.get(**kwargs)
        except Members.DoesNotExist:
            return None
        return member

    def create_member(self, member_data):
        try:
            return Members.objects.create(**member_data)
        except Exception:
            raise Exception("Duplicate Member Found")

    def deactivate_team(self, **kwargs):
        team = self.get_team_object_or_none(**kwargs)
        if team:
            team.is_active = False
            team.save()
            return True
        else:
            return False

    def deactivate_member(self, **kwargs):
        member = self.get_member_object_or_none(**kwargs)
        if member:
            member.is_active = False
            member.save()
            return True
        else:
            return False

    def member_already_exists(self, **kwargs):
        return Members.objects.filter(**kwargs).exists()