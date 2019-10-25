from django.db import models
from .gym import Gym


class ClassOffered(models.Model):

    """
    Created table for ClassesOffered
    Author: Curt Cato
    methods: none
    """

    class_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    days_offered = models.CharField(max_length=50)
    time_offered = models.CharField(max_length=50)
    gym = models.ForeignKey(
        Gym, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("classoffered")
        verbose_name_plural = ("classesoffered")

    def __str__(self):
        return self.class_name