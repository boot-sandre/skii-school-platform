# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from django import forms

from skii.platform.entities import mutate_event_state
from skii.platform.models.event import LessonEvent
from skii.platform.models.resource import LocationResource


class LessonForm(forms.ModelForm):
    class Meta:
        model = LessonEvent
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


class LocationResourceForm(forms.ModelForm):
    class Meta:
        model = LocationResource
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
