from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello, world. You're at the articles list page.")

def article_detail(request, slug):
    return HttpResponse("Hello, world. You're at the article detail page.")

def category_detail(request, slug):
    return HttpResponse("Hello, world. You're at the category detail page.")
