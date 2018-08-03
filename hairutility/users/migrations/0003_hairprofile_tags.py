# Generated by Django 2.0.7 on 2018-07-29 20:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('users', '0002_remove_hairprofile_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='hairprofile',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]