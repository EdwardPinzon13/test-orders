import requests
from datetime import datetime,timedelta
import math
import json

path_to_save_service_drivers = 'applications/orders/data/data_driver.json'

def GetLocationInicialDrivers(date):
        #global drivers_location_global
        res = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
        res = res.json()['alfreds']
        new_dict = {}
        for pos,item in enumerate(res):
            new_dict[item['id']] = item
        #print(new_dict[1], '****')
        #drivers_location_global =list(res)
        with open(path_to_save_service_drivers, 'w') as fp:
            json.dump(res,fp)
        return list(res)

def GetLocationInicialAnyDayDrivers(date):
        #global drivers_location_global
        res = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
        res = res.json()['alfreds']
        return list(res)

def SaveDataDriverJson(data):
    with open(path_to_save_service_drivers, 'w') as fp:
            json.dump(data,fp)


def GetCurrentLocationDrivers():
    with open(path_to_save_service_drivers, 'r') as fp:
            data_driver = json.load(fp)
    return data_driver

def NearestDriver(drivers,pickup):
    nearest= None
    driver_nearest = None
    #distance2 = math.sqrt(pow((x2-x1),2)+pow((y2-y1),2))
    for driver in drivers:
        distance = math.sqrt((int(pickup['lng'])-int(driver['lng']))**2 +(int(pickup['lat'])-int(driver['lat']))**2)
        if nearest==None:
            nearest = distance
            driver_nearest = driver
        if distance < nearest:
            nearest = distance
            driver_nearest = driver
    return driver_nearest

