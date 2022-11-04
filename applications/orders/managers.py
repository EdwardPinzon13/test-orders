from django.db import models 

class OrdersManager(models.Manager):

    def NearestDriver(self):
        print('hola')