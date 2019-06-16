from django.db import models
from django.contrib.auth.models import AbstractUser

class HistoryValue(models.Model):
    temperature = models.CharField(max_length=32)
    humidity = models.CharField(max_length=32)
    shidu = models.CharField(max_length=32)
    guangzhao = models.CharField(max_length=32)
    shebieid = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    shebieid = models.CharField(max_length=32)


    # class Meta(AbstractUser.Meta):
    #     pass
# 设备
class Equipment(models.Model):
    id = models.AutoField(primary_key=True)  # 自增的ID主键
    # 创建一个varchar(64)的唯一的不为空的字段
    name = models.CharField(max_length=64, null=False)