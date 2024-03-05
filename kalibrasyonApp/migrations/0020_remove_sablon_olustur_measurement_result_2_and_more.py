# Generated by Django 4.1.7 on 2023-06-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kalibrasyonApp', '0019_sablon_olustur_measurement_result_2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sablon_olustur',
            name='measurement_result_2',
        ),
        migrations.AlterField(
            model_name='sablon_olustur',
            name='measurement_result',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('2xtext', '2xtext'), ('checkbox', 'checkbox')], max_length=200, null=True, verbose_name='ölçüm sonucu'),
        ),
    ]