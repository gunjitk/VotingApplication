from django import forms

from sprints.models import Sprints


class SprintsAdminForm(forms.ModelForm):
    class Meta:
        model = Sprints
        fields = '__all__'

    def clean(self):
        if Sprints.objects.filter(is_active=1).exists():
            raise forms.ValidationError("Active sprint found")