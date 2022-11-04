from typing import ValuesView
from django.db import transaction
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist,ValidationError,FieldError
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from datetime import datetime,timedelta
import time
from .serializers import *
from .services import *

from applications.driver.models import Driver
# Create your views here.
class AddOrder(APIView):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description=' \
            Add an order or service to a particular driver, \
            read the description of the fields, take into account their formats. \
            This service takes into account whether the driver is reserved or in service \
            at the time of requesting the or order. '
            ,
            operation_summary= 'Add an order or service to a driver in specific',
            request_body= AddOrderSerializer
        )
    def post(self,request,*args, **kwargs):
        try:
            driver_to_asign = request.data['driver']
            date = request.data['date']
            hour = request.data['hour']
            pickup_place = request.data['pickup_place']
            destination_place = request.data['destination_place']
            time_order = datetime.strptime(hour, '%H:%M:%S').time()
            order_date = date+' '+ str(time_order)
            order_date_cleaned = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
            if pickup_place.keys()!={'lat','lng'} or destination_place.keys()!={'lat','lng'}:
                print('aqui ando')
                raise ValidationError('Formato incorrecto, se esperaba un diccionario de la siguiente manera {lat:valor,lng:valor}')
            else:
                for value in pickup_place.values():
                    if type(value)!=int:
                        raise ValueError('se encontraron letras, se esperaban coordenadas númericas {lat:valor,lng:valor}')
                for value in destination_place.values():
                    if type(value)!=int:
                        raise ValueError('se encontraron letras, se esperaban coordenadas númericas {lat:valor,lng:valor}')
            driver = Driver.objects.filter(id=driver_to_asign).first()
            if driver:
                drivers_in_order = Order.objects.filter(driver_id=driver.id,order_date__date= date , order_date__time__lte=hour,end_order_date__time__gte=hour,order_status=False)
                if not drivers_in_order:
                    if order_date_cleaned.date()< datetime.now().date():
                        raise ValidationError('La fecha de la ordén es anterior a la fecha actual')
                    end_order_date_cleaned = order_date_cleaned + timedelta(hours=1)
                    try:
                        add_order = Order.objects.create(
                            driver_id=driver.id,
                            order_date = order_date_cleaned,
                            pickup_place = pickup_place,
                            destination_place = destination_place,
                            end_order_date = end_order_date_cleaned
                        )
                        if add_order:
                            order_serializer = OrderSerializer(add_order)
                            if order_serializer.is_valid:
                                return Response({'message': 'Servicio reservado con exito','body' : order_serializer.data}, status = status.HTTP_201_CREATED)
                            else:
                                return Response({'message' : 'Error no se ha logrado crear el servicio, verificar los datos'}, status = status.HTTP_409_CONFLICT)
                    except IntegrityError as IntegriError:
                        return Response({'message' : IntegriError.args}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message' : 'Driver ya reservado'}, status = status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message' : 'No se registran datos para el ID del driver suministrado'}, status = status.HTTP_404_NOT_FOUND)
        except ValidationError as ValiError:
            return Response({'message' : ValiError}, status = status.HTTP_400_BAD_REQUEST)
        except ValueError as ValuError:
            return Response({'message' : ValuError.args}, status = status.HTTP_400_BAD_REQUEST)
        except  FieldError as fielderror:
             return Response({'message': fielderror.args}, status = status.HTTP_400_BAD_REQUEST)



class filterOrders(APIView):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description='Search order by Date of order and opcionally for Driver with Driver ID to consult  ',
            operation_summary= 'Search order by Date of order and opcionally for Driver',
            query_serializer= SearchOrdersSerializer
        )
    def get(self,request,*args, **kwargs):
        try:
            date = self.request.query_params.get('date',None)
            driver = self.request.query_params.get('driver',None)
            #filters = request.data['field_filters']
            if date == None:
                raise Exception('Filtro vacio, se esperaban campos con la fecha a filtrar.')
            else:
                order_date_cleaned = datetime.strptime(date, '%Y-%m-%d')
                if driver!=None:
                    driver_query = Driver.objects.filter(id=driver).first()
                    if driver_query:
                        result_query_orders = Order.objects.filter(order_date__date=order_date_cleaned, driver=driver_query.id).order_by('order_date__hour')
                    else:
                        return Response({'message' : 'Driver no encontrado'}, status = status.HTTP_404_NOT_FOUND)
                else:
                    result_query_orders = Order.objects.filter(order_date__date=order_date_cleaned).order_by('order_date__hour')
                if result_query_orders:
                    orders_result_serializer = OrderSerializer(result_query_orders , many=True)
                    if orders_result_serializer.is_valid:
                        return Response({'data' : orders_result_serializer.data}, status = status.HTTP_200_OK)
                else:
                    return Response({'message':'no se encontraron pedidos con los filtros suministrados'}, status = status.HTTP_204_NO_CONTENT)
        except  FieldError as fielderror:
             return Response({'message': fielderror.args}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({'message': exc.args} , status = status.HTTP_406_NOT_ACCEPTABLE)

    def post(self,request,*args, **kwargs):
        try:

            filters = request.data['field_filters']
            if filters=={}:
                raise Exception('Filtro vacio, se esperaban campos con filtros para los pedidos.')
            else:
                if filters['order_date']:
                    date = filters.pop('order_date')
                    order_date_cleaned = datetime.strptime(date, '%Y-%m-%d')
                    result_query_orders = Order.objects.filter(**filters,order_date__date=order_date_cleaned).order_by('order_date__hour')
                else:
                    result_query_orders = Order.objects.filter(**filters).order_by('order_date__hour')
                if result_query_orders:
                    orders_result_serializer = self.serializer_class(result_query_orders , many=True)
                    if orders_result_serializer.is_valid:
                        return Response({'data' : orders_result_serializer.data}, status = status.HTTP_200_OK)
                else:
                    return Response({'message':'no se encontraron pedidos con los filtros suministrados'}, status = status.HTTP_204_NO_CONTENT)
        except  FieldError as fielderror:
             return Response({'message': fielderror.args}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({'message': exc.args} , status = status.HTTP_406_NOT_ACCEPTABLE)



class DriverCertain(APIView):
    serializer_class = DriverSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description=' Search for the closest driver to a location point according to his last \
             registered location and his availability if he is already booked, in a specific time slot ', 
            operation_summary= 'find the nearest driver',
            request_body= FindTheNearestDriverSerializer
        )
    def post(self,request,*args, **kwargs):

        try:
            location  = request.data['location']
            date = request.data['date']
            hour = request.data['hour']
            order_date_cleaned = datetime.strptime(date, '%Y-%m-%d')
            time_order_cleaned = datetime.strptime(hour, '%H:%M:%S').time()
            if location.keys()!={'lat','lng'}:
                raise ValidationError('Formato incorrecto, se esperaba un diccionario de la siguiente manera {lat:valor,lng:valor}')
            else:
                drivers_in_order = Order.objects.filter(order_date__date= order_date_cleaned,order_date__time__lte=time_order_cleaned,end_order_date__time__gte=time_order_cleaned,order_status=False)
                get_location_drivers = GetCurrentLocationDrivers()
                #import pdb; pdb.set_trace()
                ##trae los conductores que a esa hora estan ocupados, si estan ocupados entro
                if drivers_in_order:
                    drivers_unavailable = [driver_order.driver_id for driver_order in drivers_in_order]
                    drivers_available = [driver for driver in get_location_drivers if int(driver['id']) not in drivers_unavailable]
                    if drivers_available!=[]:
                        driver_nearest = NearestDriver(drivers_available,location)
                        driver = Driver.objects.filter(id=driver_nearest['id']).first()
                        if driver:
                            driver_serializer = self.serializer_class(driver)
                            if driver_serializer.is_valid:
                                return Response(
                                    {
                                    'data-driver' : driver_serializer.data,
                                    'location' : {
                                        'lat' : driver_nearest['lat'],
                                        'lng' : driver_nearest['lng']
                                        }
                                    }, status =  status.HTTP_200_OK
                                )
                        else:
                            return Response({'message' : 'Driver no encontrado, verificar corcondancia con el registro de Drivers y el servicio de Ubicación'} , status = status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'message' : 'Drivers  cercanos al punto ya reservados'} , status = status.HTTP_404_NOT_FOUND)
                else:
                    driver_nearest = NearestDriver(get_location_drivers,location)
                    driver = Driver.objects.filter(id=driver_nearest['id']).first()
                    if driver:
                        driver_serializer = self.serializer_class(driver)
                        if driver_serializer.is_valid:
                            return Response(
                                {
                                'data-driver' : driver_serializer.data,
                                'location' : {
                                    'lat' : driver_nearest['lat'],
                                    'lng' : driver_nearest['lng']
                                    }
                                }, status =  status.HTTP_200_OK
                            )
                    else:
                        return Response({'message' : 'Driver no encontrado, verificar corcondancia con el registro de Drivers y el servicio de Ubicación'} , status = status.HTTP_400_BAD_REQUEST)
        except ValidationError as ValiError:
            return Response({'message' : ValiError}, status = status.HTTP_400_BAD_REQUEST)
        except ValueError as ValuError:
            return Response({'message' : ValuError.args}, status = status.HTTP_400_BAD_REQUEST)


class AddOrderWithDynamicDriver(APIView):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_description=' \
            Add an order or service to the nearest driver automatically  \
            if available, read the description of the fields, take into a \
            ccount their formats.  \
            This service takes into account whether the driver is reserved or in service \
             at the time of requesting the order. '
            , 
            operation_summary= 'Add an order or service to a driver automatically',
            request_body= AddOrderDynamicSerializer
        )
    def post(self,request,*args, **kwargs):
        try:
            date = request.data['date']
            hour = request.data['hour']
            pickup_place = request.data['pickup_place']
            destination_place = request.data['destination_place']
            if pickup_place.keys()!={'lat','lng'} or destination_place.keys()!={'lat','lng'}:
                raise ValidationError('Formato incorrecto, se esperaba un diccionario de la siguiente manera {lat:valor,lng:valor}')
            else:
                for value in pickup_place.values():
                    if type(value)!=int:
                        raise ValueError('se encontraron letras, se esperaban coordenadas númericas en {lat:valor,lng:valor} ')
                for value in destination_place.values():
                    if type(value)!=int:
                        raise ValueError('se encontraron letras, se esperaban coordenadas númericas {lat:valor,lng:valor}')
            time_order = datetime.strptime(hour, '%H:%M:%S').time()
            order_date = date+' '+ str(time_order)
            order_date_cleaned = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
            if order_date_cleaned.date() < datetime.now().date():
                    raise ValidationError('La fecha de la ordén es anterior a la fecha actual')
            end_order_date_cleaned = order_date_cleaned + timedelta(hours=1)

            orders_today = Order.objects.filter(order_date__date= str(datetime.now().date()))
            if not orders_today:
                CurrentDay=False
                if order_date_cleaned.date() != datetime.now().date():
                    get_location_drivers = GetLocationInicialAnyDayDrivers(date)
                else:
                    get_location_drivers = GetLocationInicialDrivers(date)
                    CurrentDay = True
                try: # aqui solo traer la data inicial cuando la date se igual a la del dia.
                    drivers_in_order = Order.objects.filter(order_date__date= date,order_date__time__lte=hour,end_order_date__time__gte=hour,order_status=False)
                    if drivers_in_order:
                        drivers_unavailable = [driver_order.driver_id for driver_order in drivers_in_order]
                        drivers_available = [driver for driver in get_location_drivers if int(driver['id']) not in drivers_unavailable]
                        if drivers_available!=[]:
                            driver_nearest = NearestDriver(drivers_available,pickup_place)
                            add_order = Order.objects.create(
                                driver_id=driver_nearest['id'],
                                order_date = order_date_cleaned,
                                pickup_place = pickup_place,
                                destination_place = destination_place,
                                end_order_date = end_order_date_cleaned
                            )
                            if add_order:
                                if CurrentDay:
                                    get_location_drivers[driver_nearest['id']-1]['lat']=str(destination_place['lat'])
                                    get_location_drivers[driver_nearest['id']-1]['lng']=str(destination_place['lng'])
                                    get_location_drivers[driver_nearest['id']-1]['lastUpdate']=str(datetime.now())
                                    SaveDataDriverJson(get_location_drivers)
                                order_serializer = self.serializer_class(add_order)
                                if order_serializer.is_valid:
                                    return Response({'message': 'Servicio reservado con exito','body' : order_serializer.data}, status = status.HTTP_200_OK)
                            else:
                                return Response({'message' : 'Error no se ha logrado crear el servicio, verificar los datos'}, status = status.HTTP_409_CONFLICT)
                        else:
                            return Response({'message' : 'Drivers en franja horaria ya reservados'}, status = status.HTTP_400_BAD_REQUEST)
                    else:
                        driver_nearest = NearestDriver(get_location_drivers,pickup_place)
                        add_order = Order.objects.create(
                            driver_id=driver_nearest['id'],
                            order_date = order_date_cleaned,
                            pickup_place = pickup_place,
                            destination_place = destination_place,
                            end_order_date = end_order_date_cleaned
                        )
                        if add_order:
                            if CurrentDay:
                                get_location_drivers[driver_nearest['id']-1]['lat']=str(destination_place['lat'])
                                get_location_drivers[driver_nearest['id']-1]['lng']=str(destination_place['lng'])
                                get_location_drivers[driver_nearest['id']-1]['lastUpdate']=str(datetime.now())
                                SaveDataDriverJson(get_location_drivers)
                            order_serializer = self.serializer_class(add_order)
                            if order_serializer.is_valid:
                                return Response({'message': 'Servicio reservado con exito','body' : order_serializer.data}, status = status.HTTP_200_OK)
                        else:
                            return Response({'message' : 'Error no se ha logrado crear el servicio, verificar los datos'}, status = status.HTTP_409_CONFLICT)
                except ValidationError as ValiError:
                     return Response({'message' : ValiError}, status = status.HTTP_400_BAD_REQUEST)
            else:
                CurrentDay=False
                if order_date_cleaned.date() != datetime.now().date():
                    drivers_location_updated = GetLocationInicialAnyDayDrivers(date)
                else:
                    drivers_location_updated = GetCurrentLocationDrivers()
                    CurrentDay = True
                drivers_in_order = Order.objects.filter(order_date__date= date,order_date__time__lte=hour,end_order_date__time__gte=hour,order_status=False)
                ##trae los conductores que a esa hora estan ocupados, si estan ocupados entro
                if drivers_in_order:
                    drivers_unavailable = [driver_order.driver_id for driver_order in drivers_in_order]
                    drivers_available = [driver for driver in drivers_location_updated if int(driver['id']) not in drivers_unavailable]
                    if drivers_available!=[]:
                        driver_nearest = NearestDriver(drivers_available,pickup_place)
                        add_order = Order.objects.create(
                            driver_id=driver_nearest['id'],
                            order_date = order_date_cleaned,
                            pickup_place = pickup_place,
                            destination_place = destination_place,
                            end_order_date = end_order_date_cleaned
                        )
                        if add_order:
                            if CurrentDay:
                                drivers_location_updated[driver_nearest['id']-1]['lat']=str(destination_place['lat'])
                                drivers_location_updated[driver_nearest['id']-1]['lng']=str(destination_place['lng'])
                                drivers_location_updated[driver_nearest['id']-1]['lastUpdate']=str(datetime.now())
                                SaveDataDriverJson(drivers_location_updated)
                            order_serializer = self.serializer_class(add_order)
                            if order_serializer.is_valid:
                                return Response({'message': 'Servicio reservado con exito','body' : order_serializer.data}, status = status.HTTP_200_OK)
                        else:
                            return Response({'message' : 'Error no se ha logrado crear el servicio, verificar los datos'}, status = status.HTTP_409_CONFLICT)
                    else:
                        return Response({'message' : 'Drivers en franja horaria ya reservados'}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    #entro si no encuentro conductores ocupados a esa hora
                    driver_nearest = NearestDriver(drivers_location_updated,pickup_place)
                    add_order = Order.objects.create(
                        driver_id=driver_nearest['id'],
                        order_date = order_date_cleaned,
                        pickup_place = pickup_place,
                        destination_place = destination_place,
                        end_order_date = end_order_date_cleaned
                    )
                    if add_order:
                        if CurrentDay:
                            drivers_location_updated[driver_nearest['id']-1]['lat']=str(destination_place['lat'])
                            drivers_location_updated[driver_nearest['id']-1]['lng']=str(destination_place['lng'])
                            drivers_location_updated[driver_nearest['id']-1]['lastUpdate']=str(datetime.now())
                            SaveDataDriverJson(drivers_location_updated)
                        order_serializer = self.serializer_class(add_order)
                        if order_serializer.is_valid:
                            return Response({'message': 'Servicio reservado con exito','body' : order_serializer.data}, status = status.HTTP_200_OK)
                    else:
                        return Response({'message' : 'Error no se ha logrado crear el servicio, verificar los datos'}, status = status.HTTP_409_CONFLICT)
        except ValidationError as ValiError:
            return Response({'message' : ValiError}, status = status.HTTP_404_NOT_FOUND)
        except ValueError as ValuError:
            return Response({'message' : ValuError.args}, status = status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message' : 'Datos en la petición incompletos'}, status = status.HTTP_400_BAD_REQUEST)