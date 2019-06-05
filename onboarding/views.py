from django.shortcuts import render,redirect
from .models import Onboarding, OnboardingTasks
from tasks.models import Task
from django.shortcuts import get_object_or_404
from .filters import OnboardingTasksFilter
from .forms import OnboardingTasksUpdateForm, OnboardingCreateForm, NewEmployeeForm, ProfileForm, TaskUpdateUserForm
from django.utils.dateparse import parse_datetime
from django.db import transaction
from core.models import OnboardingTemplate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
@login_required
def onboarding_list(request):
    onboardings = Onboarding.objects.all()
    context = {
        'onboardings':onboardings
    }
    return render(request,'onboarding/onboarding_list.html',context)


@login_required
def onboarding_detail(request,pk):
    onboarding = get_object_or_404(Onboarding,pk=pk)
    # unique_assigned = []
    # for task in onboarding.tasks:
    #     task.assigned
    # find unqiue name of users that are assigned
    # either sql query or loop with pyhton
    #User.objects.filter(assigned_tasks__onboarding=3)
    on_tasks_filter = OnboardingTasksFilter(request.GET,obj_pk=pk, queryset=onboarding.onboardingtasks_set.all())
    paginator = Paginator(on_tasks_filter.qs,20)
    page = request.GET.get('page')
    paginated = paginator.get_page(page)

    context = {
        'onboarding':onboarding,
        'Task':Task,
        'filter':on_tasks_filter,
        'paginated':paginated
    }
    return render(request,'onboarding/onboarding_detail.html',context)


@login_required
def task_detail(request,pk_onboard, pk_task):
    # diffrent view for non admin user
    if not request.user.is_staff:
        return task_detail_non_admin(request,pk_onboard, pk_task)

    onboarding_task = get_object_or_404(OnboardingTasks,onboarding=pk_onboard, task=pk_task)
    form = OnboardingTasksUpdateForm(instance=onboarding_task,user=request.user)
    date_for_picker = None

    if onboarding_task.date_due:
        date_for_picker = (onboarding_task.date_due.month,onboarding_task.date_due.day,onboarding_task.date_due.year)
    print(date_for_picker)
    context = {
        'o_task':onboarding_task,
        'form':form,
        'date_for_picker':date_for_picker
    }
    return render(request,'onboarding/task_detail_staff.html',context)

## non admin task_detail
def task_detail_non_admin(request,pk_onboard, pk_task):
    onboarding_task = get_object_or_404(OnboardingTasks,onboarding=pk_onboard, task=pk_task)
    if request.method == 'POST':
        form = TaskUpdateUserForm(request.POST, instance=onboarding_task)
        if form.is_valid():
            form.save()
            return redirect('core:main_page')
    else:
        form = TaskUpdateUserForm(instance=onboarding_task)
    context = {
        'o_task':onboarding_task,
        'form':form
    }
    return render(request,'onboarding/task_detail_user.html',context)




@login_required
@user_passes_test(lambda u: u.is_staff)
def update_task_detail(request,pk_onboard, pk_task):
    user = request.user
    onboarding_task = get_object_or_404(OnboardingTasks,onboarding=pk_onboard, task=pk_task)
    if request.method == 'POST':
        form = OnboardingTasksUpdateForm(request.POST,instance=onboarding_task, user=request.user)
        if form.is_valid():
            form.save()
    return redirect('onboarding:task_detail',pk_onboard=pk_onboard,pk_task=pk_task)

@login_required
@permission_required('onboarding.add_onboarding',raise_exception=True)
def onboarding_create(request):
    if request.method == 'POST':
        form1 = OnboardingCreateForm(request.POST)
        form2 = NewEmployeeForm(request.POST)
        form3 = ProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            with transaction.atomic():
                new_onboarding = form1.save()
                new_profile = form3.save()
                new_employee = form2.save(commit=False)
                new_employee.onboarding = new_onboarding
                new_employee.profile = new_profile
                new_employee.save()
                # Using Default Template
                def_template = OnboardingTemplate.objects.get(title='Default')
                for task_temp in def_template.templatetasks_set.all():
                    OnboardingTasks.objects.create(task=task_temp.task,onboarding=new_onboarding,position=task_temp.position)
                messages.success(request, 'Onboarding created!')
                return redirect("onboarding:onboarding_list")



    else:
        form1 = OnboardingCreateForm()
        form2 = NewEmployeeForm()
        form3 = ProfileForm()
    
    context = {
        'form1':form1,
        'form2':form2,
        'form3':form3,
    }

    return render(request,'onboarding/onboarding_create.html',context)

@require_http_methods(["POST",])
@login_required
def onboarding_delete(request,pk):
    onboarding = get_object_or_404(Onboarding,pk=pk)
    onboarding.delete()
    messages.success(request, 'Onboarding deleted!')
    return redirect('onboarding:onboarding_list')

@login_required
@permission_required('onboarding.add_onboarding',raise_exception=True)
def onboarding_update(request,pk):
    onboarding = get_object_or_404(Onboarding,pk=pk)
    if request.method == 'POST':
        form1 = OnboardingCreateForm(request.POST,instance=onboarding)
        form2 = NewEmployeeForm(request.POST,instance=onboarding.newemployee)
        form3 = ProfileForm(request.POST,instance=onboarding.newemployee.profile) 
        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            form1.save()
            form2.save()
            form3.save()
            messages.success(request, 'Onboarding updated!')
            return redirect('onboarding:onboarding_detail',pk=onboarding.id)
    else:
        form1 = OnboardingCreateForm(instance=onboarding)
        form2 = NewEmployeeForm(instance=onboarding.newemployee)
        form3 = ProfileForm(instance=onboarding.newemployee.profile)

    context = {
        'form1':form1,
        'form2':form2,
        'form3':form3,
    } 
    return render(request,'onboarding/onboarding_create.html',context)
