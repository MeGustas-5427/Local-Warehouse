from django.shortcuts import render

# Create your views here.
from main_ad.models import Carousel, Index_news, Index_banner_ad
from .models import Pro_content
from product.models import Category_pro, Category_pro_son, Category_pro_grandson
from unit.config import *
from unit.redis_connection import redis_result, redis_save_render_template
from unit.views import pagination_func
from unit.views import consultant_recommend
from django.shortcuts import render, reverse
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.views.generic import View
from django.db import connection
from django.db.models import Prefetch


class ListProductView(View):
    def get(self, request, *args, **kwargs):
        pro = request.GET.get("pro")
        pro_son = request.GET.get("pro_son")
        pro_grandson = request.GET.get("pro_grandson")
        page = int(request.GET.get('page', default=1))  # 当前页
        num = 20
        is_pro = 0

        if pro:
            url = '/list_product/?pro=%s&page=%d' % (pro, page)
            result = redis_result(url)
            if result:
                return result

            ORM = Category_pro.objects.filter(id=pro).first()
            banner = ORM.main_banner_set.all()
            product = ORM.pro_content_set.all()
            total = product.count()
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            pro = "pro_%d" % ORM.id
            pro_son = ""
            pro_grandson = ""
            is_pro_son = 0
            is_pro_grandson = 0

        elif pro_son:
            url = '/list_product/?pro_son=%s&page=%d' % (pro_son, page)
            result = redis_result(url)
            if result:
                return result

            ORM = Category_pro_son.objects.filter(id=pro_son).first()
            banner = ORM.main_banner_set.all()
            product = ORM.pro_content_set.all()
            total = product.count()
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            pro = "pro_%d" % ORM.type.all()[0].id
            pro_son = "pro_son_%d" % ORM.id
            pro_grandson = ORM.category_pro_grandson_set.all()
            is_pro_son = 1
            is_pro_grandson = 0

            if pro_grandson:
                is_pro_grandson = 2
            pro_grandson = "AAAA"

        elif pro_grandson:
            url = '/list_product/?pro_grandson=%s&page=%d' % (pro_grandson, page)
            result = redis_result(url)
            if result:
                return result

            ORM = Category_pro_grandson.objects.filter(id=pro_grandson).first()
            banner = ORM.main_banner_set.all()
            product = ORM.pro_content_set.all()
            total = product.count()
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            pro = "pro_%d" % ORM.type.all()[0].type.all()[0].id
            pro_son = "pro_son_%d" % ORM.type.all()[0].id
            pro_grandson = "pro_grandson_%d" % ORM.id
            is_pro = 0
            is_pro_son = 1
            is_pro_grandson = 1

        else:
            url = '/list_product/?page=%d' % page
            result = redis_result(url)
            if result:
                return result
            product = Pro_content.objects.all()
            banner = ""
            total = product.count()
            title = ""
            keywords = ""
            description = ""
            pro = "all-btn"
            is_pro = 1
            is_pro_son = 0
            is_pro_grandson = 0

        start, end, pagination = pagination_func(page, num, total)

        if pro or pro_son or pro_grandson:
            posts = product[start: end]
        else:
            posts = Pro_content.objects.slice(start, end)


        category_pro = Category_pro.objects.order_by('index').all()
        category_pro_son = Category_pro_son.objects.order_by('index').all()

        recommends = Pro_content.objects.order_by('-price').all()[:5]

        context = {
            "pro": pro,
            "pro_son": pro_son or "AAAA",
            "pro_grandson": pro_grandson or "AAAA",
            "is_pro": is_pro,
            "is_pro_son": is_pro_son,
            "is_pro_grandson": is_pro_grandson,
            "posts": posts,
            'category_pro': category_pro,
            'category_pro_son': category_pro_son,
            'recommends': recommends,
            "title": title or T_default,
            "keywords": keywords or K_default,
            "description": description or D_default,
            "banner": banner,
        }

        context.update(pagination)
        result = render(request, "product/list_product.html", context=context)
        redis_save_render_template(url, result)
        return result


def detail_product(request):
    return HttpResponse("detail_product")