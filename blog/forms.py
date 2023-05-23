from django import forms

from blog.models import Category


class PostFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="All",
        label="",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class PostSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by keywords..."}),
    )


class CommentForm(forms.Form):
    text = forms.CharField(
        max_length=255,
        label="",
        widget=forms.Textarea(
            attrs={"placeholder": "Join the discussion and leave a comment!"}
        ),
    )
