# Generated by Django 2.0 on 2018-07-10 08:45

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='after_ask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.CharField(max_length=100, verbose_name='问')),
                ('answer', models.TextField(max_length=300, verbose_name='答')),
                ('category', models.ManyToManyField(to='product.Category_pro', verbose_name='顶级分类')),
                ('category_grandson', models.ManyToManyField(blank=True, to='product.Category_pro_grandson', verbose_name='三级分类')),
                ('category_son', models.ManyToManyField(to='product.Category_pro_son', verbose_name='二级分类')),
                ('pro', models.ManyToManyField(blank=True, to='product.Pro_content', verbose_name='产品')),
            ],
            options={
                'verbose_name': '售后常见问题',
                'verbose_name_plural': '售后常见问题',
            },
        ),
        migrations.CreateModel(
            name='line_tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tit', models.CharField(default='售后组名称', max_length=50, verbose_name='售后组名称')),
                ('des', models.TextField(default='售后组描述', verbose_name='售后组描述')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='在线客服')),
                ('category', models.ManyToManyField(to='product.Category_pro', verbose_name='顶级分类')),
                ('category_grandson', models.ManyToManyField(blank=True, to='product.Category_pro_grandson', verbose_name='三级分类')),
                ('category_son', models.ManyToManyField(to='product.Category_pro_son', verbose_name='二级分类')),
                ('pro', models.ManyToManyField(blank=True, to='product.Pro_content', verbose_name='产品')),
            ],
            options={
                'verbose_name': '在线客服',
                'verbose_name_plural': '在线客服',
            },
        ),
        migrations.CreateModel(
            name='tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tit', models.CharField(default='售后组名称', max_length=50, verbose_name='售后组名称')),
                ('des', models.TextField(default='售后组描述', verbose_name='售后组描述')),
                ('category', models.ManyToManyField(to='product.Category_pro', verbose_name='顶级分类')),
                ('category_grandson', models.ManyToManyField(blank=True, to='product.Category_pro_grandson', verbose_name='三级分类')),
                ('category_son', models.ManyToManyField(to='product.Category_pro_son', verbose_name='二级分类')),
                ('name', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='团队')),
                ('pro', models.ManyToManyField(blank=True, to='product.Pro_content', verbose_name='产品')),
            ],
            options={
                'verbose_name': '售后服务',
                'verbose_name_plural': '售后服务',
            },
        ),
    ]