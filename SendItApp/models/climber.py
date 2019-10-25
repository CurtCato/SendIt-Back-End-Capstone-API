from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Climber(models.Model):

    """
    Creates table for climber
    Author: Curt Cato
    methods: none
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
            verbose_name = ("climber")
            verbose_name_plural = ("climbers")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'