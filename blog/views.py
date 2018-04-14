from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request): #This View lists all the Blog posts in one Page(just like a normal blog page)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk): # When the "Title/Heading" link of the post is clicked, it should go to that Post.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request): # View for the form
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)# after clicking "save" button, you are redirected to
                                                      #  "post_detail" template
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk): # View for editing an already running Blog Post
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_draft_list(request): # View to display drafts/unpublished blog Posts
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})



@login_required
def post_publish(request, pk): # View to publish drafts/unpublished blog Posts
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)



@login_required
def post_remove(request, pk): # View to remove/delete blog Posts
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list') # gets redirected to 'post_list'view after deleting the post
                                 # so as to get further instructions there
