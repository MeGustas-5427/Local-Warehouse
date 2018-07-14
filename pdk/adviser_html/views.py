from django.shortcuts import render

# Create your views here.
from main_ad.models import Carousel, Index_news, Index_banner_ad
from adviser.models import adviser_user
from product.models import Category_pro, Category_pro_son, Category_pro_grandson
from unit.config import *
from unit.redis_connection import redis_result, redis_save_render_template
from unit.views import pagination_func
from unit.views import consultant_recommend
from django.shortcuts import render, reverse
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.views.generic import View, TemplateView, ListView
from django.db import connection
from django.db.models import Prefetch
import math


class List_Adviser_View(View):
    def get(self, request, *args, **kwargs):
        pro = request.GET.get("pro")
        pro_son = request.GET.get("pro_son")
        pro_grandson = request.GET.get("pro_grandson")
        page = int(request.GET.get('page', default=1))  # 当前页
        num = 8
        is_pro = 0

        if pro:
            url = '/list_adviser/?pro=%s&page=%d' % (pro, page)
            result = redis_result(url)
            if result:
                return result

            ORM = Category_pro.objects.filter(id=pro).first()
            product = ORM.pro_content_set.all()
            consultant = list(set([j for i in product for j in i.adviser.all()]))
            total = len(consultant)
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            pro = "pro_%d" % ORM.id
            pro_son = ""
            pro_grandson = ""
            is_pro_son = 0
            is_pro_grandson = 0

        elif pro_son:
            url = '/list_adviser/?pro_son=%s&page=%d' % (pro_son, page)
            result = redis_result(url)
            if result:
                return result

            ORM = Category_pro_son.objects.filter(id=pro_son).first()
            #prefetch = Prefetch('pro_content_set', queryset=Category_pro_son.objects.filter(id=pro_son))
            #products = Category_pro.objects.prefetch_related('pro_content_set').all()
            #products = Category_pro.objects.prefetch_related(prefetch).all()
            product = ORM.pro_content_set.all()
            consultant = list(set([j for i in product for j in i.adviser.all()]))
            # consultant = []
            # for product in ORM.pro_content_set.all():
            #     product.
            #     consultant.append(i.pro_content_set.first().adviser.all())
            # consultant = list(set(consultant))

            total = len(consultant)
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
            print(connection.queries)

        elif pro_grandson:
            url = '/list_adviser/?pro_grandson=%s&page=%d' % (pro_grandson, page)
            result = redis_result(url)
            if result:
                return result
            ORM = Category_pro_grandson.objects.filter(id=pro_grandson).first()
            product = ORM.pro_content_set.all()
            consultant = list(set([j for i in product for j in i.adviser.all()]))
            total = len(consultant)
            title = ORM.Category_pro_seo + title_end
            keywords = ORM.Category_pro_key
            description = ORM.Category_pro_des
            pro = "pro_%d" % ORM.son[0].pro[0].id
            pro_son = "pro_son_%d" % ORM.son[0].id
            pro_grandson = "pro_grandson_%d" % ORM.id

            is_pro_son = 1
            is_pro_grandson = 1

        else:
            url = '/list_adviser/?page=%d' % page
            result = redis_result(url)
            if result:
                return result

            consultant = adviser_user.objects.filter(show='是').all()
            total = consultant.count()
            title = ""
            keywords = ""
            description = ""
            pro = "all-btn"
            is_pro = 1
            is_pro_son = 0
            is_pro_grandson = 0

        # 分页代码(开始) ================
        start, end, pagination = pagination_func(page, num, total)
        # 分页代码(结束) ================

        posts = consultant[start: end]

        # 分类
        category_pro = Category_pro.objects.order_by('index').all()
        category_pro_son = Category_pro_son.objects.order_by('index').all()

        current_namespace = request.resolver_match.namespace

        context = {
            "pro": pro,
            "pro_son": pro_son,
            "pro_grandson": pro_grandson,
            "is_pro": is_pro,
            "is_pro_son": is_pro_son,
            "is_pro_grandson": is_pro_grandson,
            "posts": posts,
            "pagination": pagination,
            "category_pro": category_pro,
            "category_pro_son": category_pro_son,
            "title": title or T_default,
            "keywords": keywords or K_default,
            "description": description or D_default,
            "url_for": reverse("%s:list_adviser" % current_namespace),
        }

        context.update(pagination)

        result = render(request, "adviser/list_adviser.html", context=context)
        redis_save_render_template(url, result)
        return result


"""
    pro = request.arg.get("pro")
    pro_son = request.arg.get("pro_son")
    pro_grandson = request.arg.get("pro_grandson")
    page = request.args.get(get_page_parameter(), type=int, default=1)
    num = 8
    is_pro = 0
    if pro:
        url = '/list_adviser/?pro=%s&page=%d' % (pro, page)
        result = redis_result(url)
        if result:
            return result

        ORM = Category_pro.query.filter_by(id=pro).first()
        product = ORM.pro_content
        consultant = list(set([j for i in product for j in i.adviser]))
        total = len(consultant)
        title = ORM.Category_pro_seo + title_end
        keywords = ORM.Category_pro_key
        description = ORM.Category_pro_des
        pro = "pro_%d" % ORM.id
        pro_son = ""
        pro_grandson = ""
        is_pro_son = 0
        is_pro_grandson = 0

    elif pro_son:
        url = '/list_adviser/?pro_son=%s&page=%d' % (pro_son, page)
        result = redis_result(url)
        if result:
            return result

        ORM = Category_pro_son.query.filter_by(id=pro_son).first()
        product = ORM.pro_content
        consultant = list(set([j for i in product for j in i.adviser]))
        total = len(consultant)
        title = ORM.Category_pro_seo + title_end
        keywords = ORM.Category_pro_key
        description = ORM.Category_pro_des
        pro = "pro_%d" % ORM.pro[0].id
        pro_son = "pro_son_%d" % ORM.id
        pro_grandson = ORM.pro_grandson
        is_pro_son = 1
        is_pro_grandson = 0

        if pro_grandson:
            is_pro_grandson = 2
        pro_grandson = "AAAA"

    elif pro_grandson:
        url = '/list_adviser/?pro_grandson=%s&page=%d' % (pro_grandson, page)
        result = redis_result(url)
        if result:
            return result
        ORM = Category_pro_grandson.query.filter_by(id=pro_grandson).first()
        product = ORM.pro_content
        consultant = list(set([j for i in product for j in i.adviser]))
        total = len(consultant)
        title = ORM.Category_pro_seo + title_end
        keywords = ORM.Category_pro_key
        description = ORM.Category_pro_des
        pro = "pro_%d" % ORM.son[0].pro[0].id
        pro_son = "pro_son_%d" % ORM.son[0].id
        pro_grandson = "pro_grandson_%d" % ORM.id

        is_pro_son = 1
        is_pro_grandson = 1

    else:
        url = '/list_adviser/?page=%d' % page
        result = redis_result(url)
        if result:
            return result

        consultant = Auth_Group.query.filter_by(name="顾问").first().adviser_user.filter_by(show='是').all()
        total = len(consultant)
        title = ""
        keywords = ""
        description = ""
        pro = "all-btn"
        is_pro = 1
        is_pro_son = 0
        is_pro_grandson = 0

    total_page = math.ceil(total / num) * 10
    start = num * (page - 1)
    end = num * page

    posts = consultant[start: end]

    # 可能是pagination的bug，如果总页数是8页，那么total要==80
    pagination = Pagination(bs_version=3, page=page, total=total_page, outer_window=0, inner_window=2)

    # 分类
    category_pro = Category_pro.query.order_by(Category_pro.index).all()
    category_pro_son = Category_pro_son.query.order_by(Category_pro_son.index).all()

    context = {
        "pro": pro,
        "pro_son": pro_son,
        "pro_grandson": pro_grandson,
        "is_pro": is_pro,
        "is_pro_son": is_pro_son,
        "is_pro_grandson": is_pro_grandson,
        "posts": posts,
        "pagination": pagination,
        "category_pro": category_pro,
        "category_pro_son": category_pro_son,
        "title": title or T_default,
        "keywords": keywords or K_default,
        "description": description or D_default,
    }
    # print(posts[0].name) 测试成功
    #result = render_template("list_adviser.html", **context)
    #redis_save_render_template(url, result)
    #return result
"""


def article_adviser(request):
    return HttpResponse('article_adviser')