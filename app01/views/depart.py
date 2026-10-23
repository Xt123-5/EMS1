"""部门管理"""

from django.shortcuts import render, redirect
from app01 import models


def depart_list1(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list2.html', {"queryset": queryset})


def depart_add1(request):
    """新建部门"""
    if request.method == "GET":
        return render(request, 'depart_add2.html')

    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete1(request):
    """删除部门"""
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit1(request, nid):
    """编辑部门"""
    if request.method == "GET":
        obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit2.html', {"obj": obj})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')
