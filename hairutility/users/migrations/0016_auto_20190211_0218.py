# Generated by Django 2.0.7 on 2019-02-11 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20190124_0029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hairprofile',
            old_name='first_image_url',
            new_name='first_image_key',
        ),
        migrations.RenameField(
            model_name='hairprofile',
            old_name='fourth_image_url',
            new_name='fourth_image_key',
        ),
        migrations.RenameField(
            model_name='hairprofile',
            old_name='second_image_url',
            new_name='second_image_key',
        ),
        migrations.RenameField(
            model_name='hairprofile',
            old_name='third_image_url',
            new_name='third_image_key',
        ),
    ]
