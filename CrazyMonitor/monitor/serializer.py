#_*_coding:utf-8_*_
from . import models
from django.core.exceptions import ObjectDoesNotExist
from functools import reduce
class ClientHandler(object):
    def __init__(self,client_id):
        self.client_id = client_id
        self.client_config = {
            "services":{}
        }
    def fetch_configs(self):
        try:
            #下面8行是去重，最后所得template_list_list为[[去重后的所有模板]]
            host_obj = models.Host.objects.get(id=self.client_id)
            host_groups_template_list = []
            host_template_list = list(host_obj.templates.select_related())
            for host_group in host_obj.host_groups.select_related():
                host_groups_template_list.extend(list(host_group.templates.select_related()))
            all_templates = host_template_list + host_groups_template_list
            func = lambda host_template_list,host_groups_list:host_template_list if host_groups_template_list in host_template_list else host_template_list + [host_groups_template_list]
            template_list_list = reduce(func,[[],] + all_templates)
            print(template_list_list)
            #下面4行:1.列表里面取模板列表，2.模板列表里面取得所有模板，3.循环所有模板，取得模板中的监控项service4.把service的内容存到self.client_config中
            for template_list in template_list_list:
                for template in template_list:
                    for service in template.services.select_related():
                        self.client_config['services'][service.name] = [service.plugin_name, service.intervel]
            print(self.client_config)
        except ObjectDoesNotExist:
            pass
        return self.client_config