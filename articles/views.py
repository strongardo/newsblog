from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "articles/home.html")

def article_detail(request, slug):
    return render(request, "articles/article_detail.html")

def category_detail(request, slug):
    return render(request, "articles/category_detail.html")
