from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.Drug)
admin.site.register(m.Service)
admin.site.register(m.Test)
admin.site.register(m.Receipt)
admin.site.register(m.LabStat)
admin.site.register(m.DrugStat)
admin.site.register(m.ServiceStat)
admin.site.register(m.Consultation)
admin.site.register(m.Transaction)
