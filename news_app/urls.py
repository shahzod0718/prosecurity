from django.urls import path
from .views import news_list,news_detail,homePageView,contactPageView,error404PageView\
,sportPageView,mahalliyPageView,texnologiyaPageView,xorijPageView,ShouBiznesPageView,SearchResultsList


urlpatterns=[
    path('',homePageView,name='home_page'),
    path('news/',news_list,name='all_news_list'),
    path('news/<slug:news>/',news_detail,name='news_detail_page'),
    path('contact-us/',contactPageView,name='contact_page'),
    path('page-404',error404PageView,name='error404_page'),
    path('mahalliy/',mahalliyPageView,name='mahalliy_page'),
    path('sport/',sportPageView,name='sport_page'),
    path('texnologiya',texnologiyaPageView,name='texnologiya_page'),
    path('xorij/',xorijPageView,name='xorij_page'),
    path('shou-biznes/',ShouBiznesPageView,name='shou_biznes_page'),
    path('searchresult',SearchResultsList.as_view(),name='search_results'),

]
