
from django.core.management.base import BaseCommand, CommandError
from tasks.models import TaskCategory, Task
from core.models import OnboardingTemplate, TemplateTasks


categories = [
    {
        "title":"Event",
    },
    {
        "title":"Sharepoint",
    },
    {
        "title":"Banking-Info",
    },
    {
        "title":"Appointment",
    },
    {
        "title":"Contact",
    },
    {
        "title":"Email",
    },
    {
        "title":"Contract",
    },
    {
        "title":"Calendar",
    },
    {
        "title":"Onboarding",
    },
]

tasks = [
    {
        "title":"Feedback Conversation with Personal",
        "category":"Appointment",
        "date_due":'AF',
        'description':'',
        'position':7
    },
    {
        "title":"Create Sharpoint-Folder for Employee",
        "category":"Sharepoint",
        "date_due":'BF',
        'description':'',
        'position':5

    },
    {
        "title":"Prepare and send Employment Contract",
        "category":"Contract",
        "date_due":'AI',
        'description':'',
        'position':1

    },
    {
        "title":"Welcome Email to future Employee",
        "category":"Email",
        "date_due":'AS',
        'description':'',
        'position':2
    },
    {
        "title":"Create Outlook Contract",
        "category":"Contact",
        "date_due":'PR',
        'description':'',
        'position':3
    },
    {
        "title":"Prepare Privacy Policy DSGVO Documents",
        "category":"Onboarding",
        "date_due":'BF',
        'description':'',
        'position':4
    },
    {
        "title":"Prepare Working Desk",
        "category":"Onboarding",
        "date_due":'FR',
        'description':'',
        'position':6
    },

]



class Command(BaseCommand):
    help = "seed database with default template"


    def handle(self, *args, **options):
        created_cats = []
        created_tasks = []
        for category in categories:
            new_cat = TaskCategory.objects.create(**category)
            created_cats.append(new_cat)

        for task in tasks:
            cat = next(c for c in created_cats if c.title == task['category'] )
            new_task = Task.objects.create(category=cat, title=task['title'], description=task['description'], date_due=task['date_due'])

            created_tasks.append({"task_obj":new_task, 'position':task['position']})

        default_template = OnboardingTemplate.objects.create(title="Default")

        for task in created_tasks:

            TemplateTasks.objects.create(onboardingTemplate=default_template, position=task['position'], task=task['task_obj'])




    