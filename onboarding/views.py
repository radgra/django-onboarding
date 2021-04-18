from django.shortcuts import render,redirect
from .models import Onboarding, OnboardingTasks
from tasks.models import Task
from django.shortcuts import get_object_or_404
from .filters import OnboardingTasksFilter, TaskDetailFilter
from .forms import OnboardingTasksUpdateForm, OnboardingCreateForm, NewEmployeeForm, ProfileForm, TaskAssignPersonForm, TaskUpdateDateDueForm, TaskUpdateStateForm, OnboardingTemplateForm
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
    on_tasks_filter = OnboardingTasksFilter(request.GET,obj_pk=pk, queryset=onboarding.onboardingtasks_set.all().order_by('position'))
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
    if request.method == 'POST':
        form1 = TaskUpdateStateForm(request.POST, instance=onboarding_task)
        form2 = TaskAssignPersonForm(request.POST, instance=onboarding_task)
        form3 = TaskUpdateDateDueForm(request.POST, instance=onboarding_task)
        form_submitted = request.POST.get('form_type')
        if form_submitted == '1' and form1.is_valid():
            form1.save()
        if form_submitted == '2' and form2.is_valid():
            form2.save()
        if form_submitted == '3' and form3.is_valid():
            form3.save()
        return redirect('onboarding:task_detail',pk_onboard=pk_onboard,pk_task=pk_task)
    else:
        form1 = TaskUpdateStateForm(instance=onboarding_task)
        form2 = TaskAssignPersonForm(instance=onboarding_task)
        form3 = TaskUpdateDateDueForm(instance=onboarding_task)
    date_for_picker = None

    if onboarding_task.date_due:
        date_for_picker = (onboarding_task.date_due.month,onboarding_task.date_due.day,onboarding_task.date_due.year)
    context = {
        'o_task':onboarding_task,
        'form_state':form1,
        'form_person':form2,
        'form_date_due':form3,
        'date_for_picker':date_for_picker
    }
    return render(request,'onboarding/task_detail_staff.html',context)

## non admin task_detail
def task_detail_non_admin(request,pk_onboard, pk_task):
    onboarding_task = get_object_or_404(OnboardingTasks,onboarding=pk_onboard, task=pk_task)
    if request.method == 'POST':
        form = TaskUpdateStateForm(request.POST, instance=onboarding_task)
        if form.is_valid():
            form.save()
            return redirect('core:main_page')
    else:
        form = TaskUpdateStateForm(instance=onboarding_task)
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
        form4 = OnboardingTemplateForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            with transaction.atomic():
                new_onboarding = form1.save()
                new_profile = form3.save()
                new_employee = form2.save(commit=False)
                new_employee.onboarding = new_onboarding
                new_employee.profile = new_profile
                new_employee.save()
                # Using Default Template
                template = form4.cleaned_data['templates']
                # template = OnboardingTemplate.objects.get(title='Default')
                for task_temp in template.templatetasks_set.all():
                    OnboardingTasks.objects.create(task=task_temp.task,onboarding=new_onboarding,position=task_temp.position)
                messages.success(request, 'Onboarding created!')
                return redirect("onboarding:onboarding_list")



    else:
        form1 = OnboardingCreateForm()
        form2 = NewEmployeeForm()
        form3 = ProfileForm()
        form4 = OnboardingTemplateForm()
    context = {
        'form1':form1,
        'form2':form2,
        'form3':form3,
        'form4':form4,
        'title':'Add Onboarding'
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
        'title':'Update Onboarding'
    } 
    return render(request,'onboarding/onboarding_create.html',context)


def task_list(request):
    tasks_qs = OnboardingTasks.objects.all()
    tasks = TaskDetailFilter(request.GET, queryset=tasks_qs)
    paginator = Paginator(tasks.qs,20)
    page = request.GET.get('page')
    paginated = paginator.get_page(page)
    context =  {
        'filter':tasks,
        'paginated':paginated
    }
    return render(request,'onboarding/task_list.html',context)