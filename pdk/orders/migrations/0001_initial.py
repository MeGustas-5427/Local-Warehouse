# Generated by Django 2.0 on 2018-07-10 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pro_call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacts', models.CharField(max_length=50, verbose_name='联系人')),
                ('telephone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('desc', models.TextField(blank=True, verbose_name='备注说明')),
                ('state', models.CharField(choices=[('未联系', '未联系'), ('已联系', '已联系'), ('待合作', '待合作'), ('已合作', '已合作'), ('拒绝', '拒接'), ('黑名单', '黑名单')], default='未联系', max_length=10, verbose_name='订单状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_display', models.BooleanField(default=False, verbose_name='是否黑名单')),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='顾问')),
                ('pro_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Pro_content', verbose_name='产品名称')),
            ],
            options={
                'verbose_name': '咨询',
                'verbose_name_plural': '咨询',
            },
        ),
        migrations.CreateModel(
            name='Pro_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('linkman', models.CharField(max_length=10, verbose_name='联系人')),
                ('tel', models.CharField(max_length=11, verbose_name='联系电话')),
                ('state', models.CharField(choices=[('未联系', '未联系'), ('已联系', '已联系'), ('待合作', '待合作'), ('已合作', '已合作'), ('拒绝', '拒接'), ('黑名单', '黑名单')], default='未联系', max_length=10, verbose_name='订单状态')),
                ('des', models.TextField(verbose_name='订单备注')),
                ('pro_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Pro_content', verbose_name='产品名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='订单顾问')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
    ]