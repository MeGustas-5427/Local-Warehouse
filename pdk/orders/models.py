from django.db import models
from product.models import Pro_content
from adviser.models import adviser_user
# Create your models here.


# 订单中心
class Pro_order(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    pro_title = models.ForeignKey(Pro_content, verbose_name='产品名称', on_delete=models.CASCADE)
    linkman = models.CharField('联系人', max_length=10)
    tel = models.CharField('联系电话', max_length=11)
    state_data = (
        ('未联系', '未联系'),
        ('已联系', '已联系'),
        ('待合作', '待合作'),
        ('已合作', '已合作'),
        ('拒绝', '拒接'),
        ('黑名单', '黑名单')
    )
    state = models.CharField('订单状态', choices=state_data, max_length=10, default="未联系")
    user = models.ForeignKey(adviser_user, verbose_name='订单顾问', on_delete=models.CASCADE)
    des = models.TextField('订单备注')

    def 产品名称(self):
        if self.pro_title is None:
            return "未获取到产品名"
        return self.pro_title
    产品名称.admin_order_field = "pro_title"

    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name


class Pro_call(models.Model):
    consultant = models.ForeignKey(adviser_user, verbose_name='顾问', on_delete=models.CASCADE, blank=True, null=True)
    contacts = models.CharField('联系人', max_length=50)
    telephone = models.CharField('联系电话', max_length=11)
    pro_title = models.ForeignKey(Pro_content, verbose_name='产品名称', on_delete=models.CASCADE, blank=True, null=True)
    desc = models.TextField('备注说明', blank=True)
    state_data = (
        ('未联系', '未联系'),
        ('已联系', '已联系'),
        ('待合作', '待合作'),
        ('已合作', '已合作'),
        ('拒绝', '拒接'),
        ('黑名单', '黑名单')
    )
    state = models.CharField('订单状态', choices=state_data, max_length=10, default="未联系")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    is_display = models.BooleanField('是否黑名单', default=False)

    def 产品名称(self):
        if self.pro_title is None:
            return "未获取到产品名"
        return self.pro_title
    产品名称.admin_order_field = "pro_title"

    class Meta:
        verbose_name = u"咨询"
        verbose_name_plural = verbose_name
