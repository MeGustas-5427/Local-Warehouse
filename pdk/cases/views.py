from django.shortcuts import render

# Create your views here.
from main_ad.models import Carousel, Index_news, Index_banner_ad
from .models import Cases_con
from product.models import Category_pro, Category_pro_son, Category_pro_grandson
from unit.config import *
from unit.redis_connection import redis_result, redis_save_render_template
from unit.views import pagination_func, consultant_recommend, cases_recommend
from django.shortcuts import render, reverse
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.views.generic import View
from django.db import connection
from django.db.models import Prefetch


class ListCaseView(View):
    def get(self, request, *args, **kwargs):
        pro = request.GET.get("pro")
        page = int(request.GET.get('page', default=1))  # 当前页
        num = 20
        if pro:
            url = '/list_case/?pro=%s&page=%d' % (pro, page)
            result = redis_result(url)
            if result:
                return result
            ORM = Category_pro.objects.filter(id=pro).first()
            case_type = ORM.Category_pro_tit
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            cases = ORM.cases_con_set.filter(auditing='已审核').order_by('-id').all()

        else:
            url = '/list_case/?page=%d' % page
            result = redis_result(url)
            if result:
                return result
            case_type = None
            cases = Cases_con.objects.filter(auditing="已审核").order_by('-id').all()
            title = ""
            keywords = ""
            description = ""


        total = cases.count()

        start, end, pagination = pagination_func(page, num, total)

        posts = cases[start: end]

        # 案例分类
        category_cases = Category_pro.objects.order_by('index').all()

        # 优势案例推荐
        Cases_recommend = cases_recommend()

        # 优秀顾问推荐
        Consultant_recommend = consultant_recommend(4)

        context = {
            "posts": posts,
            "pagination": pagination,
            "category_cases": category_cases,
            "cases_recommend": Cases_recommend,
            "consultant_recommend": Consultant_recommend,
            "title": title or T_default,
            "keywords": keywords or K_default,
            "description": description or D_default,
            "case_type": case_type or "全部",
        }

        context.update(pagination)
        result = render(request, "cases/list_case.html", context=context)
        redis_save_render_template(url, result)
        return result


def detail_case(request):
    return HttpResponse('detail_case')