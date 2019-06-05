from .starting_data import standard_tasks, task_categories
from tasks.models import Task, TaskCategory
from .models import OnboardingTemplate, TemplateTasks
from django.db import IntegrityError

# Migrating TaskCategory
def seedCategories():
    for task_cat in task_categories:
        try:
                newCat = TaskCategory()
                newCat.title = task_cat['title']
                newCat.save()
        except IntegrityError as e:
                pass

def seedTasks():
    for task in standard_tasks:
        try:
                new_task = Task()
                new_task.title = task['title']
                new_task.date_due = task['due']
                new_task.category = TaskCategory.objects.get(title=task['type'])
                new_task.save()
        except IntegrityError as e:
                pass

def seedDefault():
        # 1.wyszukac template z nazwa default
        # 2.TemplateTask - dla kazdego task z tasks(starting_data) - wziac position i wyszukac task w db
        # 3.Assign task z db do templatetask
        default, created = OnboardingTemplate.objects.get_or_create(title="Default")
        if created:
                default.save()
        for task in standard_tasks:
                temp_task = TemplateTasks()
                temp_task.position = task['position']
                temp_task.task = Task.objects.get(title=task['title'])
                temp_task.onboardingTemplate = default
                temp_task.save()
