# Generated by Django 4.1.7 on 2023-03-07 03:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venue_management', '0003_delete_order'),
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue_management.concert', verbose_name='Concert')),
                ('seat_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue_management.seattype', verbose_name='Seat Type')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16, verbose_name='Credit Card Number')),
                ('cvv', models.CharField(max_length=4, verbose_name='CVV')),
                ('exp_month', models.CharField(max_length=2, verbose_name='Exipration month')),
                ('exp_year', models.CharField(max_length=4, verbose_name='Exipration year')),
                ('holder_name', models.CharField(max_length=100, verbose_name='Card Holder Name')),
                ('total', models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=100000)], verbose_name='Price')),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketing.eventgoer', verbose_name='Purchaser')),
                ('tickets', models.ManyToManyField(related_name='order', to='ticketing.ticket', verbose_name='Tickets')),
            ],
        ),
    ]
