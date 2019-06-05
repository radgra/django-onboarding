from django.db import models


class Task(models.Model):
    AFTER_INFO = 'AI'
    AFTER_SIGNING = 'AS'
    PREPARATION = 'PR'
    BEFORE_START_WORK = 'BF'
    FIRST_WORK_DAY ='FR'
    AFTER_FIRST_WORK_DAY = 'AF'
    DATE_DUE_CHOICES = (
        (AFTER_INFO,'Bei Info'),
        (AFTER_SIGNING,'Nach Unterzeichung'),
        (PREPARATION,'Zur Vorbereitung'),
        (BEFORE_START_WORK,'Kurz vor Beginn'),
        (FIRST_WORK_DAY,'Zum 1. Arbeitstag'),
        (AFTER_FIRST_WORK_DAY,'Nach 1. Arbeitstag')
    )
    category = models.ForeignKey('TaskCategory',on_delete=models.CASCADE)
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(null=True,blank=True)
    date_due = models.CharField(max_length=2, choices=DATE_DUE_CHOICES,default=BEFORE_START_WORK) #later - automatic dynamic date assignment for exmaple 2 days beffore/after x(arbeitstart)

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

