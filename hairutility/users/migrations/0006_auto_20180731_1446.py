# Generated by Django 2.0.7 on 2018-07-31 14:46

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_company_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='zip_code',
            field=localflavor.us.models.USZipCodeField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=localflavor.us.models.USStateField(blank=True, max_length=2),
        ),
    ]
