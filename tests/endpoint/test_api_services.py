from django.urls import reverse_lazy

from skii.platform.factories import LocationResourceFactory
from skii.platform.schemas.resource import LocationSaveContract
from tests.testcase import SkiiServiceTestCase


class SkiiServiceTest(SkiiServiceTestCase):
    def test_skii_service_client_superuser_session(self):
        """Can use self.client and self.client_superuser."""

        anonyme_session = self.client.session.items()
        admin_session = self.client_superuser.session.items()

        self.assertListEqual(list(dict(anonyme_session).keys()), [])
        self.assertListEqual(
            list(dict(admin_session).keys()),
            ["_auth_user_id", "_auth_user_backend", "_auth_user_hash"],
        )

    def test_skii_service_user_client(self):
        """Can use the method self.client_user(student)."""
        student = self.get_factory_instance("student")
        self.client_auth(student.user)
        session = self.client.session.items()
        self.assertListEqual(
            list(dict(session).keys()),
            ["_auth_user_id", "_auth_user_backend", "_auth_user_hash"],
        )

    def test_skii_client_forbid_get_docs_anonyme(self):
        """Cannot fetch api docs with client.get method as anonyme user."""
        response = self.client.get("skii:openapi-view")
        self.assertEqual(response.status_code, 302)

    def test_skii_client_forbid_get_docs_is_active(self):
        """Cannot fetch api docs with client.get method as activate user."""
        student = self.get_factory_instance("student")
        self.client_auth(student.user)
        user = self.user_model.objects.get(
            pk=int(self.client.session.get("_auth_user_id"))
        )
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        response = self.client.get("skii:openapi-view")
        self.assertEqual(response.status_code, 302)

    def test_skii_client_get_docs_is_staff(self):
        """Can fetch api docs with client.get method as staff member."""
        teacher = self.get_factory_instance("teacher")
        self.client_auth(teacher.user)
        user = self.user_model.objects.get(
            pk=int(self.client.session.get("_auth_user_id"))
        )
        assert user.is_active
        assert user.is_staff
        assert not user.is_superuser
        response = self.client.get("skii:openapi-view")
        self.assertEqual(response.status_code, 200)

    def test_skii_client_get_docs_is_superuser(self):
        """Can fetch api docs with client.get method as superuser/admin."""
        response = self.client_superuser.get("skii:openapi-view")
        self.assertEqual(response.status_code, 200)

    def test_skii_api_reverse_urls(self):
        """SkiiClient have to reverse api routes names in urls."""
        urls_reversed = reverse_lazy("skii:openapi-view")
        self.assertURLEqual(urls_reversed, "/skii/docs")

    def test_skii_api_post(self):
        """Skii client have to trigger a POST HTTP request."""
        teacher = self.get_factory_instance("teacher")
        self.client_auth(teacher.user)
        payload = LocationSaveContract.from_orm(LocationResourceFactory.build()).dict(
            exclude_none=True
        )
        response = self.client.post(
            "skii:location_create",
            payload,
        )
        assert response.status_code == 200
        assert list(response.json().keys()) == [
            "description",
            "label",
            "address1",
            "address2",
            "city",
            "country",
            "cover",
            "illustration",
            "coordinate",
            "value",
            "pk",
        ]
