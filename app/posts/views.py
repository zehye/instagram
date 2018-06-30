from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import PostForm, PostModelForm, CommentForm
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    # PostModelForm을 사용
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            # form에 없던 내용을 채워주는 방법 (author)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostModelForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_create_with_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)



@require_POST
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # permission denied
    if post.author != request.user:
        raise PermissionDenied('지울 권한이 없습니다.')
    post.delete()
    return redirect('posts:post-list')

#
# def post_delete_decorator(request, pk):
#     if request.method != 'POST':
#         return HttpResponseNotAllowed()
#     if not request.user.is_authenticated:
#         return redirect('members:login')
#


def comment_create(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get('text')
        if not text:
            return HttpResponse('댓글 내용을 입력하세요', status=400)
        Comment.objects.create(
            post=post,
            author=request.user,
            text=text
        )
        return redirect('posts:comment-create')


@login_required
def post_like_toggle(request, pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    filtered_list_posts = user.like_posts.filter(pk=post.pk)
    if filtered_list_posts.exitsts():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)

    if next_path:
        return redirect(next_path)
    return redirect('posts:post-detail', pk=pk)


@login_required
def post_create_without_form(request):
    # 새 포스트를 만들기
    #   만든 후에는 해당하는 post_detail로 이동
    #   forms.py에 PostForm을 구현해서 사용

    # bound form(include file)
    #   PostForm(request.POST)
    #   PostForm(request.POST, request.FILES)

    # POST method에서는 생성 후 redirect
    # GET method에서는 form이 보이는 템플릿 렌더링
    if request.method == 'POST':
        post = Post(
            author=request.user,
            photo=request.FILES['photo'],
            content=request.POST['content'],
        )
        post.save()
        return redirect('posts:post-detail', pk=post.pk)
    return render(request, 'posts/post_create.html')
