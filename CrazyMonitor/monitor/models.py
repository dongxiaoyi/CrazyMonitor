#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
#监控指标
class ServiceItem(models.Model):
    #service name
    name = models.CharField(u'指标名称',max_length=64)
    #客户端发过来的唯一验证字符串
    item_key = models.CharField(u'服务指标key',max_length=64)
    #数据类型
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string"),
    )
    data_type = models.CharField(u'指标数据类型',max_length=32,choices=data_type_choices,default='int')
    #下面null为True，空值将会被存储为NULL，默认为False。blank为True，字段允许为空，默认不允许
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)

    def __str__(self):
        return "%s.%s" % (self.name,self.item_key)

    class Meta:
        verbose_name = '服务指标'
        verbose_name_plural = '服务指标'


#监控项
class Service(models.Model):
    name = models.CharField(u'服务名称',max_length=64,unique=True)
    #间隔
    intervel = models.IntegerField(u'监控间隔',default=60)
    plugin_name = models.CharField(u'插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceItem',verbose_name=u'监控列表',blank=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name
    #def get_service_item(obj):
    #    return ','.join([i.name for i in obj.items.all()])
    class Meta:
        verbose_name = '监控项'
        verbose_name_plural = '监控项'

#模板（用于对应服务）
class Template(models.Model):
    name = models.CharField(u'模板名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service',verbose_name=u'服务列表',blank=True)
    trigger = models.ManyToManyField('Trigger',verbose_name=u'触发器列表',blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '模板'
        verbose_name_plural = '模板'

class Trigger(models.Model):
    name = models.CharField(u'触发器名称', max_length=64)
    expression = models.TextField(u'表达式')
    severity_choices = (
        (1,'Information'),
        (2,'Warnning'),
        (3,'Average'),
        (4,'High'),
        (5,'Diaster')
    )
    severity = models.IntegerField(u'告警级别',choices=severity_choices)
    enable = models.BooleanField(u'是否启用',default=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '触发器'
        verbose_name_plural = '触发器'

class Host(models.Model):
    name = models.CharField(max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    host_groups = models.ManyToManyField('HostGroup',blank=True)
    templates = models.ManyToManyField('Template', blank=True)
    moitored_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )
    monitored_by = models.CharField(u'监控方式',max_length=64,choices=moitored_by_choices)
    status_choices = (
        (1,'Online'),
        (2,'Down'),
        (3,'Unreachable'),
        (4,'offline'),
    )
    status = models.IntegerField(u'状态',choices=status_choices,default=1)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = '主机'

class HostGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    templates = models.ManyToManyField('Template',blank=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'

class Action(models.Model):
    name = models.CharField( max_length=64, unique=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)
    host = models.ManyToManyField('Host', blank=True)
    conditions = models.TextField(u'告警条件')
    intervel = models.IntegerField(u'告警间隔（s）',default=300)
    operations = models.ManyToManyField('ActionOperation')
    recover_notice = models.BooleanField(u'故障回复后发送通知消息',default=True)
    recover_subject = models.CharField(max_length=128,blank=True,null=True)
    recover_message = models.TextField(blank=True,null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ActionOperation(models.Model):
    name = models.CharField(max_length=64)
    step = models.SmallIntegerField(u'第n次报警',default=1)
    action_type_chioce = (
        ('email','Email'),
        ('sms','SMS'),
        ('script','RunScript'),
    )
    action_type = models.CharField(u'动作类型',choices=action_type_chioce,default='email',max_length=255)
    #notifiers = models.ManyToManyField(host_models.UserProfile,verbose_name=u'通知对象',blank=True)

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    name = models.CharField( max_length=64, unique=True)
    hosts = models.ManyToManyField('Host',blank=True)
    host_group = models.ManyToManyField('HostGroup',blank=True)
    content = models.TextField(u'维护内容')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '维护'
        verbose_name_plural = '维护'