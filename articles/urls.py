from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),

    path(
        'api/articles/<slug:slug>/comments/',
        views.CommentAPIView.as_view(),
        name='article_comments_api'
    )
]
