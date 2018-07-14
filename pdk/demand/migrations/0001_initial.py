# Generated by Django 2.0 on 2018-07-10 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='demand_con',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('linkman', models.CharField(max_length=10, verbose_name='联系人')),
                ('tel', models.CharField(max_length=11, verbose_name='联系电话')),
                ('type', models.CharField(blank=True, max_length=50, verbose_name='选择栏目')),
                ('con_time', models.CharField(choices=[('随时联系', '随时联系'), ('8点-12点', '8点-12点'), ('12点-14点', '12点-14点'), ('14点-18点', '14点-18点'), ('18点-21点', '18点-21点')], max_length=20, verbose_name='联系我')),
                ('message', models.TextField(verbose_name='客户需求')),
                ('password', models.CharField(blank=True, default=15151515578, max_length=11, verbose_name='查询密码')),
                ('state', models.CharField(choices=[('未联系', '未联系'), ('已联系', '已联系'), ('待合作', '待合作'), ('已合作', '已合作'), ('拒绝', '拒接'), ('黑名单', '黑名单')], default='未联系', max_length=10, verbose_name='订单状态')),
                ('feedback', models.TextField(blank=True, verbose_name='顾问反馈信息')),
            ],
            options={
                'verbose_name': '需求',
                'verbose_name_plural': '需求',
            },
        ),
    ]
