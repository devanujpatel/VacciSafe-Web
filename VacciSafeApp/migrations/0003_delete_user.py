# Generated by Django 4.0.5 on 2022-06-26 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VacciSafeApp', '0002_alter_vaccinerecords_vac_taken_date_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
