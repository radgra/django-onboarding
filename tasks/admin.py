from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','category','date_due')
    list_filter = ('category','date_due')


@admin.register(models.TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    pass