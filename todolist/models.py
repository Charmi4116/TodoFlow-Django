from django.db import models

# Create your models here.
from django.db import models


class Todo(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    is_deleted = models.BooleanField(default=False)
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='Pending'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.task

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['task'],
                condition=models.Q(is_deleted=False),
                name='unique_active_task'
            )
        ]

# constraints method is not supported by MySQL

# charmi, charmi04