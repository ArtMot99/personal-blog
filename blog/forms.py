from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm

from blog.models import Category, User, Post, ContactMessage


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


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ["title", "content", "categories", "image"]


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label=False, widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    email = forms.EmailField(
        label=False, widget=forms.TextInput(attrs={"placeholder": "Email"})
    )
    subject = forms.CharField(
        label=False, widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )
    message = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={"placeholder": "Write your message..."}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
