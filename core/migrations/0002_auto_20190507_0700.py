# Generated by Django 2.2.1 on 2019-05-07 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskcategory',
            options={'verbose_name_plural': 'Task Categories'},
        ),
        migrations.RenameField(
            model_name='newemployee',
            old_name='profil',
            new_name='profile',
        ),
    ]
