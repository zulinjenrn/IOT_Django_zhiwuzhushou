
import os
import json
import random
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

from backend import settings
from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import already_authorized, get_user
from apis.models import HistoryValue
from authorization.models import User
from django.conf import settings

import thirdparty.juhe

popular_stocks = [
    {
        'ID': '000001',
        'name': '设备1'
    }
]



def stock(request):
    data = []
    stocks = []
    print(request)
    if 'get' in request.GET:
        request.get("http://192.168.43.134:5001" + "?op=" + request.GET['get'])
        return HttpResponse("ok")
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3},{4}".format(d['t'], d['h'], d['s'], d['g'], d['id']))
        # value = HistoryValue(temperature=d['t'], humidity=d['h'],shidu=d['s'],guangzhao=d['g'],shebeiid=d['id'])
        # value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
        settings.CURRENT_SHIDU = d['s']
        settings.CURRENT_GUANGZHAO = d['g']
        settings.CURRENT_SHEBEIID = d['id']
    if already_authorized(request):
        user = get_user(request)
        stocks = json.loads(user.focus_stocks)
    else:
        stocks = popular_stocks
    for stock in stocks:
        # result = thirdparty.juhe.stock(stock['market'], stock['code'])
        result = thirdparty.juhe.stock()
        data.append(result)
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)

def mingling(request):
    pass

# def addshebei(request):
#     # print("0")
#     if request.method == 'POST':
#         shebeiid = request.POST.get("shebeiid", None)
#         status = request.POST.get("status", None)
#         if status == True :
#         # 添加到数据库
#             shebeiid = HistoryValue(shebeiid=shebeiid)
#             shebeiid.save()
#             print(shebeiid)
#         else:
#             shebeiid = HistoryValue(shebeiid=shebeiid)
#             shebeiid.save()
#             print(shebeiid)
#     return JsonResponse("ok", safe=False)



























all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
# 星座运势
def constellation(request):
    data = []
    if already_authorized(request):
        user = get_user(request)
        constellations = json.loads(user.focus_constellations)
    else:
        constellations = all_constellations
    for c in constellations:
        result = thirdparty.juhe.constellation(c)
        data.append(result)

    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)
joke_cache = []
# 笑话
def joke(request):
    global joke_cache
    if not joke_cache:
        joke_cache = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r'))
    # 读缓存
    all_jokes = joke_cache
    limit = 10
    sample_jokes = random.sample(all_jokes, limit)
    response = CommonResponseMixin.wrap_json_response(data=sample_jokes, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)


# 历史上的今天
def history_today(request):
    data = thirdparty.juhe.history_today()
    data.reverse()
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(response, safe=False)


