from django.shortcuts import render

# Create your views here.
from adviser.models import adviser_user
from cases.models import Cases_con
from django.db.models import Q
from django.contrib.auth.models import Group
import math

def consultant_recommend(num=5):
    # consultants = [i.id for i in Group.objects.filter(name="顾问").first().adviser_user.all()]
    # return adviser_user.objects.filter(Q(id__in=consultants)&Q(show='是'))\
    #     .order_by('-count_order').all()[:num+1]
    return adviser_user.objects.filter(Q(show='是')).order_by('-count_order').all()[:num]


def cases_recommend():
    return Cases_con.objects.filter(auditing='已审核').order_by('-count').all()[:2]


def pagination_func(page, num, total):
    start = num * (page - 1)
    end = num * page

    around_count = 2
    current_page = page
    num_pages = math.ceil(total / num)  # 总页数

    # 默认首页、尾页比当前页数字之差少于等于4，左右两边没有 "..."
    left_has_more = False
    right_has_more = False

    # 若当前页少于等于4，则没有'...'
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)

    # 若当前页大于等于总页数 - around_count - 1，则没有'...'
    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)

    pagination = {
        'left_pages': left_pages,  # 左边页范围 ps: 3、4
        'right_pages': right_pages,  # 右边页范围 ps: 6、7
        'current_page': current_page,  # 当前页 ps: 5
        'left_has_more': left_has_more,  # 左边是否显示'...'
        'right_has_more': right_has_more,  # 右边是否显示'...'
        'num_pages': num_pages  # 总页数
    }

    return start, end, pagination