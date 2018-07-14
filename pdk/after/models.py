# encoding:utf-8

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from adviser.models import adviser_user
from product.models import (Category_pro, Category_pro_grandson,
                            Category_pro_son, Pro_content)

# Create your models here.


class tema(models.Model):
    tit = models.CharField('售后组名称',max_length=50,default="售后组名称")
    des = models.TextField('售后组描述',default="售后组描述")
    category = models.ManyToManyField(Category_pro, verbose_name='顶级分类')
    category_son = models.ManyToManyField(Category_pro_son,  verbose_name='二级分类')
    category_grandson = models.ManyToManyField(Category_pro_grandson,  verbose_name='三级分类', blank=True)
    pro = models.ManyToManyField(Pro_content, verbose_name='产品', blank=True)
    name = models.ManyToManyField(adviser_user, verbose_name='团队', blank=True)

    def __str__(self):
        return self.tit

    class Meta:
        verbose_name = u"售后服务"
        verbose_name_plural = verbose_name


class line_tema(models.Model):
    tit = models.CharField('售后组名称', max_length=50, default="售后组名称")
    des = models.TextField('售后组描述', default="售后组描述")
    category = models.ManyToManyField(Category_pro, verbose_name='顶级分类')
    category_son = models.ManyToManyField(Category_pro_son, verbose_name='二级分类')
    category_grandson = models.ManyToManyField(Category_pro_grandson, verbose_name='三级分类', blank=True)
    pro = models.ManyToManyField(Pro_content, verbose_name='产品', blank=True)
    body = RichTextUploadingField('在线客服')

    def __str__(self):
        return self.tit

    class Meta:
        verbose_name = u"在线客服"
        verbose_name_plural = verbose_name


class after_ask(models.Model):
    category = models.ManyToManyField(Category_pro, verbose_name='顶级分类')
    category_son = models.ManyToManyField(Category_pro_son,  verbose_name='二级分类')
    category_grandson = models.ManyToManyField(Category_pro_grandson,  verbose_name='三级分类', blank=True)
    pro = models.ManyToManyField(Pro_content, verbose_name='产品', blank=True)
    ask = models.CharField('问', max_length=100)
    answer = models.TextField('答', max_length=300)

    def __str__(self):
        return self.ask

    class Meta:
        verbose_name = u"售后常见问题"
        verbose_name_plural = verbose_name
