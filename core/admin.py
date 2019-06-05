from django.contrib import admin
from . import models


# Inlines


class TemplateTasksInline(admin.TabularInline):
    model = models.TemplateTasks
    extra = 0
    ordering = ('position',)

    
# Register your models here.


# @admin.register(models.Contract)
# class ContractAdmin(admin.ModelAdmin):
#     pass


# @admin.register(models.NewEmployee)
# class NewEmployeeAdmin(admin.ModelAdmin):
#     pass



# Feature will be added later
# @admin.register(models.OnboardingTemplate)
# class OnboardingTemplateAdmin(admin.ModelAdmin):
#     pass



@admin.register(models.OnboardingTemplate)
class OnboardingTemplateAdmin(admin.ModelAdmin):
    inlines = (TemplateTasksInline,)






