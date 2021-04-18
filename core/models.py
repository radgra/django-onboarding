from django.db import models


class OnboardingTemplate(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True,blank=True)
    tasks = models.ManyToManyField('tasks.Task', through="TemplateTasks")

    class Meta:
        verbose_name_plural = "Onboarding Templates"

    def __str__(self):
        return self.title
        
class TemplateTasks(models.Model):
    onboardingTemplate = models.ForeignKey("OnboardingTemplate",on_delete=models.CASCADE)
    task = models.ForeignKey('tasks.Task',on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural = "Onboarding Template Tasks"
        unique_together = (('task','onboardingTemplate'),('onboardingTemplate','position'))


