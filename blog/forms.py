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
