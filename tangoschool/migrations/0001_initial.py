# Generated by Django 4.1.7 on 2023-05-15 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='students/', verbose_name='фото')),
            ],
            options={
                'verbose_name': 'Гость',
                'verbose_name_plural': 'Гости',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('user', models.CharField(max_length=15, unique=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Номер телефона')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='students/', verbose_name='фото')),
                ('level', models.CharField(blank=True, choices=[('Продолжающий', 'advanced'), ('Начинающий', 'beginner')], max_length=30, null=True, verbose_name='Уровень подготовки')),
                ('base_amount', models.IntegerField(default=1, verbose_name='Коэффициент пристуствия ')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус активности')),
                ('lessons_balance', models.FloatField(default=0, verbose_name='Количество занятий')),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
                'ordering': ['-is_active', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='TrainerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Номер телефона')),
                ('description', models.TextField(blank=True)),
                ('experience', models.PositiveIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='trainers/', verbose_name='фото')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Тренер',
                'verbose_name_plural': 'Тренеры',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_topic', models.TextField(blank=True, max_length=510, null=True, verbose_name='Описание занятия')),
                ('lesson_type', models.CharField(choices=[('full', 'Полное занятие'), ('practice', 'Практика')], max_length=10)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата занятия')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='Время занятия')),
                ('level', models.CharField(blank=True, choices=[('beginner', 'Начинающий'), ('advanced', 'Продолжающий')], max_length=30, null=True, verbose_name='Уровень сложности')),
                ('guests', models.ManyToManyField(blank=True, to='tangoschool.guest', verbose_name='Список гостей, записанных на занятие')),
                ('students', models.ManyToManyField(blank=True, to='tangoschool.student', verbose_name='Список учеников, записанных на занятие')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tangoschool.trainerprofile')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
                'ordering': ['date', 'trainer'],
            },
        ),
    ]