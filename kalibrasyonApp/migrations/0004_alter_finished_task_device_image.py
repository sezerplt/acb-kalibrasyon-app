# Generated by Django 4.1.3 on 2022-11-10 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalibrasyonApp', '0003_alter_finished_task_device_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finished_task',
            name='device_image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='images/'),
        ),
    ]
