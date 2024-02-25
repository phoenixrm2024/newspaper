# articles/views.py
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import Article, Comment
from .forms import CommentForm
# Create your views here.

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.html'
    ordering = ['-date']
    # Or:
    # def get_queryset(self):
    #     return Article.objects.order_by('-date')

class CommentGet(DetailView):
    model = Article
    template_name = 'article_detail.html'
    
    def get_context_data(self, **kwargs):
# First by helping super() we pulled all existing information into context 'as kwargs':
        context = super().get_context_data(**kwargs)
# Then we add the variable name (form) with its value (CommentForm()) to the context:
        context['form'] = CommentForm
# and finally we returned the 'updated context':
        return context
    
class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = 'article_detail.html'
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)
    def get_success_url(self):
        article = self.get_object()
        return reverse('article_detail', kwargs={'pk': article.pk})
        
class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'body')
    template_name = 'article_edit.html'

    def test_func(self):
       obj = self.get_object()
       return obj.author == self.request.user
    
    # get_object() returns 'current object' that view is displaying, and we set 
    # the variable obj to it. Then we say, if the author on the current object 
    # matches the current user (by accessing via self.request), then allow (return) it.
    
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'body')
    template_name = 'article_new.html'
    
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)
    # Before sending the form, we add the 'author' field and set it as the'user' 
    #   by accessing the 'self.request object' (it holds the meta-data about 
    #   the request that is being sent), so we can access the 'user' who is 
    #   currently logged in.
    # form_valid() is a 'helper built-in method' to redirect to the success_url 
    # when the form data is being posted.