from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm




# Create your views here.
def index(request):
    #If the method is POST
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        
        if form.is_valid():
           # Yes, Save
           form.save()

           # Redirect to Home
           return HttpResponseRedirect('/')

        else:
           # NO, Show Error
           return HttpResponseRedirect(form.erros.as_json())

    # Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]

    # show 
    return render(request, 'posts.html',
                   {'posts': posts})

def delete(request, post_id):
   # Find post
   post = Post.objects.get(id = post_id)
   post.delete()
   return HttpResponseRedirect('/')


def edit(request, post_id):
   post = Post.objects.get(id = post_id)
   if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
           # Yes, Save
           form.save()

           # Redirect to Home
           return HttpResponseRedirect('/')

   else:
      form = PostForm
      return render(request, 'edit.html',
                   {'post': post, 'form': form})
   

def like(request, post_id):
   newlike = Post.objects.get(id = post_id)
   newlike.likecount += 1
   newlike.save()
   return HttpResponseRedirect('/')