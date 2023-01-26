from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'done', 'created_date')
    search_fields = ('title', 'user')
    sortable_by = ('title', 'user', 'done')
    raw_id_fields = ('user', )
