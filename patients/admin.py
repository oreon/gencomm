from django.contrib import admin

from patients.models import Schedule, Ward, Appointment, Patient, Bed,\
    ScheduleProcedure, PatientScheduleProcedure, Measurement,\
    MeasurementCategory, PatientMeasurement


class CustomModelAdminMixin(object):

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)

class WardAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class PatientAdmin( admin.ModelAdmin):
    list_display = ('id','displayName', 'firstName', 'lastName', 'state','show_view_url')
    list_filter = ('dob', 'gender')
    ordering = ('-id',)
    search_fields = ('firstName','lastName', 'dob')
    
    def show_view_url(self, obj):
        return '<a href="viewPatient/%d/">View</a>' % (obj.id)
    show_view_url.allow_tags = True
    

class BedAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class PatientScheduleProcedureAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

class ScheduleProcedureInline(admin.TabularInline):
    model = ScheduleProcedure
    
class ScheduleAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    inlines = [ ScheduleProcedureInline, ]


# Register your models here.
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Ward, WardAdmin)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(Appointment)

admin.site.register(ScheduleProcedure)

admin.site.register(PatientScheduleProcedure, PatientScheduleProcedureAdmin)

admin.site.register(Measurement)
admin.site.register(MeasurementCategory)
admin.site.register(PatientMeasurement)
