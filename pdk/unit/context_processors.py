#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from help_con.models import Help_con
from product.models import Category_pro


def ServiceProduct_dict_fuc(model=Category_pro):
    """
    :param model: 参数指定使用ServiceProduct模型
    :return: service_dict字典结构：{service_division:{service_type:[service],
                                                    service_type:[service],
                                                    ...
                                                    },
                                   ...
                                   }
    """
    division = model.objects.order_by('index').all()

    service_dict = {}
    for category_pro in division:
        category_pro_tit = category_pro.Category_pro_tit # 顶类
        List = category_pro.category_pro_son_set.all()
        if List:
            service_dict[category_pro_tit] = {}
            for category_pro_son in List:
                pro_son_tit = category_pro_son.Category_pro_tit
                service_dict[category_pro_tit][pro_son_tit] = category_pro_son.pro_content_set.all()
        else:
            service_dict.setdefault("其他", {})
            service_dict['其他'][category_pro_tit] = category_pro.pro_content_set.all()

    return service_dict


def base_context(request):
    ServiceProduct_dict = ServiceProduct_dict_fuc()
    help_con = Help_con.objects.all()

    advertising = {}
    for pro in Category_pro.objects.all():
        advertising['id_%d' % pro.id] = {'左侧大图': [], '右侧小图': []}
        for ad in pro.menu_nav_ad_set.all():
            advertising['id_%d' % pro.id][ad.type].append(ad)

    advertising.update({
        "service_dict": ServiceProduct_dict,
        "help_con": [help_con[:3], help_con[3:6], help_con[6:9], help_con[9:]],
    })

    return advertising


