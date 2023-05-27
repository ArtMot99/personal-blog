from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q, QuerySet
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from blog.forms import (
    PostFilterForm,
    PostSearchForm,
    CommentForm,
    SignUpForm,
    PostForm,
    ContactForm,
)
from blog.models import Post, Comment, ContactMessage


def index(request) -> HttpResponse:
    """
    The index home page view

    Which contains the processing of two widgets
    and also contains pagination, prefetch and select related
    was used to reduce the load on the database

    :param request: request
    :return: HttpResponse
    """
    post_list = (
        Post.objects.select_related("author")
        .prefetch_related("categories")
        .annotate(num_comments=Count("comments"))
        .order_by("-created_at")
    )
    filter_form = PostFilterForm()
    search_form = PostSearchForm()

    if request.method == "GET":
        filter_form = PostFilterForm(request.GET)
        search_form = PostSearchForm(request.GET)

        if filter_form.is_valid():
            category = filter_form.cleaned_data["category"]
            if category:
                post_list = post_list.filter(categories=category)

        if search_form.is_valid():
            search_term = search_form.cleaned_data["search_term"]
            if search_term:
                post_list = post_list.filter(
                    Q(
                        title__icontains=search_term
                    ) | Q(
                        content__icontains=search_term
                    )
                )
                if not post_list.exists():
                    messages.error(request, "No results found")

    paginator = Paginator(post_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "filter_form": filter_form,
        "search_form": search_form,
    }

    return render(request, "blog/index.html", context=context)


def register(request) -> HttpResponse:
    """
    User registration view

    That processes the registration form
    and redirects to the login page

    :param request: request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "registration/sign-up.html", {"form": form})


def permission_denied(request, exception) -> HttpResponse:
    """Handle 403 error and return custom template"""
    return render(request, "error_pages/error_403.html", status=403)


def page_not_found(request, exception) -> HttpResponse:
    """Handle 404 error and return custom template"""
    return render(request, "error_pages/error_404.html", status=404)


def about(request) -> HttpResponse:
    """About page view"""
    return render(request, "blog/about.html")


def contact(request) -> HttpResponse:
    """
    View for contact page

    In this view, the feedback form is processed, after the successful
    submission of the form, the user will receive notifications
    of successful submission

    :param request: request
    :return: HttpResponse
    """
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            contact_message = ContactMessage(
                name=name, email=email, subject=subject, message=message
            )
            contact_message.save()
            messages.success(
                request, "Your message has been sent successfully!"
            )
            return redirect(request.path)

    return render(request, "blog/contact.html", {"form": form})


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs) -> dict:
        """
        Processing comments on the selected post

        Show comments that belong to the selected post,
        add a comment form to the context, and add pagination to the
        page with comments

        :param kwargs: **kwargs
        :return: dict
        """
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object)
        paginator = Paginator(comments, 4)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["comment_form"] = CommentForm()
        context["comments"] = page_obj

        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Process the form for adding a comment by the user

        In this view, the url address is processed and after the user
        has left a comment, he will be redirected to the section that is
        marked comments-section in the template

        :param request: request
        :param args: *args
        :param kwargs: **kwargs
        :return: HttpResponse
        """
        self.object = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(
                text=form.cleaned_data["text"],
                post=self.object,
                author=request.user
            )
            comment.save()

            url = reverse("blog:post-detail", kwargs={"pk": self.object.pk})
            return redirect(f"{url}?page=1#comments-section")

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("blog:index")

    def test_func(self) -> bool:
        """Check if user is superuser or Forbidden(403)"""
        return self.request.user.is_superuser

    def form_valid(self, form) -> HttpResponse:
        """
        Assign the author to the post and also save the picture

        :param form: PostCreateForm
        :return: HttpResponse
        """
        form.instance.author = self.request.user
        self.object = form.save()
        if "image" in self.request.FILES:
            self.object.image = self.request.FILES["image"]
            self.object.save()

        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self) -> bool:
        """Check if user is superuser or Forbidden(403)"""
        return self.request.user.is_superuser

    def get_success_url(self) -> Optional[str]:
        """Redirect after update to post page"""
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:index")

    def test_func(self) -> bool:
        """Check if user is superuser or Forbidden(403)"""
        return self.request.user.is_superuser


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self) -> Optional[str]:
        """To stay at the #comments-section after delete a comment"""
        post_pk = self.object.post.pk

        return reverse(
            "blog:post-detail", kwargs={"pk": post_pk}
        ) + "#comments-section"

    def get_queryset(self) -> QuerySet[Comment]:
        """Comments will be filtered by the current user"""
        queryset = super().get_queryset()

        return queryset.filter(author=self.request.user)
