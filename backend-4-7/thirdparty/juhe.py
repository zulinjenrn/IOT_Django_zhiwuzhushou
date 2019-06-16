import json
import time
import requests

import json
import requests as rts
from django.conf import settings

from utils import proxy
from authorization.models import User



def constellation(cons_name):

    key = '638590d043a54639f3560b5381f5c4f0'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    types = ('today', 'tomorrow', 'week', 'month', 'year')
    params = 'consName=%s&type=%s&key=%s' % (cons_name, types[0], key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    return {
        'name': cons_name,
        'text': data['summary']
    }



def getValue():
    t = ''
    h = ''
    s = ''
    g = ''
    id = str(settings.CURRENT_SHEBEIID)
    if settings.CURRENT_TEMPERATURE == None:
        t = 0
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_HUMIDITY == None:
        h = 0
    else:
        h = str(settings.CURRENT_HUMIDITY)
    if settings.CURRENT_SHIDU == None:
        s = 0
    else:
        s = str(settings.CURRENT_SHIDU)
    if settings.CURRENT_GUANGZHAO == None:
        g = 0
    else:
        g = str(settings.CURRENT_GUANGZHAO)
    return t, h, s, g ,id


def stock():
    requests.get("http://192.168.43.134:5001?op=on")
    t, h, s, g ,id = getValue()
    # if id in User.objects.all().values('user'):
    #     response = {
    #         't': t,
    #         'h': h,
    #         's': s,
    #         'g':g,
    #         'id':id
    #     }
    # else:
    #     response = {
    #         't': None,
    #         'h': None,
    #         's': None,
    #         'g': None,
    #         'id': None
    #     }
    t, h, s, g ,id= getValue()
    response = {
        't': t,
        'h': h,
        's': s,
        'g':g,
        'id':id
    }
    return response


def history_today():
    key = '6c6b318d983b6b4ac8cc5cda0da92155'
    api = 'http://api.juheapi.com/japi/toh'
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    params = 'v=1.0&month=%d&day=%d&key=%s' % (month, day, key)
    url = api + '?' + params
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    result_list = data.get('result')
    result = []
    for item in result_list:
        result.append({
            'title': item.get('title'),
            'content': item.get('des')
        })
    return result


def weather(cityname):
    key = '9a3e1fa6cb79d69f1594af5cb219a469'
    api = 'http://v.juhe.cn/weather/index'
    params = 'cityname=%s&key=%s' % (cityname, key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url, proxies=proxy.proxy())
    data = json.loads(response.text)
    print(data)
    result = data.get('result')
    sk = result.get('sk')
    response = {}
    response['temperature'] = sk.get('temp')
    response['wind_direction'] = sk.get('wind_direction')
    response['wind_strength'] = sk.get('wind_strength')
    response['humidity'] = sk.get('humidity')  # 湿度
    response['time'] = sk.get('time')
    return response
