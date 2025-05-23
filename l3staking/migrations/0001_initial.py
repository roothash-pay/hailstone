# Generated by Django 4.1.1 on 2024-03-27 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StakingChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(default='', max_length=100, verbose_name='链名称')),
                ('chain_id', models.CharField(default='', max_length=100, verbose_name='链ID')),
                ('rpc_url', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='节点 rpc')),
            ],
            options={
                'verbose_name': 'StakingChain',
                'verbose_name_plural': 'StakingChain',
            },
        ),
        migrations.CreateModel(
            name='StakingStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(default='Social', max_length=100, verbose_name='质押模块名称')),
            ],
            options={
                'verbose_name': 'StakingStrategy',
                'verbose_name_plural': 'StakingStrategy',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(default='unknown', max_length=500, verbose_name='节点名称')),
                ('eth_income', models.CharField(default='0', max_length=500, verbose_name='Eth 收益金额')),
                ('eth_income_rate', models.CharField(default='0', max_length=500, verbose_name='Eth 收益率')),
                ('dp_income', models.CharField(default='0', max_length=500, verbose_name='DP 收益金额')),
                ('dp_income_rate', models.CharField(default='0', max_length=500, verbose_name='DP 收益率')),
                ('eth_evil', models.CharField(default='0', max_length=500, verbose_name='Eth 惩罚金额')),
                ('eth_evil_rate', models.CharField(default='0', max_length=500, verbose_name='Eth 惩罚率')),
                ('dp_evil', models.CharField(default='0', max_length=500, verbose_name='DP 惩罚金额')),
                ('dp_evil_rate', models.CharField(default='0', max_length=500, verbose_name='DP 惩罚率')),
                ('tvl', models.CharField(default='0', max_length=500, verbose_name='总质押量')),
                ('chain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staking_chain', to='l3staking.stakingchain', verbose_name='质押的链')),
                ('strategy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staking_chain', to='l3staking.stakingstrategy', verbose_name='质押策略')),
            ],
            options={
                'verbose_name': 'Node',
                'verbose_name_plural': 'Node',
            },
        ),
    ]
