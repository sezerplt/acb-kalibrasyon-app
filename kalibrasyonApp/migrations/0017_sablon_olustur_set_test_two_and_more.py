# Generated by Django 4.1.7 on 2023-04-04 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalibrasyonApp', '0016_finished_task_calibratordata_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sablon_olustur',
            name='set_test_two',
            field=models.CharField(default=" ", max_length=200, verbose_name='ayarlanan'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sablon_olustur',
            name='measurement_result',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('checkbox', 'checkbox')], max_length=200, null=True, verbose_name='ölçüm sonucu 2'),
        ),
    ]
