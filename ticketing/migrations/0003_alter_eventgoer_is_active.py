# Generated by Django 4.1.7 on 2023-02-20 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_alter_eventgoer_is_reseller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgoer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
    ]
