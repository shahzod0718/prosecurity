from .models import News,Category
from datetime import datetime
from django.shortcuts import render
def latest_news(request):
    latest_news=News.published.all().order_by('-publish_time')[:2]
    galery_news=News.published.all().order_by('-publish_time')[:9]
    categories=Category.objects.all()
    today = datetime.today()

    context={
        'latest_news':latest_news,
        'galery_news':galery_news,
        'categories':categories,
        'today': today,
        
    }
    return context






