# Generated by Django 2.0.7 on 2018-08-09 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_company_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bio',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
