from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import News, NewsCategory
from django.db.models import Q

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = News.objects.filter(status='published')
        category_slug = self.kwargs.get('category_slug')
        search_query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(summary__icontains=search_query)
            )
        
        return queryset.order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        context['recent_news'] = News.objects.filter(
            status='published'
        ).order_by('-published_at')[:5]
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    query_pk_and_slug = True

    def get_queryset(self):
        return News.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_news'] = News.objects.filter(
            status='published'
        ).exclude(id=self.object.id).order_by('-published_at')[:5]
        return context
