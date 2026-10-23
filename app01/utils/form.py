"""
公共 Form 基类：统一自动注入 Bootstrap 样式。

使用方式：

    # 原来要写 __init__ 循环加样式，现在只需要继承这两个基类：
    class UserModelForm(BootStrapModelForm):
        class Meta:
            model = models.UserInfo
            fields = ["name", "password", ...]

    class MyForm(BootStrapForm):
        name = forms.CharField(label="姓名")
        ...
"""

from django import forms
from app01.utils.bootstrap import set_bootstrap


class BootStrapModelForm(forms.ModelForm):
    """带 Bootstrap form-control 样式的 ModelForm 基类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_bootstrap(self)


class BootStrapForm(forms.Form):
    """带 Bootstrap form-control 样式的普通 Form 基类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_bootstrap(self)
