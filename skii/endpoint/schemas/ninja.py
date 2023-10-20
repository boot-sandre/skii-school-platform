# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from typing import List, Any, Dict

from ninja import Schema


class FormInvalidResponseContract(Schema):
    """Form errors dict provided by Django from form validation

    Args:
        errors (Dict[str, List[Dict[str, Any]]]): a Django form errors dict

    Example:
        ::

        {
            "errors": {
                'password2': [
                    {
                        'message': 'The two password fields didn’t match.',
                        'code': 'password_mismatch'
                    }
                ]
            }
        }
    """

    errors: Dict[str, List[Dict[str, Any]]]
