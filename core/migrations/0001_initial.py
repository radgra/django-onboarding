# Generated by Django 2.2.1 on 2019-05-07 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Onboarding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('trail_period', models.IntegerField(default=12, help_text='Weeks')),
            ],
        ),
        migrations.CreateModel(
            name='OnboardingTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Onboarding Templates',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_due', models.CharField(choices=[('AI', 'Bei Info'), ('AS', 'Nach Unterzeichung'), ('PR', 'Zur Vorbereitung'), ('BF', 'Kurz vor Beginn'), ('FR', 'Zum 1. Arbeitstag'), ('AF', 'Nach 1. Arbeitstag')], default='BF', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Onboarding Categories',
            },
        ),
        migrations.CreateModel(
            name='TemplateTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('onboardingTemplate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.OnboardingTemplate')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task')),
            ],
            options={
                'verbose_name_plural': 'Onboarding Template Tasks',
                'unique_together': {('task', 'onboardingTemplate'), ('onboardingTemplate', 'position')},
            },
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TaskCategory'),
        ),
        migrations.AddField(
            model_name='onboardingtemplate',
            name='tasks',
            field=models.ManyToManyField(through='core.TemplateTasks', to='core.Task'),
        ),
        migrations.CreateModel(
            name='OnboardingTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('state', models.CharField(choices=[('CM', 'Erledigt'), ('ST', 'Offen'), ('PR', 'In Bearbeitung'), ('NC', 'Nicht Notwendig')], default='ST', max_length=2)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('date_due', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_updated_tasks', to=settings.AUTH_USER_MODEL)),
                ('onboarding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Onboarding')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Task')),
            ],
            options={
                'verbose_name_plural': 'Onboarding Tasks',
                'unique_together': {('onboarding', 'position'), ('task', 'onboarding')},
            },
        ),
        migrations.AddField(
            model_name='onboarding',
            name='tasks',
            field=models.ManyToManyField(through='core.OnboardingTasks', to='core.Task'),
        ),
        migrations.CreateModel(
            name='NewEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField()),
                ('personal_email', models.EmailField(max_length=254, null=True)),
                ('onboarding', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Onboarding')),
                ('profil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profil')),
            ],
            options={
                'verbose_name_plural': 'New Employees',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_nr', models.IntegerField()),
                ('salary', models.DecimalField(decimal_places=2, help_text='€ Brutto pro Year', max_digits=8)),
                ('work_time', models.IntegerField(default=40, help_text='Hours pro week')),
                ('onboarding', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Onboarding')),
            ],
        ),
    ]
