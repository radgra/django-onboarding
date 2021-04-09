from django.contrib import admin
from . import models


# Inlines


class TemplateTasksInline(admin.TabularInline):
    model = models.TemplateTasks
    extra = 0
    ordering = ('position',)



@admin.register(models.OnboardingTemplate)
class OnboardingTemplateAdmin(admin.ModelAdmin):
    inlines = (TemplateTasksInline,)






