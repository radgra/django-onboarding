# Generated by Django 2.2.1 on 2019-05-19 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190519_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newemployee',
            name='onboarding',
        ),
        migrations.RemoveField(
            model_name='newemployee',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='onboarding',
            name='tasks',
        ),
        migrations.AlterUniqueTogether(
            name='onboardingtasks',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='onboardingtasks',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='onboardingtasks',
            name='last_updated_by',
        ),
        migrations.RemoveField(
            model_name='onboardingtasks',
            name='onboarding',
        ),
        migrations.RemoveField(
            model_name='onboardingtasks',
            name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AlterField(
            model_name='onboardingtemplate',
            name='tasks',
            field=models.ManyToManyField(through='core.TemplateTasks', to='tasks.Task'),
        ),
        migrations.AlterField(
            model_name='templatetasks',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task'),
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.DeleteModel(
            name='NewEmployee',
        ),
        migrations.DeleteModel(
            name='Onboarding',
        ),
        migrations.DeleteModel(
            name='OnboardingTasks',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='TaskCategory',
        ),
    ]
