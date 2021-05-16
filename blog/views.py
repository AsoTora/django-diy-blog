from django.shortcuts import render
from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
from django.contrib.auth.models import User  # Blog author or commenter
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


# class-view template: <app>/<model>_<viewtype>.html


def index(request):
    """
    home page.
    """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )


class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5
    template_name = 'blog_list.html'


class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name = 'blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(BlogAuthor, pk=self.kwargs['pk'])
        return context


class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog


class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.
    """
    model = BlogAuthor
    paginate_by = 5


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Form for creating a blog
    """
    model = Blog
    fields = ['name', 'description']

    def form_valid(self, form):
        """
        Connect created blog model with BlogAuthor
        """
        form.instance.author = get_object_or_404(BlogAuthor, user_id=self.request.user.id)
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Form for updating a blog
    """
    model = Blog
    fields = ['name', 'description']

    def form_valid(self, form):
        """
        Connect updated blog model with BlogAuthor
        """
        form.instance.author = get_object_or_404(BlogAuthor, user_id=self.request.user.id)
        return super().form_valid(form)

    def test_func(self):
        """
        Auth check for blog author only.
        """
        blog = self.get_object()
        if self.request.user.id == blog.author.user_id:
            return True
        return False


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Form for deleting a blog.
    """
    model = Blog
    success_url = '/'

    def test_func(self):
        """
        Auth check for blog author only.
        """
        blog = self.get_object()
        if self.request.user.id == blog.author.user_id:
            return True
        return False


class BlogCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login. 
    """
    model = BlogComment
    fields = ['text', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })


from django.conf import settings
from django.http import Http404
from .utils import *


def debug_random_populate(request):
    """
    create mock data
    """
    if not settings.DEBUG:
        raise Http404

    try:
        user = User.objects.get(username='John Testing')
    except User.DoesNotExist:
        print('hello')
        user = User(username='John Testing', email='JohnTesting@gmail.com', password=12345)
        user.save(force_insert=False)

    for i in range(1, 5):
        Blog.objects.get_or_create(
            name=random_name(),
            description=random_descr(),
            author=BlogAuthor.objects.filter(user_id=user.id).first()
        )

    return render(
        request,
        'index.html',
    )
