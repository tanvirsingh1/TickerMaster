""" Generated by Django 4.1.7 on 2023-02-16 05:55 """

from django.db import migrations


class Migration(migrations.Migration):
    """
    Because pylint forced me :(
    """
    dependencies = [
        ('venue_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venuemanager',
            options={'verbose_name': 'Venue Manager', 'verbose_name_plural': 'Venue Managers'},
        ),
    ]
