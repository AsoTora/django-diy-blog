from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogger/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blogs-by-author'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blog/new', views.BlogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update', views.BlogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', views.BlogDeleteView.as_view(), name='blog-delete'),
    path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog_comment'),
    path('populate/', views.debug_random_populate)
]