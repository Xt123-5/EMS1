"""用户管理"""

from django.shortcuts import render, redirect
from django import forms
from app01 import models
from app01.utils.form import BootStrapModelForm, BootStrapForm


class UserModelForm(BootStrapModelForm):
    """用户编辑/新增共用的 ModelForm"""

    create_time = forms.DateField(
        label="入职时间",
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "depart", "gender"]


class MyForm(BootStrapForm):
    """原始 Form 方式（PDF 8.2）"""

    name = forms.CharField(label="姓名")
    password = forms.CharField(label="密码", widget=forms.PasswordInput())
    age = forms.IntegerField(label="年龄")
    account = forms.DecimalField(label="账户余额", max_digits=10, decimal_places=2)
    create_time = forms.DateField(label="入职时间", input_formats=['%Y-%m-%d'],
                                  widget=forms.DateInput(attrs={'type': 'date'}))
    depart = forms.ChoiceField(label="部门", choices=[])
    gender = forms.ChoiceField(label="性别", choices=[(1, "男"), (2, "女")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 自动注入 bootstrap 样式
        # 部门下拉框的数据从数据库动态读取（这是子类独有的逻辑，保留）
        self.fields['depart'].choices = [(obj.id, obj.title) for obj in models.Department.objects.all()]


def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {"queryset": queryset})


def user_edit(request, nid):
    """编辑用户"""
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=obj)
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        models.UserInfo.objects.filter(id=nid).update(
            name=form.cleaned_data['name'],
            password=form.cleaned_data['password'],
            age=form.cleaned_data['age'],
            account=form.cleaned_data['account'],
            create_time=form.cleaned_data['create_time'],
            depart_id=form.cleaned_data['depart'].id,
            gender=form.cleaned_data['gender'],
        )
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request):
    """删除用户"""
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def user_add(request):
    """新建用户（原始 Form 方式）"""
    if request.method == "GET":
        form = MyForm()
        return render(request, 'user_add.html', {"form": form})

    form = MyForm(data=request.POST)
    if form.is_valid():
        models.UserInfo.objects.create(
            name=form.cleaned_data['name'],
            password=form.cleaned_data['password'],
            age=form.cleaned_data['age'],
            account=form.cleaned_data['account'],
            create_time=form.cleaned_data['create_time'],
            depart_id=form.cleaned_data['depart'],
            gender=form.cleaned_data['gender'],
        )
        return redirect('/user/list/')
    return render(request, 'user_add.html', {"form": form})


def user_model_form_add(request):
    """新建用户（ModelForm 方式）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_model_form_add.html', {"form": form})
