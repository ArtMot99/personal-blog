from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Category, Post, Comment, ContactMessage


class ModelTests(TestCase):
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

    def test_user_str(self) -> None:
        self.assertEqual(str(self.user), self.user.username)

    def test_category_str(self) -> None:
        category = Category.objects.create(
            name="TestCategory",
        )

        self.assertEqual(str(category), category.name)

    def test_post_str(self) -> None:
        self.assertEqual(str(self.post), self.post.title)

    def test_comment_str(self) -> None:
        comment = Comment.objects.create(
            text="Test comment",
            post=self.post,
            author=self.user,
        )

        self.assertEqual(str(comment), comment.text)

    def test_contact_message_str(self) -> None:
        contact_message = ContactMessage.objects.create(
            name="Test",
            email="test@email.com",
            subject="Test subject",
            message="Test message",
        )

        self.assertEqual(str(contact_message), contact_message.name)
