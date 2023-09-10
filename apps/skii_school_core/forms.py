from django import forms

from apps.skii_school_core.entities import mutate_event_state
from apps.skii_school_core.models import Event, Location


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "state", "start", "stop", "teacher", "students"]

    def clean_state(self):
        if "state" in self.changed_data:
            initial = self.initial.get("state", None)
            value = self.cleaned_data.get("state", None)
            if value and "state" in self.cleaned_data:
                value_res = mutate_event_state(value, initial)
                if value_res == self.cleaned_data["state"]:
                    return value_res
            return initial


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["label", "description", "country", "address1", "address2", "city",
                  "cover", "illustration", "coordinate"]
