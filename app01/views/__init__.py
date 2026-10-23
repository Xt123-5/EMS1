"""
views 包：统一重导出各子模块的视图函数，保持 `from app01 import views` 接口不变。
"""

from app01.views.depart import (
    depart_list1,
    depart_add1,
    depart_delete1,
    depart_edit1,
)
from app01.views.user import (
    user_list,
    user_add,
    user_model_form_add,
    user_edit,
    user_delete,
)
from app01.views.pretty import (
    pretty_list,
    pretty_add,
    pretty_edit,
    pretty_delete,
)

__all__ = [
    # 部门管理
    "depart_list1",
    "depart_add1",
    "depart_delete1",
    "depart_edit1",
    # 用户管理
    "user_list",
    "user_add",
    "user_model_form_add",
    "user_edit",
    "user_delete",
    # 靓号管理
    "pretty_list",
    "pretty_add",
    "pretty_edit",
    "pretty_delete",
]
