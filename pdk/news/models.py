# encoding:utf-8

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# 自动摘要引入
from django.utils.html import strip_tags


# Create your models here.
class Category_news(models.Model):
    Category_news_tit = models.CharField('栏目名称', max_length=20)
    Category_news_seo = models.CharField('SEO标题', max_length=100)
    Category_news_key = models.CharField('关键词', max_length=200)
    Category_news_des = models.TextField('栏目描述', max_length=200)
    index = models.IntegerField('分类的排序', default=999)

    def __str__(self):
        return self.Category_news_tit

    class Meta:
        verbose_name = u"新闻栏目"
        verbose_name_plural = u"新闻栏目"


class News_con(models.Model):
    title = models.CharField('新闻标题', max_length=100)
    keywords = models.CharField('关键词', max_length=200, blank=True)
    excerpt = models.TextField('摘要', max_length=200, blank=True, help_text='如未填写,则在内容中取60个字作为简介')
    thumbnail = models.ImageField('缩略图', upload_to='news/%Y/%m/', blank=True, default="215bg.png")
    category = models.ForeignKey(Category_news, on_delete=models.CASCADE, verbose_name='新闻分类')
    body = RichTextUploadingField()
    count = models.PositiveIntegerField('文章点击率', default=1)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"新闻详细"
        verbose_name_plural = u"新闻详细"

        # 增加阅读量
    def increase_count(self):
        self.count += 1
        self.save(update_fields=['count'])

        # 自动摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.body)[:100]
        super(News_con, self).save(*args, **kwargs)
