from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name