# Generated by Django 2.0 on 2018-07-10 08:45

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category_help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_tit', models.CharField(max_length=20, verbose_name='帮助栏目')),
                ('Category_seo', models.CharField(max_length=100, verbose_name='SEO标题')),
                ('Category_key', models.CharField(max_length=200, verbose_name='关键词')),
                ('Category_des', models.TextField(max_length=200, verbose_name='栏目描述')),
                ('index', models.IntegerField(default=999, verbose_name='分类的排序')),
            ],
            options={
                'verbose_name': '帮助栏目',
                'verbose_name_plural': '帮助栏目',
            },
        ),
        migrations.CreateModel(
            name='Help_con',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='帮助标题')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='help_con.Category_help', verbose_name='帮助分类')),
            ],
            options={
                'verbose_name': '帮助内容',
                'verbose_name_plural': '帮助内容',
            },
        ),
        migrations.CreateModel(
            name='Help_sug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=100, verbose_name='联系人')),
                ('tel', models.CharField(max_length=100, verbose_name='联系电话')),
                ('email', models.CharField(max_length=100, verbose_name='邮箱')),
                ('help_type', models.CharField(choices=[('投诉', '投诉'), ('建议', '建议')], max_length=10, verbose_name='类型')),
                ('help_con', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='投诉内容')),
                ('state', models.CharField(choices=[('未处理', '未处理'), ('已处理', '已处理')], max_length=10, verbose_name='状态')),
            ],
            options={
                'verbose_name': '投诉与建议',
                'verbose_name_plural': '投诉与建议',
            },
        ),
    ]
