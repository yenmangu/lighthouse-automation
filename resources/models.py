from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))
STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}


# ResourceSubject 'join' table included for greater control
# Unique constraint is applied to the entity model through the Meta class, to ensure every resource-subject association is unique
class SubjectResourceJoin(models.Model):
    """Join table provides the many-to-many relationship between Resource & Subject"""

    resource = models.ForeignKey("resources.Resource", on_delete=models.CASCADE)
    subject = models.ForeignKey("resources.Subject", on_delete=models.CASCADE)

    class Meta:
        """Provides unique constraint on the combination of resource & subject"""

        constraints = [
            models.UniqueConstraint(
                fields=["resource", "subject"], name="unique_subject_resource"
            )
        ]


class Subject(models.Model):
    """Stores a single Subject entity"""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """
        Override the save() method to ensure a slug is always created/provided
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Resource(models.Model):
    """Stores a single Resourse entity"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    description = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    resource_link = models.URLField(blank=True, null=True)
    subjects = models.ManyToManyField(
        Subject, related_name="all_resources", through=SubjectResourceJoin
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """
        Return the absolute URL for this Resource instance.

        Used by generic views and redirects after create/update operations.
        """
        return reverse(
            "resources:resource_detail",
            kwargs={
                "slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        """
        Override the save() method to ensure a slug is always created/provided.

        Prevents URL reversing failures and avoids IntegrityError when two
        resources would otherwise share the same slug.
        """
        if not self.slug:
            self.slug = self._build_unique_slug()
        super().save(*args, **kwargs)

    def _build_unique_slug(self) -> str:
        """
        Create a slug from the title, adding a numeric suffix if needed.

        Example:
        - "My Notes" -> "my-notes"
        - if taken -> "my-notes-2", then "my-notes-3", etc.
        """
        base_slug = slugify(self.title) or "resource"
        candidate_slug = base_slug
        suffix = 2

        while self.__class__.objects.filter(slug=candidate_slug).exists():
            candidate_slug = f"{base_slug}-{suffix}"
            suffix += 1
        return candidate_slug


class Comment(models.Model):
    """
    Stores a single comment entry related to :model:`auth.User` & :model:`resources.Resource`
    """

    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
