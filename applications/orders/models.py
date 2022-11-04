from email.policy import default
from tabnanny import verbose
from django.db import models

from applications.driver.models import Driver
# Create your models here.
class Order(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name = 'Conductor', related_name= 'order_to_driver')
    order_date = models.DateTimeField('Fecha de la orden')
    #arrive_date = models.DateTimeField('Fecha de llegada del conductor', blank=True)
    pickup_place = models.JSONField('Lugar de recogida',null=False,blank=False)
    destination_place = models.JSONField('Lugar de destino',null=False,blank=False)
    order_status = models.BooleanField('Estado de finalización de la orden',default=False)
    end_order_date = models.DateTimeField('Fecha de entrega')


    def __str__(self):
        return self.driver.name 