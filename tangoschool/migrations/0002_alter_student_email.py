# Generated by Django 4.1.7 on 2023-07-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangoschool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=70, null=True, verbose_name='Почта'),
        ),
    ]
