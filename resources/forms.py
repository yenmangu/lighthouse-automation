from .models import Comment, Resource
from django import forms
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = (
            "title",
            "author",
            "description",
            "featured_image",
            "resource_link",
            "subjects",
        )
        widgets = {
            "description": TinyMCE(
                attrs={
                    "cols": 80,
                    "rows": 40,
                },
            )
        }
