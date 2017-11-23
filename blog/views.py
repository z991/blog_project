#coding:utf8
import logging
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from models import *


logger=logging.getLogger('blog.views')
# Create your views here.
def global_setting(request):
    return {'SITE_NAME':settings.SITE_NAME,
            'SITE_DESC':settings.SITE_DESC,}



def index(request):
    try:
        #分类信息获取（导航数据）
        category_list=Category.objects.all()[:3]
        #广告数据
        ad_list=Ad.objects.all()[0:4]
        #最新文章数据
        article_list=Article.objects.all()
        paginator=Paginator(article_list,10)
        try:
            page=int(request.GET.get('page',1))
            article_list=paginator.page(page)
        except (EmptyPage,InvalidPage,PageNotAnInteger):
            article_list = paginator.page(1)
        #文章归档
        #先获取文章中有的年份-月份
        archive_list= Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    return render(request,'index.html',locals())

#归档
def archive(request):
    try:
        #先获取客户端提交的信息
        category_list = Category.objects.all()[:3]
        # 广告数据
        ad_list = Ad.objects.all()[0:4]
        year=request.GET.get('year',None)
        month=request.GET.get('month',None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        paginator = Paginator(article_list, 2)
        archive_list = Article.objects.distinct_date()
        try:
            page = int(request.GET.get('page', 1))
            article_list = paginator.page(page)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            article_list = paginator.page(1)
    except Exception as e:
        logger.error(e)
    return render(request,'archive.html',locals())