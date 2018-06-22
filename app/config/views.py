from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def index(request):
    # return HttpResponseRedirect('/posts/')
    return redirect('posts:post-list')
