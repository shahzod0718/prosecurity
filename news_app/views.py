from django.shortcuts import render,get_object_or_404,redirect
from .models import News,Category
from .forms import ContactForm,CommentForm
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.contrib.contenttypes.models import ContentType
from hitcount.models import HitCount


# Create your views here.

def news_list(request):
    news_list=News.published.all()
    context={
        'news_list':news_list,
    }

    return render(request,'news/news_list.html',context)





# def news_detail(request,news):
#     news=get_object_or_404(News,slug=news,status=News.Status.Published)
#     context={}
#     hit_count=get_hitcount_model().objects.get_for_object(news)
#     hits=hit_count.hits
#     hitcontext = context['hitcount'] = {'pk':hit_count.pk}
#     hit_count_response=HitCountMixin.hit_count(request,hit_count)
#     if hit_count_response.hit_counted:
#         hits=hits+1
#         hitcontext['hit_counted']=hit_count_response.hit_counted
#         hitcontext['hit_message']=hit_count_response.hit_message
#         hitcontext['total_hits']=hits
    

#     comments=news.comments.filter(active=True)
#     new_comment=None
#     if request.method =="POST":
#         comment_form=CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             # yangi komment obyektini yaratamiz lekin malumotlar bazasiga saqlamaymiz
#             new_comment = comment_form.save(commit=False)
#             new_comment.news=news
#             #izoh egasini surov yuborayotgan userga bogladik
#             new_comment.user=request.user
#             #malumotlar bazasiga saqlaymiz
#             new_comment.save()
#             comment_form=CommentForm()
#             return redirect('news_detail_page', news=news.slug)
#     else:
#         comment_form=CommentForm()
#     context={
        
#         'news':news,
#         'comments':comments,
#         'new_comment':new_comment,
#         'comment_form':comment_form,

#     }
#     return render(request,'news/news_detail.html',context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}

    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}

    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message

    hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    new_comment = None
    comment_count = comments.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            return redirect('news_detail_page', news=news.slug)
    else:
        comment_form = CommentForm()

    context.update({
        'news': news,
        'comments': comments,
        'comment_count':comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
        

    })

    return render(request, 'news/news_detail.html', context)





def homePageView(request):
    categories=Category.objects.all()
    news_one=News.published.order_by('-publish_time')[:1]
    news_two=News.published.order_by('-publish_time')[1:2]
    news_list=News.published.all().order_by('-publish_time')[2:6]

    local_one=News.published.filter(category__name='mahalliy').order_by('-publish_time')[:1]
    local_news=News.published.all().filter(category__name='mahalliy').order_by('-publish_time')[1:6]
    
    sport_one=News.published.filter(category__name='sport').order_by('-publish_time')[:1]
    sport_news=News.published.all().filter(category__name='sport').order_by('-publish_time')[1:6]
    

    xorij_one=News.published.filter(category__name='xorij').order_by('-publish_time')[:1]
    xorij_news=News.published.all().filter(category__name='xorij').order_by('-publish_time')[1:6]


    techno_one=News.published.filter(category__name='texnologiya').order_by('-publish_time')[:1]
    techno_news=News.published.all().filter(category__name='texnologiya').order_by('-publish_time')[1:6]

    shou_biznes=News.published.filter(category__name='shouBiznes').order_by('-publish_time')[:2]



    news_ct = ContentType.objects.get_for_model(News)
    # Eng ko‘p ko‘rilgan yangiliklarni HitCount bo‘yicha olish
    top_hits = HitCount.objects.filter(content_type=news_ct).order_by('-hits')[:1]  # eng ko‘p 5ta
    most_viewed_news_list = [hit.content_object for hit in top_hits if hit.content_object is not None]


    
    

    context={
        'news_list':news_list,
        'news_one':news_one,
        'news_two':news_two,
        'categories':categories,
        'local_one':local_one,
        'local_news':local_news,
        'sport_one':sport_one,
        'sport_news':sport_news,
        'xorij_one':xorij_one,
        'xorij_news':xorij_news,
        "techno_one":techno_one,
        'techno_news':techno_news,
        'shou_biznes':shou_biznes,
        'most_viewed_news_list': most_viewed_news_list,
        
    
    }
    return render(request,'news/home.html',context)

def sportPageView(request):
    sport_news=News.published.all().filter(category__name='sport').order_by('-publish_time')
    context={
        "sport_news":sport_news,
    }
    return render(request,'news/sport.html',context)



def mahalliyPageView(request):
    mahalliy_news=News.published.all().filter(category__name='mahalliy').order_by('-publish_time')
    context={
        "mahalliy_news":mahalliy_news,
    }
    return render(request,'news/mahalliy.html',context)


def xorijPageView(request):
    xorij_news=News.published.all().filter(category__name='xorij').order_by('-publish_time')

    context={
        "xorij_news":xorij_news,
    }
    return render(request,'news/xorij.html',context)



def texnologiyaPageView(request):
    texnologiya_news=News.published.all().filter(category__name='texnologiya').order_by('-publish_time')

    context={
        "texnologiya_news":texnologiya_news,
    }
    return render(request,'news/texnologiya.html',context)



def ShouBiznesPageView(request):
    shou_news=News.published.all().filter(category__name='shouBiznes').order_by('-publish_time')

    context={
        "shou_news":shou_news,
    }
    
    return render(request,'news/shou-biznes.html',context)






class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) |Q(body__icontains=query)

        )









def contactPageView(request):
    
    form =ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("biz bilan boglanganingiz uchun raxmat")
    context = {
        'form':form
    }
    return render(request,'news/contact.html',context)


def error404PageView(request):
    context={

    }
    return render(request,'news/404.html',context)











