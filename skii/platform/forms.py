from django import forms

from skii.platform.entities import mutate_event_state
from skii.platform.models.event import Lesson, Location


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["label", "state", "start", "stop", "teacher", "students"]

    def clean_state(self):
        """Hooks to mutate the state."""
        initial = self.initial.get("state", None)
        value = self.cleaned_data.get("state", None)
        if "state" in self.changed_data:
            value_res = mutate_event_state(value, initial)
            return value_res
        else:
            return value


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "label",
            "description",
            "country",
            "address1",
            "address2",
            "city",
            "cover",
            "illustration",
            "coordinate",
        ]
