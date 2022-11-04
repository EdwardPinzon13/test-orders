from tabnanny import verbose
from django.db import models
from django.core.validators import RegexValidator

from applications.vehicles.models import Vehicle

nuipRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
# Create your models here.
class Driver(models.Model):
    name = models.CharField('Nombre del Conductor', max_length=25)
    last_name = models.CharField('Apellido del Conductor', max_length=25)
    nuip = models.CharField('Número de identificación', validators=[nuipRegex,] ,max_length=16)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE, verbose_name = 'vehiculo del conductor', related_name = 'driver_to_vehicule')

    def __str__(self):
        return self.name + ' ' +  self.last_name + ' ' + self.nuip + ' ' + self.vehicle.plate