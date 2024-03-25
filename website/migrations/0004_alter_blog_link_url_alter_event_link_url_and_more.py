# Generated by Django 4.1.1 on 2024-03-25 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='link_url',
            field=models.CharField(default='', max_length=500, verbose_name='博客链接'),
        ),
        migrations.AlterField(
            model_name='event',
            name='link_url',
            field=models.CharField(default='', max_length=500, verbose_name='事件链接'),
        ),
        migrations.AlterField(
            model_name='forum',
            name='link_url',
            field=models.CharField(default='', max_length=500, verbose_name='form 链接'),
        ),
    ]
