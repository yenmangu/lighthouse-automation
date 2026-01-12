from .models import Comment, Resource, Subject
from django import forms
from django.utils.text import slugify
from django.db.models import Q
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class ResourceForm(forms.ModelForm):

    new_subjects = forms.CharField(
        required=False,
        help_text="Add subjects separated by commas (e.g. Maths, JavaScript, Biology). If they don't already exist, they will be created for you.",
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

        # Get existing chosen subjects
        selected_subjects = self.cleaned_data.get("subjects")
        selected_names = [subject.name for subject in selected_subjects]

        # Get list of new subjects
        raw_new_subjects = (self.cleaned_data.get("new_subjects") or "").strip()
        new_subject_names = self._parse_subject_names(raw_new_subjects)

        # Merge subject lists
        merged_names = self._dedupe_names(selected_names + new_subject_names)

        # Early return: honour commit=False by not writing to DB.
        if not commit:
            self._pending_subject_names = merged_names
            return resource

        # Save to DB so `resource` has PK (required for M2M join-table writes).
        resource.save()

        # PERSIST the EXISTING choices made:
        # insert join-table rows like:
        # (resource_id, subject_id) pairs
        # MUST `save_m2m` before adding new m2m entity
        self.save_m2m()

        self._attach_subjects(resource, merged_names)

        return resource

    def save_m2m(self):
        """
        Override existing save_m2m method to ensure any pending names are attached via
        own defined _attach_subjects.
        Call super method first, to ensure existing normal behaviour persists.
        Reset to None is guarded protexted against raised exceptions by try... finally... block.
        """
        super().save_m2m()

        pending_names = getattr(self, "_pending_subject_names", None)
        if not pending_names:
            return

        try:
            self._attach_subjects(self.instance, pending_names)
        finally:
            self._pending_subject_names = None

    # ---------------- Start custom ---------------- #

    def _dedupe_names(self, names: list[str]) -> list[str]:
        """
        Docstring for _dedupe_names
        Deduplicate list of subject names case-insensitively
        """
        seen = set()
        deduped = []

        for name in names:
            clean_name = name.strip()
            if not clean_name:
                continue

            key = clean_name.lower()
            if key in seen:
                continue
            seen.add(key)

            deduped.append(clean_name)
        return deduped

    def _parse_subject_names(self, raw_value: str) -> list[str]:

        # Early empty list return
        if not raw_value:
            return []

        # define list for return and set for deduplication
        names = []
        seen = set()

        for part in raw_value.split(","):
            name = part.strip()
            if not name:
                continue

            # NOTE:
            # In a production-facing, multilingual system, I would use:
            #   key = name.casefold()
            # casefold() handles Unicode and edge cases more robustly.
            # For this project (English only), lower() is sufficient
            # and improves readability while clarifying intent.

            key = name.lower()
            # If key exists: skip adding to names
            if key in seen:
                continue

            seen.add(key)
            names.append(name)

        return names

    def _attach_subjects(self, resource: Resource, subject_names: list[str]) -> None:
        """
        Attach Subject relationships to a Resource based on a list of subject names.

        For each provided name, this method:
        - reuses an existing Subject if one exists (case-insensitive match), or
        - creates a new Subject if no match is found.

        All resolved Subject instances are then associated with the given Resource.
        This method is idempotent with respect to existing relationships and will
        not create duplicate Subject records or duplicate many-to-many links.
        """

        if not subject_names:
            return

        # Case-insensitive lookup
        # (__iexact - https://docs.djangoproject.com/en/dev/ref/models/querysets/#iexact)
        # SQL equivalent: ILIKE

        query = Q()
        for name in subject_names:
            # query = query OR Q(...)
            # Each loop adds another OR clause
            query |= Q(name__iexact=name)

        existing_subjects = Subject.objects.filter(query)

        existing_by_lower = {
            subject.name.lower(): subject for subject in existing_subjects
        }

        subjects_to_attach = []

        # Iterate all subjects chosen or entered
        for name in subject_names:
            lower_name = name.lower()

            # Build the relationships from subjects chosen,
            # that exist in DB already
            if lower_name in existing_by_lower:
                subjects_to_attach.append(existing_by_lower[lower_name])
                continue

            # Subject doesn't exist (case-insensitive): create it.
            # Subject.save() already has slugify()

            subject = Subject.objects.create(name=name)

            # Append newly created subject to subjects_to_attach
            subjects_to_attach.append(subject)

        # Add all subjects_to_attach;
        # unpack each element of list into a positional argument
        resource.subjects.add(*subjects_to_attach)

    # ----------------- End custom ----------------- #

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subjects"].widget.attrs.update(
            {
                "size": 6,
                "class": "form-select",
            }
        )

    class Meta:
        model = Resource
        fields = (
            "author",
            "title",
            "description",
            "featured_image",
            "resource_link",
            "subjects",
            "new_subjects",
        )

        exclude = ("slug",)

        help_texts = {
            "subjects": "Hold ⌘ (Mac) / Ctrl (Windows) to select multiple subjects.",
        }

        widgets = {
            "description": TinyMCE(
                attrs={
                    "cols": 80,
                    "rows": 40,
                },
            ),
            "subjects": forms.SelectMultiple(),
        }
