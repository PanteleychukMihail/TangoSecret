# Generated by Django 4.1.7 on 2023-07-12 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangoschool', '0002_alter_student_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='Время операции'),
        ),
    ]
