# Generated by Django 4.1.7 on 2023-07-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangoschool', '0005_alter_student_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['-date', '-time'], 'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Почта'),
        ),
    ]
