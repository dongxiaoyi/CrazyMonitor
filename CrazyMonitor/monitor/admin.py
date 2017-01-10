from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Host)
admin.site.register(HostGroup)
admin.site.register(Service)
admin.site.register(ServiceItem)
admin.site.register(Action)
admin.site.register(ActionOperation)
admin.site.register(Template)
admin.site.register(Trigger)
admin.site.register(Maintenance)