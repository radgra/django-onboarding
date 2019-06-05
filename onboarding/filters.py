from onboarding.models import OnboardingTasks
from tasks.models import Task
import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

class OnboardingTasksFilter(django_filters.FilterSet):
    state = django_filters.ChoiceFilter(empty_label="All", choices=OnboardingTasks.STATE_CHOICES)
    def __init__(self, *args, obj_pk=None, **kwargs):
        print(self)
        super().__init__(*args, **kwargs)
        # if obj_pk:
        #     User = get_user_model()
        #     qs = User.objects.filter(assigned_tasks__onboarding=obj_pk)
        #     self.base_filters['assigned_to'].extra['queryset'] = qs
        # print(self)

    class Meta:
        model = OnboardingTasks
        fields = ['assigned_to','task__category','task__date_due']
    
    