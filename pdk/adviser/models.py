# encoding:utf-8
from django.db import models
from django.contrib.auth.hashers import make_password
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser


class adviser_user(AbstractUser):
    tel = models.CharField('联系电话', max_length=11, blank=True, null=True)
    thumbnail = models.ImageField('头像', upload_to='adviser_user/%Y/%m/', blank=True, default="100user.png",help_text="图片尺寸：180 * 180")
    profession = models.CharField('职位',max_length=30,help_text='请输入小于15个字的职位介绍',default="跑得快企服超市商务")
    serve = models.CharField('服务范围',max_length=30,help_text='请输入小于40个字的服务范围',default="跑得快,助推企业跑得更快")
    excerpt = models.TextField('简要介绍', max_length=200, help_text='请务必填写', blank=True, null=True)
    body = RichTextUploadingField('个人介绍')
    count_con = models.PositiveIntegerField('咨询量', default=1)
    count_order = models.PositiveIntegerField('下单量', default=1)

    #新增字段
    superior = models.CharField('上级', max_length=11, default=1)
    department = models.CharField('部门',max_length=200,blank=True,default="空")
    position = models.CharField('职位', max_length=200, blank=True, default="空")


    seo_title = models.CharField('SEO标题', max_length=100, blank=True)
    keywords = models.CharField('关键词', max_length=100, blank=True)

    show_list = (
        ('否', '不显示'),
        ('是', '显示'),
    )
    show = models.CharField('是否显示顾问', choices=show_list, max_length=10, default='否')

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        verbose_name = u"用户"
        verbose_name_plural = verbose_name
