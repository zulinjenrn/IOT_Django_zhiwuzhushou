
from django.urls import path

from authorization import views

urlpatterns = [
    path('test', views.test_session),
    path('authorize', views.authorize, name='authorize'),
    path('status', views.get_status, name='get_status'),
    path('logout', views.logout, name='logout'),
    path('user', views.UserView.as_view()),
    path('addshebei', views.addshebei)
]