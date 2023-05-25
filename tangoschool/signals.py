from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.http import request

from .models import TrainerProfile, Lesson


@receiver(post_save, sender=User)
def create_trainer_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        TrainerProfile.objects.create(user=instance, email=instance.email)


@receiver(pre_delete, sender=Lesson)
def update_lessons_balance_on_lesson_delete(sender, instance, **kwargs):
    students = instance.students.all()

    for student in students:
        count = 1
        if instance.lesson_type == 'full':
            student.lessons_balance += 1 * count
        elif instance.lesson_type == 'practice':
            student.lessons_balance += 0.5 * count
        student.save()
