from datetime import timedelta, datetime
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from jedi.inference.value import instance

LEVEL_CHOICES = (
    ('beginner', 'Начинающий'),
    ('advanced', 'Продолжающий'),
)


class TrainerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    email = models.EmailField(max_length=70, verbose_name="Почта")
    birth_day = models.DateField(blank=True, null=True, verbose_name="День рождения")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    description = models.TextField(blank=True, verbose_name="Описание")
    experience = models.PositiveIntegerField(blank=True, null=True, verbose_name="Стаж в танго")
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True, verbose_name="фото")

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name}'

    def get_absolute_url(self):
        return reverse('TrainerProfile-detail', args=[str(self.id)])


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(blank=True, verbose_name="Почта")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="фото")

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.FloatField(blank=True, null=True, default=0, verbose_name="Остаток занятий")

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'

    def __str__(self):
        students = ", ".join([str(student) for student in self.students.all()])
        return f"{students}"


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    operation_type = models.CharField(max_length=10, choices=[("buying", 'Покупка'), ('visiting', 'Посещение')],
                                      verbose_name="Операция с балансом")
    date = models.DateField(verbose_name="Дата операции")
    time = models.TimeField(verbose_name="Время операции")
    lesson_balance = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='operations')
    amount = models.FloatField(default=1, verbose_name="количество за раз")

    class Meta:
        verbose_name = 'Операция с балансом'
        verbose_name_plural = 'Операции с балансом'

    def student_name(self):
        names = self.lesson_balance.students.values_list('last_name', flat=True)
        return ', '.join(names)

    student_name.short_description = 'Студент'

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now().date()  # Устанавливаем текущую дату, если она не указана
        if not self.time:
            self.time = datetime.now().time()  # Устанавливаем текущее время, если оно не указано
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Operation: {self.operation_type} - {self.date} - {self.student_name()}"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=25, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(max_length=70, null=True, blank=True, verbose_name="Почта")
    birth_day = models.DateField(blank=True, null=True, verbose_name="День рождения")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="фото")
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES,
                             blank=True, null=True, verbose_name="Уровень подготовки")
    is_active = models.BooleanField(default=True, verbose_name="Статус активности", editable=True)
    student_balance = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="students")

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['-is_active', 'level', 'last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}  ({self.level}) "

    def get_absolute_url(self):
        return reverse('student', kwargs={'pk': self.id})



class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    lesson_topic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Тема занятия")
    trainer1 = models.ForeignKey(TrainerProfile, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name='lessons_as_trainer1', verbose_name="Тренер 1")
    trainer2 = models.ForeignKey(TrainerProfile, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name='lessons_as_trainer2', verbose_name="Тренер 2")
    lesson_type = models.CharField(max_length=10, choices=(('full', 'Полное занятие'), ('practice', 'Практика')))
    students = models.ManyToManyField(Student, blank=True, verbose_name="Список учеников, записанных на занятие")
    guests = models.ManyToManyField(Guest, blank=True, verbose_name="Список гостей, записанных на занятие")
    date = models.DateField(auto_now_add=True, verbose_name="Дата занятия")
    time = models.TimeField(auto_now_add=True, verbose_name="Время занятия")
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, blank=True, null=True,
                             verbose_name="Уровень сложности")
    guests_total_money = models.IntegerField(blank=True, default=0, verbose_name="Сумма от гостей")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.date} {self.time} {self.lesson_type} "

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk': self.id})


