# encoding:utf-8
from django.db import models
from adviser.models import adviser_user

from ckeditor_uploader.fields import RichTextUploadingField
# 自动摘要引入
from django.utils.html import strip_tags


# 产品栏目创建
class Category_pro(models.Model):
    Category_pro_tit = models.CharField('顶级分类标题', max_length=20)
    Category_pro_seo = models.CharField('SEO标题', max_length=20)
    Category_pro_key = models.CharField('关键词', max_length=200)
    Category_pro_des = models.TextField('栏目描述', max_length=200)
    index = models.IntegerField('分类的排序', default=999)

    def __str__(self):
        return self.Category_pro_tit

    class Meta:
        verbose_name = u"一级类"
        verbose_name_plural = verbose_name


# 二级类栏目创建


class Category_pro_son(models.Model):
    type = models.ManyToManyField(Category_pro, verbose_name="一级分类")
    Category_pro_tit = models.CharField('二级分类标题', max_length=20)
    Category_pro_seo = models.CharField('SEO标题', max_length=100)
    Category_pro_key = models.CharField('关键词', max_length=200)
    Category_pro_des = models.TextField('栏目描述', max_length=200)
    index = models.IntegerField('分类的排序', default=999)

    def __str__(self):
        return self.Category_pro_tit

    class Meta:
        verbose_name = u"二级类"
        verbose_name_plural = verbose_name


# 三级类栏目创建


class Category_pro_grandson(models.Model):
    type = models.ManyToManyField(Category_pro_son, verbose_name="二级分类")
    Category_pro_tit = models.CharField('三级分类标题', max_length=20)
    Category_pro_seo = models.CharField('SEO标题', max_length=100)
    Category_pro_key = models.CharField('关键词', max_length=200)
    Category_pro_des = models.TextField('栏目描述', max_length=200)
    index = models.IntegerField('分类的排序', default=999)

    def __str__(self):
        return self.Category_pro_tit

    class Meta:
        verbose_name = u"三级类"
        verbose_name_plural = verbose_name


# class Pro_question(models.Model):
#     ask = models.CharField('问', max_length=100)
#     answer = models.TextField('答', max_length=100)

#     def __str__(self):
#         return self.ask

#     class Meta:
#         verbose_name = u"常见问答"
#         verbose_name_plural = verbose_name


class Pro_question(models.Model):
    category = models.ForeignKey(Category_pro, on_delete=models.CASCADE, verbose_name='一级分类')
    category_son = models.ForeignKey(Category_pro_son, on_delete=models.CASCADE, verbose_name='二级分类', blank=True)
    category_grandson = models.ForeignKey(Category_pro_grandson, on_delete=models.CASCADE, verbose_name='三级分类',
                                          blank=True, null=True)
    ask = models.CharField('问', max_length=100)
    answer = models.TextField('答', max_length=300)

    def __str__(self):
        return self.ask

    class Meta:
        verbose_name = u"常见问答"
        verbose_name_plural = verbose_name


# 产品中心
class Pro_content(models.Model):
    title = models.CharField('产品名称', max_length=100)
    seo_title = models.CharField('SEO标题', max_length=100)
    keywords = models.CharField('关键词', max_length=200, blank=True)
    excerpt = models.TextField('摘要', max_length=200, blank=True, help_text='如未填写,则在内容中取60个字作为简介')
    price = models.IntegerField('产品价格')
    add_list = (
        ('全国', '全国'),

    )
    address = models.CharField('服务城市', choices=add_list, max_length=10, default='全国')
    thumbnail = models.ImageField('缩略图', upload_to='pro/%Y/%m/', blank=True, default="222bg.png",
                                  help_text="图片尺寸：390 * 344")
    category = models.ForeignKey(Category_pro, on_delete=models.CASCADE, verbose_name='一级分类')
    category_son = models.ForeignKey(Category_pro_son, on_delete=models.CASCADE, verbose_name='二级分类', blank=True)
    category_grandson = models.ForeignKey(Category_pro_grandson, on_delete=models.CASCADE, verbose_name='三级分类',
                                          blank=True, null=True)

    body = RichTextUploadingField('产品内容')
    relation = models.ManyToManyField('self', verbose_name='关联产品', blank=True)
    count = models.PositiveIntegerField('点击率', default=1)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    adviser = models.ManyToManyField(adviser_user, verbose_name='顾问', blank=True)
    question = models.ManyToManyField(Pro_question, verbose_name='常见问答', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"产品详细"
        verbose_name_plural = verbose_name

        # 增加阅读量

    def increase_count(self):
        self.count += 1
        self.save(update_fields=['count'])

        # 自动摘要

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.body)[:100]
        super(Pro_content, self).save(*args, **kwargs)
