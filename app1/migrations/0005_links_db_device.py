# Generated by Django 4.2.5 on 2023-09-12 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_alter_links_db_date_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='links_db',
            name='device',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
