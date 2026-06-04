from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer

from .models import Article, Category, Comment


def home(request):
    articles = Article.objects.filter(is_published=True).select_related('category')
    return render(request, "articles/home.html", {"articles": articles})


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('category'),
        slug=slug
    )
    return render(request, "articles/article_detail.html", {"article": article})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, is_published=True).select_related('category')
    return render(request, "articles/category_detail.html",
                  {"articles": articles, "category": category})


class CommentAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            article__slug=self.kwargs['slug']
        )

    def perform_create(self, serializer):
        article = get_object_or_404(
            Article,
            slug=self.kwargs['slug']
        )

        serializer.save(article=article)