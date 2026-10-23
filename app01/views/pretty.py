"""靓号管理"""

import re

from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import BootStrapModelForm


class PrettyModelForm(BootStrapModelForm):
    """靓号新增 ModelForm：手机号格式 + 查重"""

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        if not re.match(r"^1[3-9]\d{9}$", mobile):
            self.add_error("mobile", "手机号格式不正确")
        if models.PrettyNum.objects.filter(mobile=mobile).exists():
            self.add_error("mobile", "手机号已存在")
        return mobile


class PrettyEditModelForm(PrettyModelForm):
    """靓号编辑 ModelForm：排除自己再查重"""

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        if not re.match(r"^1[3-9]\d{9}$", mobile):
            self.add_error("mobile", "手机号格式不正确")
        if models.PrettyNum.objects.filter(mobile=mobile).exclude(id=self.instance.pk).exists():
            self.add_error("mobile", "手机号已存在")
        return mobile


def pretty_list(request):
    """靓号列表：搜索 + 分页"""
    data_dict = {}
    search = request.GET.get("q", "")
    if search:
        data_dict["mobile__contains"] = search
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-id")
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.queryset,
        "page_string": page_object.page_html(),
        "search": search,
    }
    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """新建靓号"""
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""
    obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request):
    """删除靓号"""
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
