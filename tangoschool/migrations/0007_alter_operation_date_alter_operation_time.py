# Generated by Django 4.1.7 on 2023-07-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangoschool', '0006_alter_lesson_options_alter_guest_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateField(verbose_name='Дата операции'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='time',
            field=models.TimeField(verbose_name='Время операции'),
        ),
    ]
