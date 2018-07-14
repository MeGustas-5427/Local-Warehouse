from django.shortcuts import render

# Create your views here.

from main_ad.models import Carousel, Index_news, Index_banner_ad
from cases.models import Cases_con
from unit.config import *
from unit.redis_connection import redis_result, redis_save_render_template
from unit.views import consultant_recommend
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponse


@require_GET
def index(request):
    result = redis_result("index/")
    if result:
        return result

    carousel = Carousel.objects.order_by('index').all()

    # 顾问推荐
    adviser_user = consultant_recommend(9)

    # 企优托案例轮播图
    carouselnews = Index_news.objects.order_by('index').all()

    # 企优托案例
    cases = Cases_con.objects.filter(auditing='已审核', index_show=1).order_by('-id').all()[:12]

    # 首页三个banner广告
    banner = Index_banner_ad.objects.order_by('index').all()[:3]

    context = {
        "title": T_default,
        "keywords": K_default,
        "description": D_default,
        "carousel": carousel,
        "carouselnews": carouselnews,
        "cases": cases,
        "adviser_user": adviser_user,
        "banner": banner or [{"url":""}, {"url":""}, {"url":""}],
    }

    result = render(request, 'index.html', context=context)
    redis_save_render_template("index/", result)
    return result



"""
    result = redis_result("/")
    if result:
        return result

    carousel = Carousel.query.order_by(Carousel.index).all()
    # 顾问推荐
    adviser_user = consultant_recommend(9)

    # 企优托案例轮播图
    carouselnews = CarouselNews.query.order_by(CarouselNews.index).all()

    # 企优托案例
    cases = Cases_con.query.filter_by(auditing='已审核', index_show=1).order_by(Cases_con.id.desc()).limit(12).all()

    # 首页三个banner广告
    banner = Index_banner_ad.query.order_by(Index_banner_ad.index).limit(3).all()

    context = {
        "title": T_default,
        "keywords": K_default,
        "description": D_default,
        "carousel": carousel,
        "carouselnews": carouselnews,
        "cases": cases,
        "adviser_user": adviser_user,
        "banner": banner or [{"url":""}, {"url":""}, {"url":""}],
    }

    result = render_template("index.html", **context)
    redis_save_render_template("/",result)
    return result
"""