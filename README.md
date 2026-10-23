# 联通用户管理系统（EMS）

基于 Django + MySQL + Bootstrap 的后台管理系统练习项目，包含部门管理、用户管理、靓号管理三个模块的完整增删改查（CRUD）功能。

## 功能特性

- **部门管理**：部门的增删改查
- **用户管理**：员工信息的增删改查，支持原生 Form 与 ModelForm 两种添加方式
- **靓号管理**：手机号靓号的增删改查
  - 手机号格式校验（正则）
  - 新增 / 编辑时唯一性校验（编辑时排除自身）
  - 关键字搜索（手机号）
  - 自定义分页组件（页码折叠、保留搜索条件）

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端 | Python 3.9 · Django 4.2 |
| 数据库 | MySQL（mysqlclient 2.2） |
| 前端 | Bootstrap 3.4 · jQuery |
| 模板 | Django Template |

## 项目结构

```
ems1/
├── ems/                    # 项目配置
│   ├── settings.py         # 数据库、中间件等配置
│   └── urls.py             # 路由分发
├── app01/
│   ├── models.py           # Department / UserInfo / PrettyNum
│   ├── views/              # 视图层（按模块拆分）
│   │   ├── __init__.py     # 统一导出所有视图函数
│   │   ├── depart.py       # 部门管理
│   │   ├── user.py         # 用户管理 + UserModelForm
│   │   ├── pretty.py       # 靓号管理 + 手机号校验
│   │   └── admin.py
│   ├── utils/              # 公共组件
│   │   ├── bootstrap.py    # set_bootstrap：批量注入 form-control 样式
│   │   ├── form.py         # BootStrapModelForm / BootStrapForm 基类
│   │   └── pagination.py   # 通用分页组件（页码折叠 + 跳转）
│   ├── templates/          # 模板（layout.html 母版 + 各页面）
│   └── static/             # bootstrap、jQuery 等静态资源
└── manage.py
```

## 核心设计

### 1. BootStrap 表单基类（utils/form.py）

所有表单统一注入 `form-control` 样式，避免每个 Form 重复写 `__init__` 循环：

```python
class UserModelForm(BootStrapModelForm):   # 继承即自动带样式
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]
```

### 2. 通用分页组件（utils/pagination.py）

- 页码折叠：始终显示首页、末页、当前页前后若干页
- 自动保留 GET 搜索参数
- 空表 / 越界页码保护

### 3. 手机号校验（views/pretty.py）

```python
def clean_mobile(self):
    mobile = self.cleaned_data["mobile"]
    if not re.match(r"^1[3-9]\d{9}$", mobile):
        self.add_error("mobile", "手机号格式错误")
    # 编辑时 exclude(pk) 排除自身再查重
```

## 快速开始

### 1. 环境准备

```bash
pip install django==4.2.30 mysqlclient
```

### 2. 创建数据库

```sql
CREATE DATABASE ems DEFAULT CHARSET utf8;
```

### 3. 修改数据库配置

编辑 `ems/settings.py` 中的 `DATABASES`，填入你的 MySQL 账号密码：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ems',
        'USER': 'root',
        'PASSWORD': '你的密码',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```

### 4. 初始化并启动

```bash
python manage.py migrate
python manage.py runserver
```

访问：

- 部门管理：http://127.0.0.1:8000/depart/list/
- 用户管理：http://127.0.0.1:8000/user/list/
- 靓号管理：http://127.0.0.1:8000/pretty/list/

## 路由一览

| 模块 | 列表 | 添加 | 编辑 | 删除 |
|------|------|------|------|------|
| 部门 | `/depart/list/` | `/depart/add/` | `/depart/<nid>/edit/` | `/depart/delete/` |
| 用户 | `/user/list/` | `/user/add/`（原生 Form）<br>`/user/model/form/add/`（ModelForm） | `/user/<nid>/edit/` | `/user/delete/` |
| 靓号 | `/pretty/list/` | `/pretty/add/` | `/pretty/<nid>/edit/` | `/pretty/delete/` |

## 学习要点

- ModelForm 的字段校验：`clean_字段名` 钩子、唯一性校验、编辑时排除自身
- 公共代码抽取：BootStrap 基类、分页组件、视图按模块拆包
- Django ORM：ForeignKey、choices、`__contains` 模糊查询、Q 对象
