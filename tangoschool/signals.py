from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver
from django.http import request

from .models import TrainerProfile, Lesson, Operation, Student


@receiver(post_save, sender=User)
def create_trainer_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        TrainerProfile.objects.create(user=instance, email=instance.email)


@receiver(pre_save, sender=Operation)
def update_student_balance(sender, instance, **kwargs):
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
        previous_amount = previous_instance.amount
    except sender.DoesNotExist:
        previous_amount = 0

    if instance.operation_type == 'buying':
        amount_diff = instance.amount - previous_amount

    if instance.operation_type == 'visiting':
        amount_diff = previous_amount - instance.amount

    balance = instance.lesson_balance
    balance.balance += amount_diff
    balance.save()


@receiver(post_delete, sender=Operation)
def update_student_balance_on_delete(sender, instance, **kwargs):
    balance = instance.lesson_balance
    if instance.operation_type == 'buying':
        balance.balance -= instance.amount
    else:
        balance.balance += instance.amount
    balance.save()


# @receiver(post_delete, sender=Student)
# def delete_account_with_student(sender, instance):
#     account = instance.student_balance
#     if not account:
#         account.del()
