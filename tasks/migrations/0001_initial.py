# Generated by Django 2.2.1 on 2019-05-19 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Task Categories',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_due', models.CharField(choices=[('AI', 'Bei Info'), ('AS', 'Nach Unterzeichung'), ('PR', 'Zur Vorbereitung'), ('BF', 'Kurz vor Beginn'), ('FR', 'Zum 1. Arbeitstag'), ('AF', 'Nach 1. Arbeitstag')], default='BF', max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.TaskCategory')),
            ],
        ),
    ]
