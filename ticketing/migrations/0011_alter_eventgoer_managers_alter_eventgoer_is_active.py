# Generated by Django 4.1.7 on 2023-03-01 22:31
""""
This migration file adds two new boolean fields, is_staff and is_superuser, to the VenueManager model.
"""
from django.db import migrations, models
import ticketing.manager


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0010_alter_eventgoer_email_alter_eventgoer_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='eventgoer',
            managers=[
                ('objects', ticketing.manager.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='eventgoer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
    ]
