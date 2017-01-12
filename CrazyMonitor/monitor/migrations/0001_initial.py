# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-10 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('conditions', models.TextField(verbose_name='告警条件')),
                ('intervel', models.IntegerField(default=300, verbose_name='告警间隔（s）')),
                ('recover_notice', models.BooleanField(default=True, verbose_name='故障回复后发送通知消息')),
                ('recover_subject', models.CharField(blank=True, max_length=128, null=True)),
                ('recover_message', models.TextField(blank=True, null=True)),
                ('enable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('step', models.SmallIntegerField(default=1, verbose_name='第n次报警')),
                ('action_type', models.CharField(choices=[('email', 'Email'), ('sms', 'SMS'), ('script', 'RunScript')], default='email', max_length=255, verbose_name='动作类型')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('monitored_by', models.CharField(choices=[('agent', 'Agent'), ('snmp', 'SNMP'), ('wget', 'WGET')], max_length=64, verbose_name='监控方式')),
                ('status', models.IntegerField(choices=[(1, 'Online'), (2, 'Down'), (3, 'Unreachable'), (4, 'offline')], default=1, verbose_name='状态')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('content', models.TextField(verbose_name='维护内容')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('host_group', models.ManyToManyField(blank=True, to='monitor.HostGroup')),
                ('hosts', models.ManyToManyField(blank=True, to='monitor.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='服务名称')),
                ('intervel', models.IntegerField(default=60, verbose_name='监控间隔')),
                ('plugin_name', models.CharField(default='n/a', max_length=64, verbose_name='插件名')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='指标名称')),
                ('item_key', models.CharField(max_length=64, verbose_name='服务指标key')),
                ('data_type', models.CharField(choices=[('int', 'int'), ('float', 'float'), ('str', 'string')], default='int', max_length=32, verbose_name='指标数据类型')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='模板名称')),
                ('services', models.ManyToManyField(blank=True, to='monitor.Service', verbose_name='服务列表')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='触发器名称')),
                ('expression', models.TextField(verbose_name='表达式')),
                ('severity', models.IntegerField(choices=[(1, 'Information'), (2, 'Warnning'), (3, 'Average'), (4, 'High'), (5, 'Diaster')], verbose_name='告警级别')),
                ('enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
        ),
        migrations.AddField(
            model_name='template',
            name='trigger',
            field=models.ManyToManyField(blank=True, to='monitor.Trigger', verbose_name='触发器列表'),
        ),
        migrations.AddField(
            model_name='service',
            name='items',
            field=models.ManyToManyField(blank=True, to='monitor.ServiceItem', verbose_name='监控列表'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='host',
            name='templates',
            field=models.ManyToManyField(blank=True, to='monitor.Template'),
        ),
        migrations.AddField(
            model_name='action',
            name='host',
            field=models.ManyToManyField(blank=True, to='monitor.Host'),
        ),
        migrations.AddField(
            model_name='action',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='monitor.HostGroup'),
        ),
        migrations.AddField(
            model_name='action',
            name='operations',
            field=models.ManyToManyField(to='monitor.ActionOperation'),
        ),
    ]