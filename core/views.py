from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from onboarding.models import Onboarding, OnboardingTasks
from django.utils import timezone
import datetime
from django.db.models import Q

@login_required
def main_page(request):
    # MAKE THIS LOGIC REUSABLE ON MODEL !!!!!!!!!!
    # onboarding which entry date < today
    # task where status not completed and date.due > today
    # task due in one week(7 days) - later change this dynamically with filter
    # task updated > today-7days
    if not request.user.is_staff:
        return main_page_user(request)


    today = timezone.now()
    active_onboardings = Onboarding.objects.filter(entry_date__gte=today)
    #status not commpleted
    #tasks to complete
    past_due_tasks = OnboardingTasks.objects.filter(Q(state='ST') | Q(state='PR'), date_due__lt=today)[:10]
    
    tasks_due_week = OnboardingTasks.objects.filter(date_due__lt=today + datetime.timedelta(days=7),date_due__gte=today)[:10]
    
    task_updated_last_week = OnboardingTasks.objects.filter(last_updated__lte=today).order_by('-last_updated')[:10]

    context = {
        'active_onboardings':active_onboardings,
        'past_due_tasks':past_due_tasks,
        'tasks_due_week':tasks_due_week,
        'task_updated_last_week':task_updated_last_week
    }
    return render(request,'core/main.html',context)


def main_page_user(request):
    today = timezone.now()
    tasks_due = OnboardingTasks.objects.filter(Q(date_due__gte=today) | Q(date_due=None),assigned_to=request.user)
    tasks_completed = OnboardingTasks.objects.filter(state=OnboardingTasks.COMPLETED, assigned_to=request.user).order_by('-date_due')[:10]

    context = {
        'tasks_due':tasks_due,
        'tasks_completed':tasks_completed
    }
    return render(request,'core/main_user.html',context)

