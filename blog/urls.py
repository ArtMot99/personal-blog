from django.urls import path
from blog.views import index, PostDetailView, register

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("signup/", register, name="sign-up"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
]
