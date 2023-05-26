from django.urls import path

from blog.views import (
    index,
    PostDetailView,
    register,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentDeleteView,
    contact,
    about,
)

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("signup/", register, name="sign-up"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
]
