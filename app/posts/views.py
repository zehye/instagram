from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from members.forms import PostForm
from .models import Post


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


def post_create(request):
    # 새 포스트를 만들기
    #   만든 후에는 해당하는 post_detail로 이동
    #   forms.py에 PostForm을 구현해서 사용

    # bound form(include file)
    #   PostForm(request.POST)
    #   PostForm(request.POST, request.FILES)

    # POST method에서는 생성 후 redirect
    # GET method에서는 form이 보이는 템플릿 렌더링
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Post(img_profile=request.FILES['file'])
            instance.save()
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post-create', context)
    return redirect('posts:post-detail')