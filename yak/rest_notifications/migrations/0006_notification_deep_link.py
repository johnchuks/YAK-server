# Generated by Django 2.0 on 2018-03-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_notifications', '0005_auto_20180209_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='deep_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]