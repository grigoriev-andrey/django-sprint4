from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.forms import UserEditForm
from .constants import POSTS_PER_PAGE
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


def get_published_posts(queryset):
    queryset = queryset.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('category', 'location', 'author')
    return queryset


def index(request):
    post_list = get_published_posts(Post.objects)[:POSTS_PER_PAGE]

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    comments = post.comments.order_by('created_at')
    form = CommentForm()

    if not post.is_published:
        if post.author != request.user:
            raise Http404()

    if post.pub_date > timezone.now():
        if post.author != request.user:
            raise Http404()

    if post.category and not post.category.is_published:
        if post.author != request.user:
            raise Http404()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.pub_date:
                post.pub_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required(login_url='/auth/login/')
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if post.author != request.user:
        return redirect('blog:post_detail', id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if post.author != request.user:
        return redirect('blog:index')
    post.delete()
    return redirect('blog:index')


@login_required
def add_comment(request, id):
    post = get_object_or_404(
        get_published_posts(Post.objects),
        pk=id
    )
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'blog/comment.html', context)


@login_required
def edit_comment(request, id, comment_id):
    post = get_object_or_404(Post, pk=id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form, 'comment': comment, 'post': post
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, id, comment_id):
    post = get_object_or_404(Post, pk=id)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', id=id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=id)

    context = {'comment': comment, 'post': post}

    return render(request, 'blog/comment.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = get_published_posts(category.posts)

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category.html', context)


def user_detail(request):
    form = forms.UserDetailForm()
    context = {'form': form}
    return render(request, '')


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        post_list = Post.objects.filter(
            author=profile
        ).order_by('-pub_date')
    else:
        post_list = Post.objects.filter(
            author=profile,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).order_by('-pub_date')

    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'page_obj': page_obj,
    }

    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    context = {'form': form}
    return render(request, 'blog/user.html', context)
