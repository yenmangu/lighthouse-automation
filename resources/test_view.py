from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Resource, Subject
from .views import ResourceDelete, ResourceDetail


class TestEntityDeletion(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myAdmin",
            password="adminPass",
            email="super@user.com",
        )

        self.subject = Subject.objects.create(
            name="Test Subject",
            slug="test-subject",
        )

        self.resource = Resource.objects.create(
            title="Resource Title",
            author=self.user,
            description="Test description",
            status="p",
        )
        self.resource.subjects.add(self.subject)

        self.non_admin = User.objects.create_user(
            username="myUser",
            password="userPass",
            email="non_admin@user.com",
        )

    def test_delete_view_deletes_resource(self):
        """
        A superuser should be able to delete a Resource via delete view.
        """
        # CORE: ensure we are authenticated (Delete View is login protected)
        self.client.login(username="myAdmin", password="adminPass")

        delete_url = reverse(
            "resources:resource_delete",
            kwargs={
                "slug": self.resource.slug,
            },
        )

        response = self.client.post(delete_url)

        # OPTIONAL: Confirm redirect happened (to list view)
        self.assertEqual(response.status_code, 302)

        # CORE: Assert Resource row no longer exists in DB
        self.assertFalse(
            Resource.objects.filter(pk=self.resource.pk).exists(),
            msg="Resource should have been deleted from the DB",
        )

        # CORE: Assert no Resource records remain after deletion
        self.assertEqual(
            Resource.objects.count(),
            0,
            msg="Expected no rows after deletion",
        )

    def test_negative_delete(self):
        self.client.login(
            username="myUser",
            password="userPass",
        )

        delete_url = reverse(
            "resources:resource_delete",
            kwargs={
                "slug": self.resource.slug,
            },
        )

        response = self.client.post(delete_url)

        # CORE: Confirm 403 forbidden response for non Author/Superuser
        self.assertEqual(response.status_code, 403)

        # CORE: Confim record still exists
        self.assertTrue(
            Resource.objects.filter(pk=self.resource.pk).exists(),
            msg="Resource should not be deleted by a non-author user.",
        )
