# Generated by Django 4.2.7 on 2023-11-16 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codes',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, unique=True),
        ),
    ]
