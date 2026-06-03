from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Article, Category


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
    articles = Article.objects.filter(category=category, is_published=True)
    return render(request, "articles/category_detail.html",
                  {"articles": articles, "category": category})
