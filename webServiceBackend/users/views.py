from .forms import RegisterForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import requests as rts
from users.models import HistoryValue
from django.conf import settings

from django.db import connection
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line

from django.shortcuts import render, redirect

from email.mime.text import MIMEText
import smtplib
from users import models



REMOTE_HOST = "https://pyecharts.github.io/assets/js"




def exc_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def getValue():
    t = ''
    h = ''
    s = ''
    g = ''
    id = ''
    if settings.CURRENT_TEMPERATURE == None:
        t = "无读数"
    else:
        t = str(settings.CURRENT_TEMPERATURE)
    if settings.CURRENT_HUMIDITY == None:
        h = "无读数"
    else:
        h = str(settings.CURRENT_HUMIDITY)
    if settings.CURRENT_SHIDU == None:
        s = "无读数"
    else:
        s = str(settings.CURRENT_SHIDU)
    if settings.CURRENT_GUANGZHAO == None:
        g = "无读数"
    else:
        g = str(settings.CURRENT_GUANGZHAO)
    if settings.CURRENT_SHEBEIID == None:
        id = "无读数"
    else:
        id = str(settings.CURRENT_SHEBEIID)
    return t, h, s, g , id

def send_mail(message):
    # message = "尊敬的I植物保姆用户，您账号下的{id}的"
    msg = MIMEText(message,"plain ","utf - 8")
    msg['FROM']="I植物保姆"
    msg['Subject'] = "【I植物保姆状态提醒】"
    receivers = ['321782792@qq.com']
    server = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
    server.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_FROM,receivers,msg.as_string())
    server.close()

# @login_required
def index(request):
    t, h, s, g ,id= getValue()
    return render(request, 'index.html', {'t':t, 'h':h, 's':s, 'g':g ,'id':id})

@csrf_exempt
def data(request):
    if 'data' in request.GET:
        d = json.loads(request.GET['data'].replace("'", '"'))
        print("get data {0}, {1}, {2}, {3},{4}".format(d['t'], d['h'], d['s'], d['g'], d['id']))
        value = HistoryValue(temperature=d['t'], humidity=d['h'],shidu=d['s'],guangzhao=d['g'],shebieid = d['id'])
        value.save()
        settings.CURRENT_TEMPERATURE = d['t']
        settings.CURRENT_HUMIDITY = d['h']
        settings.CURRENT_SHIDU = d['s']
        settings.CURRENT_GUANGZHAO = d['g']
        settings.CURRENT_SHEBEIID = d['id']
        if settings.CURRENT_GUANGZHAO != None:
            message = "尊敬的‘I’植物保姆用户Test1，您好，您账号下的id为的植物需要照顾了,快登录网站或微信小程序看看吧。"
            # send_mail(message)
    if 'get' in request.GET:
        rts.get("http://192.168.43.134:5001" + "?op=" + request.GET['get'])
    if 'recv' in request.GET:
        t, h, s, g , id = getValue()
        return HttpResponse(json.dumps({'t': t, 'h': h, 's': s, 'g':g , 'id':id}))
    return HttpResponse("ok")

def detail(request):
    return render(request,'detail.html')



def pyecharts(request):
    template = loader.get_template('pyecharts.html')
    b = bar()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts1(request):
    template = loader.get_template('pyecharts1.html')
    b = bar1()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts2(request):
    template = loader.get_template('pyecharts2.html')
    b = bar2()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts3(request):
    template = loader.get_template('pyecharts3.html')
    b = bar3()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def charts4(request):
    template = loader.get_template('pyecharts4.html')
    b = bar4()
    context = dict(
        myechart=b.render_embed(),
        host=REMOTE_HOST,
        script_list=b.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


def bar():
    query_sql = "select  temperature,humidity,shidu,guangzhao from users_historyvalue"
    data_list = exc_sql(query_sql)
    temperature = [i[0] for i in data_list]
    print(temperature)
    temperature_lens = len(temperature)
    print(temperature_lens)
    temperature1 = temperature[:temperature_lens-24:-1][::-1]
    print(temperature1)
    humidity = [i[1] for i in data_list]
    humidity_lens = len(humidity)
    humidity1 = humidity[:humidity_lens-24:-1][::-1]
    shidu = [i[2] for i in data_list]
    shidu_lens = len(shidu)
    shidu1 = shidu[:shidu_lens-24:-1][::-1]
    guangzhao = [i[3] for i in data_list]
    guangzhao_lens = len(guangzhao)
    guangzhao1 = guangzhao[:guangzhao_lens-24:-1][::-1]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar = Line("植物24小时状态")
    bar.add(
        "大气24h温度",
        attr,
        temperature1,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="°C",
    )
    bar.add(
        "大气24h湿度",
        attr,
        humidity1,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%RH",
    )
    bar.add(
        "土壤24h含水量",
        attr,
        shidu1,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%",
    )
    bar.add(
        "生长24h光照强度",
        attr,
        guangzhao1,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="Lux",
    )
    bar.render()
    return bar

def bar1():
    # query_sql = "select  temperature from tem"
    query_sql = "select  temperature from users_historyvalue"
    data_list = exc_sql(query_sql)
    lens = len(data_list)
    print(data_list)
    x = data_list[:lens-24:-1][::-1]
    print(x)
    # temperature = [i[0] for i in data_list]
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar1 = Line("植物24小时状态")
    bar1.add(
        "大气24h温度",
        attr,
        x,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="°C",
    )
    bar1.render()
    return bar1


def bar2():
    query_sql = "select humidity from users_historyvalue"
    data_list = exc_sql(query_sql)
    lens = len(data_list)
    print(data_list)
    x = data_list[:lens-24:-1][::-1]
    print(x)
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar2 = Line("植物24小时状态")
    bar2.add(
        "大气24h湿度",
        attr,
        x,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%RH",
    )
    bar2.render()
    return bar2


def bar3():
    query_sql = "select  shidu from users_historyvalue"
    data_list = exc_sql(query_sql)
    lens = len(data_list)
    print(data_list)
    x = data_list[:lens-24:-1][::-1]
    print(x)
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar3 = Line("植物24小时状态")
    bar3.add(
        "土壤24h含水量",
        attr,
        x,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="%",
    )
    bar3.render()
    return bar3

def bar4():
    query_sql = "select guangzhao from users_historyvalue"
    data_list = exc_sql(query_sql)
    lens = len(data_list)
    print(data_list)
    x = data_list[:lens-24:-1][::-1]
    print(x)
    attr = ["{}时".format(i) for i in range(1, 24)]
    bar4 = Line("植物24小时状态")
    bar4.add(
        "生长24h光照强度",
        attr,
        x,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="Lux",
    )
    bar4.render()
    return bar4






def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def user(request):
    return render(request, 'user.html')

def design(request):
    return render(request, 'design.html')

def water(request):
    return render(request, 'water.html')


def jiankong(request):
    return render(request, 'jiankong.html')

# 展示设备列表
def equipment_list(request):
    # 去数据库查出所有的设备,填充到HTML中,给用户返回
    ret = models.Equipment.objects.all().order_by("id")
    return render(request, "equipment_list.html", {"equipment_list": ret})


# 添加新的设备
@csrf_exempt
def add_equipment(request):
    error_msg = ""
    # 如果是POST请求,我就取到用户填写的数据
    if request.method == "POST":
        new_name = request.POST.get("equipment_name", None)
        if new_name:
            # 通过ORM去数据库里新建一条记录
            models.Equipment.objects.create(name=new_name)
            # 引导用户访问设备列表页,查看是否添加成功  --> 跳转
            return redirect("/equipment_list/")
        else:
            error_msg = "设备名字不能为空!"
    # 用户第一次来,我给他返回一个用来填写的HTML页面
    return render(request, "add_equipment.html", {"error": error_msg})


# 删除设备的函数
def delete_equipment(request):
    print(request.GET)
    print("=" * 120)
    # 删除指定的数据
    # 1. 从GET请求的参数里面拿到将要删除的数据的ID值
    del_id = request.GET.get("id", None)  # 字典取值,娶不到默认为None
    # 如果能取到id值
    if del_id:
        # 去数据库删除当前id值的数据
        # 根据id值查找到数据
        del_obj = models.Equipment.objects.get(id=del_id)
        # 删除
        del_obj.delete()
        # 返回删除后的页面,跳转到设备的列表页,查看删除是否成功
        return redirect("/equipment_list/")
    else:
        return HttpResponse("要删除的数据不存在!")


# 编辑设备
@csrf_exempt
def edit_equipment(request):
    # 用户修改完设备的名字,点击提交按钮,给我发来新的设备名字
    if request.method == "POST":
        print(request.POST)
        # 取新设备名字
        edit_id = request.POST.get("id")
        new_name = request.POST.get("equipment_name")
        # 更新设备
        # 根据id取到编辑的是哪个设备
        edit_equipment = models.Equipment.objects.get(id=edit_id)
        edit_equipment.name = new_name
        edit_equipment.save()  # 把修改提交到数据库
        # 跳转设备列表页,查看是否修改成功
        return redirect("/equipment_list/")
    # 从GET请求的URL中取到id参数
    edit_id = request.GET.get("id")
    if edit_id:
        # 获取到当前编辑的设备对象
        equipment_obj = models.Equipment.objects.get(id=edit_id)
        return render(request, "edit_equipment.html", {"equipment": equipment_obj})
    else:
        return HttpResponse("编辑的设备不存在!")