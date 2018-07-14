# encoding:utf-8

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from adviser.models import adviser_user
from product.models import Category_pro, Category_pro_son, Category_pro_grandson, Pro_content
# Create your models here.


class Cases_con(models.Model):
    title = models.CharField('案例标题', max_length=100,help_text="公司名 - 服务项目，例：苏州企优托信息科技有限公司 - 工商注册")
    keywords = models.CharField('关键词', max_length=200, help_text="每个关键词之前使用英文逗号区分，即：跑得快,企优托,一网推")
    thumbnail = models.ImageField('企业LOGO', upload_to='cases/%Y/%m/', default="215bg.png",help_text="尺寸宽：120px，高：70px")
    category = models.ForeignKey(Category_pro, on_delete=models.CASCADE, verbose_name='顶级分类')
    category_son = models.ForeignKey(Category_pro_son, on_delete=models.CASCADE, verbose_name='二级分类',help_text="请认真选择栏目")
    category_grandson = models.ForeignKey(Category_pro_grandson, on_delete=models.CASCADE, verbose_name='三级分类',blank=True,help_text="请认真选择栏目")
    pro = models.ManyToManyField(Pro_content, verbose_name='关联产品',help_text="仅支持单个产品")
    uptime = models.DateField('项目上线时间',auto_now_add=False)
    hangye = models.CharField('所属行业',max_length=50)
    corporate_nane = models.CharField('公司名称',max_length=50)
    url= models.URLField('公司网址',help_text="网址需要输入http://或https://")
    pro_one = models.CharField('主推产品1',max_length=20)
    pro_one_url =models.URLField('主推产品1链接',help_text="网址需要输入http://或https://")
    pro_two = models.CharField('主推产品2', max_length=20)
    pro_two_url = models.URLField('主推产品2链接',help_text="网址需要输入http://或https://")
    pro_three = models.CharField('主推产品3', max_length=20)
    pro_three_url = models.URLField('主推产品3链接',help_text="网址需要输入http://或https://")
    pro_four = models.CharField('主推产品4', max_length=20,blank=True)
    pro_four_url = models.URLField('主推产品4链接',help_text="网址需要输入http://或https://",blank=True)
    pro_five = models.CharField('主推产品5', max_length=20,blank=True)
    pro_five_url = models.URLField('主推产品5链接',help_text="网址需要输入http://或https://",blank=True)
    excerpt = models.TextField('公司介绍', max_length=200)
    body = RichTextUploadingField('项目展示')
    data = RichTextUploadingField('数据展示')
    count = models.PositiveIntegerField('文章点击率', default=1)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    auditing_list = (
        ('未审核', '未审核'),
        ('未通过', '未通过'),
        ('已审核', '已审核'),
    )
    auditing = models.CharField('文章状态', choices=auditing_list, max_length=10, default='未审核')
    adviser = models.ForeignKey(adviser_user, verbose_name='顾问', blank=True, null=True, on_delete=models.CASCADE)
    index_show = models.BooleanField('是否首页推荐',default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"案例详细"
        verbose_name_plural = verbose_name

    def increase_count(self):
        self.count += 1
        self.save(update_fields=['count'])

