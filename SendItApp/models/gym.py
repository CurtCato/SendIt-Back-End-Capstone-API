from django.db import models
from .climber import Climber

class Gym(models.Model):
    """
    Creates table for Gyms
    Author: Curt Cato
    methods: none
    """
    gym_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    url = models.CharField(max_length=50)
    wall_height = models.CharField(max_length=20)
    gym_size = models.CharField(max_length=20)
    climber = models.ForeignKey(Climber, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("gym")
        verbose_name_plural = ("gyms")

    def __str__(self):
        return self.gym_name