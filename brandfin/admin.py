from django.contrib import admin

from .models import Query, DataConnection, Schema, ReportTemplate
from .forms import DataConnectionForm
from .actions import generate_report_action


class QueryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by_user',)
    list_filter = ('title',)

    actions = [generate_report_action()]


class DataConnectionAdmin(admin.ModelAdmin):
    form = DataConnectionForm


admin.site.register(Query, QueryAdmin)
admin.site.register(DataConnection, DataConnectionAdmin)
admin.site.register(Schema)
admin.site.register(ReportTemplate)