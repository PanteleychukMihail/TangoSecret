from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

LEVEL_CHOICES = (
    ('beginner', 'Начинающий'),
    ('advanced', 'Продолжающий'),
)


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    email = models.EmailField(max_length=70, unique=True)
    birth_day = models.DateField(blank=True, null=True, verbose_name="День рождения")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    description = models.TextField(blank=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True, verbose_name="фото")

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} '

    def get_absolute_url(self):
        return reverse('TrainerProfile-detail', args=[str(self.id)])


class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="фото")

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"

    def __str__(self):
        return self.last_name


class Student(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, unique=True)
    birth_day = models.DateField(blank=True, null=True, verbose_name="День рождения")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="фото")
    level = models.CharField(max_length=30, choices=[("Продолжающий", 'advanced'), ('Начинающий', 'beginner')],
                             blank=True, null=True, verbose_name="Уровень подготовки")
    is_active = models.BooleanField(default=True, verbose_name="Статус активности", editable=True)
    lessons_balance = models.FloatField(default=0, verbose_name="Количество занятий")

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'
        ordering = ['-is_active', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.level}) "

    def get_absolute_url(self):
        return reverse('student', kwargs={'pk': self.id})


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    lesson_topic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Описание занятия")
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=10, choices=(('full', 'Полное занятие'), ('practice', 'Практика')))
    students = models.ManyToManyField(Student, blank=True, verbose_name="Список учеников, записанных на занятие")
    guests = models.ManyToManyField(Guest, blank=True, verbose_name="Список гостей, записанных на занятие")
    date = models.DateField(auto_now_add=True, verbose_name="Дата занятия")
    time = models.TimeField(auto_now_add=True, verbose_name="Время занятия")
    level = models.CharField(max_length=30, choices=LEVEL_CHOICES, blank=True, null=True,
                             verbose_name="Уровень сложности")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ['date', 'trainer']

    def __str__(self):
        return f"{self.level} {self.date} {self.time} {self.trainer.user}"

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk': self.id})


