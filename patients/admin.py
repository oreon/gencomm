from django.contrib import admin

from patients.models import Schedule, Ward, Appointment, Patient, Bed


class CustomModelAdminMixin(object):

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)

class WardAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class PatientAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class BedAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Ward, WardAdmin)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Appointment)

