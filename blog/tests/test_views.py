from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.forms import PostFilterForm, PostSearchForm, SignUpForm
from blog.models import User, ContactMessage, Post


class FunctionBasedViewTests(TestCase):
    def test_index_view(self) -> None:
        """
        Test for index view

        This test checks access to the site's index page
        as well as a correctly passed context and a valid template

        :return: None
        """
        response = self.client.get(reverse("blog:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")
        self.assertIsInstance(response.context["filter_form"], PostFilterForm)
        self.assertIsInstance(response.context["search_form"], PostSearchForm)
        self.assertIn("page_obj", response.context)

    def test_register_view(self) -> None:
        """
        Test for the registration view

        This test checks if the SignUpForm has been submitted to the view and
        also checks that after creating a new user, it will be stored in the
        database and the user will be redirected to the login page

        :return: None
        """
        response = self.client.get(reverse("blog:sign-up"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/sign-up.html")
        self.assertIsInstance(response.context["form"], SignUpForm)

        form_data = {
            "username": "test_user",
            "password1": "Test12345",
            "password2": "Test12345",
        }
        response = self.client.post(reverse("blog:sign-up"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="test_user").exists())
        self.assertRedirects(response, reverse("login"))

    def test_contact_view(self) -> None:
        """
        Test for the contact view

        This test verifies that after a successful user recall,
        the recall will be saved to the database

        :return: None
        """
        response = self.client.get(reverse("blog:contact"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/contact.html")

        form_data = {
            "name": "Test Name",
            "email": "test@email.com",
            "subject": "Test Subject",
            "message": "Test Message",
        }
        response = self.client.post(reverse("blog:contact"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(
            name="Test Name"
        ).exists())


class ClassBasedViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test12345",
        )
        self.post = Post.objects.create(
            title="Test title",
            content="Lorem ipsum dolor",
            author=self.user,
        )
        self.client.login(username="test_user", password="Test12345")

    def test_post_detail_view(self) -> None:
        """
        Test for the PostDetailView

        This test checks if a registered user can
        leave a comment on the post detail page

        :return: None
        """
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertIn("comments", response.context)

        form_data = {
            "text": "Test comment",
        }
        url = reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)

    def test_post_create_view_forbidden_for_simple_user(self) -> None:
        response = self.client.get(reverse("blog:post-create"))

        self.assertEqual(response.status_code, 403)

    def test_post_update_view_forbidden_for_simple_user(self) -> None:
        response = self.client.get(
            reverse("blog:post-update", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_post_delete_view_forbidden_for_simple_user(self) -> None:
        response = self.client.get(
            reverse("blog:post-delete", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, 403)
