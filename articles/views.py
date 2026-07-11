from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer
from django.db.models import Q

from .models import Article, Category, Comment
from .utils import paginate_queryset

def home(request):
    queryset = Article.objects.filter(is_published=True).select_related('category')
    articles = paginate_queryset(request, queryset, per_page=5)
    return render(request, "articles/home.html", {"articles": articles})


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('category'),
        slug=slug
    )
    return render(request, "articles/article_detail.html", {"article": article})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = Article.objects.filter(category=category, is_published=True).select_related('category')
    articles = paginate_queryset(request, queryset, per_page=5)
    return render(request, "articles/category_detail.html",
                  {"articles": articles, "category": category})


class CommentAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(
            article__slug=self.kwargs['slug']
        ).order_by('-created_at')

    def perform_create(self, serializer):
        article = get_object_or_404(
            Article,
            slug=self.kwargs['slug']
        )

        serializer.save(article=article)


def search_view(request):
    query = request.GET.get('q', '').strip()

    queryset = Article.objects.none()

    if query:
        queryset = Article.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    articles = paginate_queryset(request, queryset, per_page=5)

    return render(request, 'articles/search.html',
                  {
                      'articles': articles,
                      'query': query,
                  })

def health(request):
    return HttpResponse("OK", content_type="text/plain")