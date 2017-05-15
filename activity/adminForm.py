from django import forms

from activity.models import ActivityBoard
from sprints.models import Sprints


class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = ActivityBoard
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get("sprint") != Sprints.get_active_sprint():
            raise forms.ValidationError("Choose Active Sprint")