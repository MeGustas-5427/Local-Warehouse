# encoding:utf-8
from django.db import models
from product.models import Category_pro, Category_pro_son, Category_pro_grandson


class Carousel(models.Model):
    name = models.CharField('广告名', max_length=100)
    url = models.URLField('广告地址')
    thumbnail = models.ImageField('广告图', upload_to='ad/%Y/%m/', blank=True, help_text="轮播图尺寸：980 * 518")
    index = models.IntegerField('广告排序', default=999)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"首页轮播"
        verbose_name_plural = verbose_name


class Index_news(models.Model):
    name = models.CharField('广告名', max_length=100)
    url = models.URLField('广告地址')
    thumbnail = models.ImageField('广告图', upload_to='ad_news/%Y/%m/', blank=True, help_text="图片尺寸：980 * 518")
    index = models.IntegerField('广告排序', default=999, help_text="数值越大越靠后")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"底部轮播"
        verbose_name_plural = verbose_name


class Main_banner(models.Model):
    category = models.ManyToManyField(Category_pro, verbose_name='一级分类')
    category_son = models.ManyToManyField(Category_pro_son, verbose_name='二级分类', blank=True)
    category_grandson = models.ManyToManyField(Category_pro_grandson, verbose_name='三级分类', blank=True)
    name = models.CharField('广告名', max_length=100)
    url = models.URLField('广告地址')
    thumbnail = models.ImageField('广告图', upload_to='ad_news/%Y/%m/', blank=True, help_text="图片宽度：1190px，高度不限")
    index = models.IntegerField('广告排序', default=999, help_text="数值越大越靠后")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"产品列表"
        verbose_name_plural = verbose_name


class Menu_nav_ad(models.Model):
    category = models.ForeignKey(Category_pro, on_delete=models.CASCADE, verbose_name='一级分类')
    type_data = (
        ('左侧大图', '左侧大图'),
        ('右侧小图', '右侧小图'),
    )
    type = models.CharField('图片类型', choices=type_data, max_length=10)
    name = models.CharField('广告名', max_length=100)
    url = models.URLField('广告地址')
    thumbnail = models.ImageField('广告图', upload_to='ad_news/%Y/%m/', blank=True, help_text="小图尺寸：宽250px、大图尺寸：宽657px，高度不限")
    index = models.IntegerField('广告排序', default=999, help_text="数值越大越靠后")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"导航广告"
        verbose_name_plural = verbose_name


class Index_banner_ad(models.Model):
    name = models.CharField('广告名', max_length=100)
    url = models.URLField('广告地址')
    thumbnail = models.ImageField('广告图', upload_to='ad_news/%Y/%m/', blank=True,
                                  help_text="宽度1190，高度不限")
    index = models.IntegerField('广告排序', default=999, help_text="数值越大越靠后")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"首页广告"
        verbose_name_plural = verbose_name
