# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
import copy

LATITUDE_RANGE_CONFIG = {
    "left_digits": 3,
    "right_digits": 4,
    "positive": False,
    "min_value": -90,
    "max_value": 90,
}
LONGITUDE_RANGE_CONFIG = copy.deepcopy(LATITUDE_RANGE_CONFIG)
LONGITUDE_RANGE_CONFIG.update(
    {
        "min_value": -180,
        "max_value": 180,
    }
)
