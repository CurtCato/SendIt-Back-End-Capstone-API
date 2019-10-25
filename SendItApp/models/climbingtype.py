from django.db import models

class ClimbingType(models.Model):

    """
    Creates table for climbing types
    Author: Curt Cato
    methods: none
    """

    type_name = models.CharField(max_length = 55)

    class Meta:
        verbose_name = ("climbingtype")
        verbose_name_plural = ("climbingtypes")

    def __str__(self):
        return self.type_name