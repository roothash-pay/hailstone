# Generated by Django 4.1.1 on 2024-03-17 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airdrop', '0005_remove_periodreward_name_periodreward_period_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(default='', max_length=200, verbose_name='活动主题')),
                ('sub_title', models.CharField(default='', max_length=200, verbose_name='活动副标题')),
                ('image', models.ImageField(blank=True, null=True, upload_to='period/%Y/%m/%d/', verbose_name='活动图片')),
                ('link_url', models.CharField(default='', max_length=100, verbose_name='活动链接')),
                ('period', models.CharField(blank=True, max_length=300, verbose_name='活动周期')),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Period',
            },
        ),
        migrations.RemoveField(
            model_name='periodreward',
            name='period',
        ),
        migrations.RemoveField(
            model_name='periodreward',
            name='sub_title',
        ),
        migrations.RemoveField(
            model_name='periodreward',
            name='title',
        ),
    ]
