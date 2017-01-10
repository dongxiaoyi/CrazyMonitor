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
        ('float',"float")
        ('str',"string"),
    )
    data_type = models.CharField(u'指标数据类型',max_length=32,choices=data_type_choices,default='int')
    #下面null为True，空值将会被存储为NULL，默认为False。blank为True，字段允许为空，默认不允许
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __str__(self):
        return "%s.%s" % (self.name,self.item_key)

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

#模板（用于对应服务）
class Template(models.Model):
    name = models.CharField(u'模板名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service',verbose_name=u'服务列表',blank=True)
    trigger = models.ManyToManyField('Trigger',verbose_name=u'触发器列表',blank=True)
    def __str__(self):
        return self.name

class Tigger(models.Model):
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
    class Host(models.Model):
        