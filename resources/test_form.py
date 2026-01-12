from django.test import TestCase
from django.contrib.auth.models import User
from .forms import ResourceForm
from .models import Subject, Resource


class TestResourceForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_username",
            password="test_password",
        )
        self.subject = Subject.objects.create(
            name="Test Subject",
            slug="test-subject",
        )

    def test_form_is_valid(self):
        """
        Test form is valid with non empty values
        """

        resource_form = ResourceForm(
            data={
                "title": "test title",
                "author": self.user.id,
                "description": "This is a description",
                "subjects": [self.subject.id],
            }
        )
        self.assertTrue(
            resource_form.is_valid(),
            msg="The resource form is valid",
        )

    def test_save_creates_links_subject(self):

        form = ResourceForm(
            data={
                "title": "test_title",
                "author": self.user.id,
                "description": "Another useless description",
                "subjects": [self.subject.id],
                "new_subject_field": "A brand new subject",
            }
        )
        self.assertTrue(form.is_valid(), msg=form.errors.as_text)

        resource = form.save()

        # OPTIONAL: Assert that saving the form returns a Resource model instance (useful for debugging)
        self.assertIsInstance(resource, Resource)

        # CORE: Persistance signal - A saved model must have a primary key.
        self.assertIsNotNone(resource.pk)

        # OPTIONAL: Assert that the saved Resource can be retrieved from the database
        self.assertTrue(Resource.objects.filter(pk=resource.pk).exists())

        # CORE: Assert that exactly one Resource row was created in the database
        # (guard against double save bugs)
        self.assertEqual(
            Resource.objects.count(),
            1,
            msg="Expected exactly one Resource to be saved to the db",
        )
