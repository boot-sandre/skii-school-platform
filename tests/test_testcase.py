# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com> synw (https://github.com/synw/)
# project: SkiiSchoolPlatform
# github: https://github.com/boot-sandre/skii-school-platform/
# template: https://github.com/synw/django-spaninja
from .testcase import SkiiTestCase


class TestSkiiTestCase(SkiiTestCase):
    def test_get_public(self):
        res = self.client.get("/")
        assert res.status_code == 200

    def test_get_anonymous(self):
        res = self.client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res.status_code == 302

    def test_get_redirected_to_login(self):
        res_redirect = self.user_client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res_redirect.status_code == 302
        res = self.user_client.get(f"{self.root_path}login")
        assert res.status_code == 200

    def test_get_admin_authentificated(self):
        res = self.admin_client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res.status_code == 200
