# Generated by Django 4.1.7 on 2023-03-20 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalibrasyonApp', '0014_remove_finished_task_test_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finished_task',
            name='test_end_date',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Test bitiş tarihi'),
        ),
        migrations.AlterField(
            model_name='finished_task',
            name='test_start_date',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Test başlangıç tarihi'),
        ),
    ]
