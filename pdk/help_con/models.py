# encoding:utf-8

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Category_help(models.Model):
    Category_tit = models.CharField('帮助栏目',max_length=20)
    Category_seo = models.CharField('SEO标题',max_length=100)
    Category_key = models.CharField('关键词', max_length=200)
    Category_des = models.TextField('栏目描述', max_length=200)
    index = models.IntegerField('分类的排序', default=999)

    def __str__(self):
        return self.Category_tit

    class Meta:
        verbose_name = u"帮助栏目"
        verbose_name_plural = verbose_name

class Help_con(models.Model):
    title = models.CharField('帮助标题', max_length=100)
    category = models.ForeignKey(Category_help,on_delete=models.CASCADE,verbose_name='帮助分类')
    body = RichTextUploadingField()
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    modified_time = models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"帮助内容"
        verbose_name_plural = verbose_name


#投诉与建议
class Help_sug(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    name = models.CharField('联系人',max_length=100)
    tel =models.CharField('联系电话',max_length=100)
    email=models.CharField('邮箱',max_length=100)
    help_type_list=(
        ('投诉', '投诉'),
        ('建议', '建议'),
    )
    help_type=models.CharField('类型',choices=help_type_list,max_length=10)
    help_con = RichTextUploadingField('投诉内容')
    state_list=(
        ('未处理', '未处理'),
        ('已处理', '已处理'),
    )
    state =models.CharField('状态',choices=state_list,max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"投诉与建议"
        verbose_name_plural = verbose_name
