from django.db import models


# this feature will be added later
class OnboardingTemplate(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True,blank=True)
    tasks = models.ManyToManyField('tasks.Task', through="TemplateTasks")

    class Meta:
        verbose_name_plural = "Onboarding Templates"

    def __str__(self):
        return self.title
        
class TemplateTasks(models.Model):
    AFTER_INFO = 'AI'
    AFTER_SIGNING = 'AS'
    PREPARATION = 'PR'
    BEFORE_START_WORK = 'BF'
    FIRST_WORK_DAY ='FR'
    AFTER_FIRST_WORK_DAY = 'AF'
    DATE_DUE_CHOICES = (
        (AFTER_INFO,'After Info'),
        (AFTER_SIGNING,'After Signing'),
        (PREPARATION,'Preparation'),
        (BEFORE_START_WORK,'Before Work Start'),
        (FIRST_WORK_DAY,'First Day of Work'),
        (AFTER_FIRST_WORK_DAY,'After First Day of Work')
    )
    onboardingTemplate = models.ForeignKey("OnboardingTemplate",on_delete=models.CASCADE)
    task = models.ForeignKey('tasks.Task',on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    date_due = models.CharField(max_length=2, choices=DATE_DUE_CHOICES,default=BEFORE_START_WORK)
    category = models.ForeignKey('tasks.TaskCategory',on_delete=models.CASCADE, null=True)
    
    class Meta:
        verbose_name_plural = "Onboarding Template Tasks"
        unique_together = (('task','onboardingTemplate'),('onboardingTemplate','position'))


