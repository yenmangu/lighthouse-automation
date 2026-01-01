from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))


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

    def __str__(self):
        return f"{self.name}"


class Resource(models.Model):
    """Stores a single Resourse entity"""

    # TODO: Add resource_type when associated model is defined

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    description = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    resource_link = models.URLField(null=True)
    subjects = models.ManyToManyField(
        Subject, related_name="all_resources", through=SubjectResourceJoin
    )
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
