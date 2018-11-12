from blog.forms import PostForm,CommentForm
from blog import models
from django.views.generic import TemplateView, UpdateView, DeleteView, DetailView, ListView, CreateView

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class About(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    context_object_name='post_list'
    template_name = "blog/main.html"
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte= timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = models.Post
    context_object_name = "post_detail"

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html' #means which teplate to be redirected after logging in if not
    form_class = PostForm
    model = models.Post
    success_url = reverse_lazy("post_draft_list") #where to be redirected

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name='blog/post_edit.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = models.Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('post_draft_list')
    model = models.Post

class DraftListView(LoginRequiredMixin, ListView):
    template_name='blog/post_draft_list.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = models.Post
    context_object_name = "draft_list"

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull=True).order_by('create_date')



@login_required
def post_publish(request,pk):
    post = get_object_or_404(models.Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk = pk)



@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(models.Comment,pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk= post_pk)