from django.test import TestCase

from blog.forms import (
    PostFilterForm,
    PostSearchForm,
    CommentForm,
    SignUpForm,
    PostForm,
    ContactForm,
)
from blog.models import Category


class FormTests(TestCase):
    def test_post_filter_form_with_data(self) -> None:
        category = Category.objects.create(name="FirstCategory")
        form_data = {"category": category}
        form = PostFilterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_filter_form_without_data(self) -> None:
        form_data = {"category": ""}
        form = PostFilterForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_search_form_with_data(self) -> None:
        form_data = {"search_term": "test"}
        form = PostSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_search_form_without_data(self) -> None:
        form_data = {"search_term": ""}
        form = PostSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_search_form_correct_placeholder(self) -> None:
        form = PostSearchForm()

        self.assertEqual(
            form.fields["search_term"].widget.attrs["placeholder"],
            "Search by keywords...",
        )

    def test_comment_form_valid_data(self) -> None:
        form_data = {"text": "This is a test comment!"}
        form = CommentForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_comment_form_correct_placeholder(self) -> None:
        form = CommentForm()

        self.assertEqual(
            form.fields["text"].widget.attrs["placeholder"],
            "Join the discussion and leave a comment!",
        )

    def test_sign_up_form_valid_data(self) -> None:
        form_data = {
            "username": "test_user",
            "password1": "Test12345",
            "password2": "Test12345",
        }
        form = SignUpForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_form_valid_data(self) -> None:
        category = Category.objects.create(name="Test")
        form_data = {
            "title": "Test Post",
            "content": "Test content",
            "categories": [category.id],
            "image": "test_image.jpg",
        }
        form = PostForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_post_form_without_title_should_be_invalid(self) -> None:
        category = Category.objects.create(name="Test")
        form_data = {
            "title": "",
            "content": "Test content",
            "categories": [category.id],
            "image": "test_image.jpg",
        }
        form = PostForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_contact_form_valid_data(self) -> None:
        form_data = {
            "name": "Test Name",
            "email": "test@email.com",
            "subject": "Test Subject",
            "message": "Test message!",
        }
        form = ContactForm(data=form_data)

        self.assertTrue(form.is_valid())
