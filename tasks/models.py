from django.db import models


class Task(models.Model):
    AFTER_INFO = 'AI'
    AFTER_SIGNING = 'AS'
    PREPARATION = 'PR'
    BEFORE_START_WORK = 'BF'
    FIRST_WORK_DAY ='FR'
    AFTER_FIRST_WORK_DAY = 'AF'
    DATE_DUE_CHOICES = (
        (AFTER_INFO,'Info'),
        (AFTER_SIGNING,'After Signing'),
        (PREPARATION,'Preparation'),
        (BEFORE_START_WORK,'Before Work Start'),
        (FIRST_WORK_DAY,'First Day of Work'),
        (AFTER_FIRST_WORK_DAY,'After First Day of Work')
    )
    category = models.ForeignKey('TaskCategory',on_delete=models.CASCADE)
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True,blank=True)
    date_due = models.CharField(max_length=2, choices=DATE_DUE_CHOICES,default=BEFORE_START_WORK)

    def __str__(self):
        return self.title


# Create your models here.


class TaskCategory(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Task Categories"

    def __str__(self):
        return self.title


