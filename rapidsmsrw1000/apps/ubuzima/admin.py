#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.contrib import admin
from rapidsmsrw1000.apps.ubuzima.models import *

import unicodecsv as csv
import xlwt
import datetime
from django.contrib.admin import util as admin_util
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse


def export_model_as_excel(modeladmin, request, queryset):
    has_name_fields = ['village', 'cell', 'sector', 'health_centre', 'referral_hospital', 'district', 'province','role']
    is_date_fields = ['date_of_birth', 'dob', 'join_date']
    workbook = xlwt.Workbook()
    sheet_name = "%s" % ( queryset.model.__name__.lower(), )
    sheet = workbook.add_sheet(sheet_name)
    if hasattr(modeladmin, 'exportable_fields'):
        field_list = modeladmin.exportable_fields
    else:
        # Copy modeladmin.list_display to remove action_checkbox
        field_list = modeladmin.list_display[:]
        #field_list.remove('action_checkbox')

    response = HttpResponse(mimetype = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s.xls' % sheet_name

    row = col = 0
    for f in field_list:
        sheet.write(row , col, admin_util.label_for_field(f, queryset.model, modeladmin).upper())
        col = col + 1

    row = row + 1
    for obj in queryset:
        excel_line_values = []
        col = 0
        for field in field_list:
            field_obj, attr, value = admin_util.lookup_field(field, obj, modeladmin)
            
            try:
                if field in has_name_fields:  sheet.write(row, col, value.name)    
                elif field in is_date_fields: sheet.write(row, col, "%d/%d/%d" % (value.day, value.month, value.year))
                else:   sheet.write(row, col, value)
            except Exception, e:
                try:    sheet.write(row, col, value)
                except: sheet.write(row, col, "NULL")                
            col = col + 1
        row = row + 1
 
    workbook.save(response)
    return response

export_model_as_excel.short_description = _('Export to EXCEL')


admin.site.register(Report)
admin.site.register(ReportType)
admin.site.register(Field)
admin.site.register(Patient)
admin.site.register(Reminder)
admin.site.register(UserLocation)
admin.site.register(TriggeredAlert)
admin.site.register(ErrorType)
admin.site.register(ErrorNote)
admin.site.register(Refusal)
admin.site.register(Departure)

class TriggerAdmin(admin.ModelAdmin):
    actions = (export_model_as_excel, )
    exportable_fields = ('id','name', 'description', 'destination', 'message_en', 'message_fr', 'message_kw')
    list_display = ('name', 'description', 'destination', 'message_en', 'message_fr', 'message_kw')
    search_fields = ('name',)

class ReminderAdmin(admin.ModelAdmin):
    actions = (export_model_as_excel, )
    exportable_fields = ('id','name','message_en', 'message_fr', 'message_kw')
    list_display = ('name', 'message_en', 'message_fr', 'message_kw')
    search_fields = ('name',)
    

class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ('key', 'description', 'category')
    search_fields = ('key', 'description')

admin.site.register(TriggeredText, TriggerAdmin)
admin.site.register(FieldType, FieldTypeAdmin)
admin.site.register(ReminderType, ReminderAdmin)


