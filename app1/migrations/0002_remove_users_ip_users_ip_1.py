# Generated by Django 4.2.7 on 2023-11-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='ip',
        ),
        migrations.AddField(
            model_name='users',
            name='ip_1',
            field=models.GenericIPAddressField(blank=True, null=True, unique=True),
        ),
    ]
