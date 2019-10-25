from django.db import models
from .gym import Gym
from .climbingtype import ClimbingType


class GymType(models.Model):
    """
    Creates the join table for the many to many relationship between gyms and climbing types
    Author: Curt Cato
    methods: none
    """

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    climbing_type = models.ForeignKey(ClimbingType, on_delete=models.CASCADE)
