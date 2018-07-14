# encoding:utf-8

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class SpecialSubject(models.Model):
    title = models.CharField('专题标题',max_length=100)
    seo_title = models.CharField('SEO标题', max_length=100)
    keywords = models.CharField('关键词', max_length=200, blank=True)
    excerpt = models.TextField('摘要', max_length=200, blank=True, help_text='如未填写,则在内容中取60个字作为简介')
    thumbnail = models.ImageField('缩略图', upload_to='topic/%Y/%m/', blank=True, default="215bg.png")
    body = RichTextUploadingField('专题内容')
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    modified_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"专题管理"
        verbose_name_plural = u"专题管理"
