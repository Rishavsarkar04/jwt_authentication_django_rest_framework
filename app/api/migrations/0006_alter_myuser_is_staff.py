# Generated by Django 4.2 on 2023-04-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_myuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates that this can log into the admin site ', verbose_name='staff status'),
        ),
    ]
