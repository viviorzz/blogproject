import markdown
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category
# Create your views here.

def index(request):
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
    }
    return render(request,'blog/detail.html',context=context)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request,'blog/index.html',{'error_msg':error_msg})
    post_list = Post.objects.filter(title__icontains=q)
    return render(request,'blog/index.html',{'error_msg':error_msg,'post_list':post_list})