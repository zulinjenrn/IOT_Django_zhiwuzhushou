from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^data', views.data,name='data'),
    url(r'^register/', views.register, name='register'),
    url(r'^index', views.index, name='index'),
    url(r'^user', views.user, name='user'),
    url(r'^pyecharts', views.pyecharts, name='pyecharts'),
    url(r'^design', views.design, name='design'),
    url(r'^water', views.water, name='water'),
    url(r'^detail', views.detail, name='detail'),
    url(r'^jiankong', views.jiankong, name='jiankong'),
    url(r'^charts1', views.charts1, name='pyecharts1'),
    url(r'^charts2', views.charts2, name='pyecharts2'),
    url(r'^charts3', views.charts3, name='pyecharts3'),
    url(r'^charts4', views.charts4, name='pyecharts4'),
    url(r'^equipment_list/', views.equipment_list, name='equipment_list'),
    url(r'^add_equipment/', views.add_equipment, name='add_equipment'),
    url(r'^delete_equipment/', views.delete_equipment, name='delete_equipment'),
    url(r'^edit_equipment/', views.edit_equipment, name='edit_equipment'),
]
