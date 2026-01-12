from django.test import TestCase
from django.contrib.auth.models import User

from .models import Resource


class TestUniqueSlug(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_slug_generation_and_is_unique(self):
        resource_one = Resource.objects.create(
            title="Test Resource",
            author=self.user,
            description="First resource",
        )

        resource_two = Resource.objects.create(
            title="Test Resource",
            author=self.user,
            description="Second resource",
        )

        resource_three = Resource.objects.create(
            title="Test Resource",
            author=self.user,
            description="Third resource",
        )
        slugs = {
            resource_one.slug,
            resource_two.slug,
            resource_three.slug,
        }
        self.assertEqual(len(slugs), 3)
