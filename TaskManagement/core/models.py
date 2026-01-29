from django.db import models
from django.contrib.auth.models import AbstractUser


# user model

class User(AbstractUser):

    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User')
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )


# task model

class TaskModel(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('completed', 'Completed')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        limit_choices_to={'role': 'user'}
    )
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    completion_report = models.TextField(
        null=True,
        blank=True
    )
    worked_hours = models.FloatField(
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = 'TaskModel'
        verbose_name_plural = 'Task_Model'
        indexes = [
            models.Index(fields=['status'])
        ]


    def __str__(self):
        return f'{self.title}'