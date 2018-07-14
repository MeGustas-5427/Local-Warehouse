# encoding:utf-8
from django.db import models

# Create your models here.


class demand_con(models.Model):
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    linkman = models.CharField('联系人', max_length=10)

    tel = models.CharField('联系电话', max_length=11)
    type = models.CharField('选择栏目', max_length=50, blank=True)
    con_time_list =(
        ('随时联系', '随时联系'),
        ('8点-12点', '8点-12点'),
        ('12点-14点', '12点-14点'),
        ('14点-18点', '14点-18点'),
        ('18点-21点', '18点-21点'),
    )
    con_time = models.CharField('联系我',choices=con_time_list,max_length=20)
    message = models.TextField('客户需求')
    password = models.CharField('查询密码', max_length=11, default=15151515578, blank=True)
    state_data = (
        ('未联系', '未联系'),
        ('已联系', '已联系'),
        ('待合作', '待合作'),
        ('已合作', '已合作'),
        ('拒绝', '拒接'),
        ('黑名单', '黑名单')
    )
    state = models.CharField('订单状态', choices=state_data, max_length=10,default="未联系")
    feedback = models.TextField('顾问反馈信息', blank=True)

    # 短信回复：订单状态 + 顾问反馈信息 + 需求单号（pdk801 + ID值） + 查询密码，

    def __str__(self):
        return self.linkman

    class Meta:
        verbose_name = u"需求"
        verbose_name_plural = verbose_name
