from django.db import models
from django.contrib.auth import get_user_model
import datetime

# Create your models here.
class Onboarding(models.Model):
    entry_date = models.DateField(blank=False, default=datetime.date.today)
    tasks = models.ManyToManyField('tasks.Task', through="OnboardingTasks")    
    trial_period = models.IntegerField(default=12, help_text="Weeks") # months

    def __str__(self):
        return f'{self.newemployee}'

    def last_name(self):
        return self.newemployee.profile.last_name

    def first_name(self):
        return self.newemployee.profile.first_name

    def tasks_to_complete(self):
        return self.onboardingtasks_set.exclude(state='CM').count()

    def email(self):
        return self.newemployee.personal_email

    #later implement
    def days_since_due(self):
        pass


class NewEmployee(models.Model):
    profile = models.OneToOneField('users.Profile',on_delete=models.CASCADE)
    birth_date = models.DateField()
    personal_email = models.EmailField(null=True, blank=False)
    onboarding = models.OneToOneField('Onboarding',on_delete=models.CASCADE) 

    def work_email(self):
        return self.profile.email

    class Meta:
        verbose_name_plural = "New Employees"
    
    def __str__(self):
        return f'{self.profile}'


class Contract(models.Model):
    contract_nr = models.IntegerField()
    onboarding = models.OneToOneField('Onboarding',on_delete=models.CASCADE)    
    salary = models.DecimalField(max_digits=8, decimal_places=2, help_text="€ Brutto pro Year") # pro Year brutto
    work_time = models.IntegerField(default=40,help_text="Hours pro week") # pro week

    def __str__(self):
        return f'{self.onboarding}'



class OnboardingTasks(models.Model):
    COMPLETED = 'CM'
    OPEN = 'ST'
    PROCCESSED = 'PR'
    NOT_NECESSARY = 'NC'
    STATE_CHOICES = (
        (COMPLETED,'Completed'),
        (OPEN,'Open'),
        (PROCCESSED,'Processed'),
        (NOT_NECESSARY,'Not necessary'),
    )
    task = models.ForeignKey('tasks.Task',on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    onboarding = models.ForeignKey('Onboarding',on_delete=models.CASCADE)
    state = models.CharField(max_length=2,choices=STATE_CHOICES,default=OPEN)
    assigned_to = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="assigned_tasks",blank=True,null=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="last_updated_tasks", null=True,blank=True) 
    date_due = models.DateField(null=True,blank=True)
    description = models.TextField(null=True,blank=True) 
    # later add notes feature - notes from workes about this task - only assigned and supervisor

    class Meta:
        verbose_name_plural = "Onboarding Tasks"
        unique_together = (('task','onboarding'),('onboarding','position'))

