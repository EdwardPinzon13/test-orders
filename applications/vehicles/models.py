from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField('Nombre de la Marca',max_length=20)

    def __str__(self):
        return self.brand_name

class TypeVehicle(models.Model):
    type_vehicle = models.CharField('Tipo de vehiculo',max_length=20)

    def __str__(self):
        return self.type_vehicle

class Vehicle(models.Model):
    plate = models.CharField('Placa del Vehiculo',max_length=8)
    modelo = models.IntegerField('Modelo del Vehiculo', max_length = 10)
    brand =  models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name = 'Marca', related_name = 'vehicle_to_brand')
    type_vehicle = models.ForeignKey(TypeVehicle,on_delete=models.CASCADE,verbose_name = 'Tipo Vehiculo', related_name = 'vehicle_to_type_vehicle')

    def __str__(self):
        return self.plate

