# Generated by Django 2.1.5 on 2019-01-26 09:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20190126_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1, verbose_name='性別'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exam.Customer', verbose_name='顧客名'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_day',
            field=models.DateField(verbose_name='受講日'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_time',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='受講時間（h）'),
        ),
    ]
