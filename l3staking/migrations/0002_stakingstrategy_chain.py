# Generated by Django 4.1.1 on 2024-03-27 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('l3staking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stakingstrategy',
            name='chain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staking_chain_strategies', to='l3staking.stakingchain', verbose_name='质押的链'),
        ),
    ]
