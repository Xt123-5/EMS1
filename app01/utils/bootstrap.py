"""
Bootstrap 样式工具：给 Form/ModelForm 所有字段批量加上 Bootstrap form-control 样式。

视图层 Form 类里原来都有一段重复代码：

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

这段循环抽成了下面的 set_bootstrap 函数。
"""


def set_bootstrap(form):
    """
    给一个 Form/ModelForm 实例的所有字段 widget 统一加上：
        - class="form-control"
        - placeholder=field 的 label

    用法：在 Form 子类的 __init__ 里 super() 之后调用
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                set_bootstrap(self)
    """
    for name, field in form.fields.items():
        if field.widget.attrs:
            # widget 已有 attrs（比如传了 type='date'），用 update 避免覆盖
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label
        else:
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label,
            }
