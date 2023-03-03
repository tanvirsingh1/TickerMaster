# Generated by Django 4.1.7 on 2023-03-03 21:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venue_management', '0005_alter_venuemanager_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')])),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expiration_date', models.DateField()),
                ('generated_time', models.DateTimeField(auto_now_add=True)),
                ('venue_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue_management.venuemanager')),
            ],
        ),
    ]
