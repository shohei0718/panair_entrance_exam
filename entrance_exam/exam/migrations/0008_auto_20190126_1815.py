# Generated by Django 2.1.5 on 2019-01-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_auto_20190126_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_day',
            field=models.DateTimeField(verbose_name='受講日'),
        ),
    ]
