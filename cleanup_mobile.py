# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems.settings')
import django
django.setup()
from app01 import models
deleted, _ = models.PrettyNum.objects.filter(mobile='18812345678').delete()
print('清理测试号 18812345678:', deleted, '条')
print('剩余靓号数:', models.PrettyNum.objects.count())
