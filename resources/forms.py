from .models import Comment, Resource, Subject
from django import forms
from django.utils.text import slugify
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class ResourceForm(forms.ModelForm):

    new_subject_field = forms.CharField(
        required=False,
        label="Add a new Subject",
        help_text="If subject does not exist it will be created.",
    )

    def save(self, commit=True):
        """
        Save the Resource instance and optionally create/link a new Subject.

        This override pauses the default ModelForm save so we can control ordering:
        - save the Resource first to ensure it has a primary key,
        - persist the user's selected subjects via `save_m2m()` (join-table rows),
        - optionally create/find a Subject from `new_subject_name` and attach it.

        The `commit` flag represents the caller's intent:
        - True (default): persist the Resource and its relationships.
        - False: return an unsaved Resource instance (no DB writes).
        """

        # Build the model instance but do NOT save to DB yet.
        resource = super().save(commit=False)

        # Early return: honour commit=False by not writing to DB.
        if not commit:
            return resource

        # Save to DB so `resource` has PK (required for M2M join-table writes).
        resource.save()

        # PERSIST the EXISTING choices made:
        # insert join-table rows like:
        # (resource_id, subject_id) pairs
        # MUST `save_m2m` before adding new m2m entity
        self.save_m2m()

        # Attempt to get a new subject name
        raw_subject_name = (self.cleaned_data.get("new_subject_name") or "").strip()
        raw_subject_name = " ".join(raw_subject_name.split())

        if raw_subject_name:
            subject_slug = slugify(raw_subject_name)

            # `get_or_create` returns (subject, created_flag);
            # flag is not needed, so is assigned to `_`
            subject, _ = Subject.objects.get_or_create(
                slug=subject_slug,
                defaults={
                    "name": raw_subject_name,
                },
            )
            # Add one extra join-table row: (resource_id, subject_id)
            resource.subjects.add(subject)

        return resource

    class Meta:
        model = Resource
        fields = (
            "title",
            "author",
            "description",
            "featured_image",
            "resource_link",
            "subjects",
            "new_subject_field",
        )

        widgets = {
            "description": TinyMCE(
                attrs={
                    "cols": 80,
                    "rows": 40,
                },
            )
        }
