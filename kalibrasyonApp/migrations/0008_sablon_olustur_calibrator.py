# Generated by Django 4.1.6 on 2023-02-11 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalibrasyonApp', '0007_alter_sablon_olustur_set_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='sablon_olustur',
            name='calibrator',
            field=models.ManyToManyField(to='kalibrasyonApp.kalibrator_listesi'),
        ),
    ]
