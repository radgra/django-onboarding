from django import forms
from .models import Onboarding, OnboardingTasks, NewEmployee
from core.models import OnboardingTemplate
from users.models import Profile
from django.contrib.auth import get_user_model


class OnboardingAdminForm(forms.ModelForm):
    """Form definition for Onboarding."""
    template = forms.ModelChoiceField(queryset=OnboardingTemplate.objects.all(),empty_label="(Nothing)",required=False)


    class Meta:
        """Meta definition for Onboardingform."""

        model = Onboarding
        fields = ('entry_date','trial_period','template')
    
    def save(self, commit=True):
        new_obj = super().save(commit=commit)
        template = self.cleaned_data.get('template',None)
        return new_obj



class OnboardingTasksUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        return super().__init__(*args, **kwargs)
    class Meta:
        model = OnboardingTasks
        fields = ('state','assigned_to','date_due')

    def clean_assigned_to(self):
        data = self.cleaned_data['assigned_to']
        return data

    def clean_date_due(self):
        data = self.cleaned_data['date_due']
        return data


# form for onboarding creation
class ProfileForm(forms.ModelForm): 
    class Meta:
        model = Profile
        fields = ('first_name','last_name','gender')

class OnboardingCreateForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = ('entry_date','trial_period')

class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = NewEmployee
        fields = ('birth_date','personal_email')       


class TaskUpdateStateForm(forms.ModelForm):
    class Meta:
        model = OnboardingTasks
        fields = ('state',)


class TaskUpdateDateDueForm(forms.ModelForm):
    # date_due = forms.DateField(input_formats=['%d %b %Y','%Y-%m-%d'])
    class Meta:
        model = OnboardingTasks
        fields = ('date_due',)

class TaskAssignPersonForm(forms.ModelForm):
    class Meta:
        model = OnboardingTasks
        fields = ('assigned_to',)

class TaskAssignPersonForm(forms.ModelForm):
    class Meta:
        model = OnboardingTasks
        fields = ('assigned_to',)

class OnboardingTemplateForm(forms.Form):
    templates = forms.ModelChoiceField(queryset=OnboardingTemplate.objects.all(),required=True)

    # class Meta:
    #     model = OnboardingTemplate
    #     fields = ('title',)