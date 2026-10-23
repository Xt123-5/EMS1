import math


class Pagination(object):
    """分页组件：首页/上一页/页码/下一页/末页，并保留原搜索条件

    使用方式（视图中）:
        page_object = Pagination(request, queryset, page_size=10)
        # page_object.queryset  -> 当前页要显示的数据
        # page_object.page_html() -> 底部分页条的 HTML 字符串
    """

    def __init__(self, request, queryset, page_size=10, page_param="page", max_page=11):
        """
        :param request:   Django 的请求对象，用于读取 URL 中的 ?page=N 等参数
        :param queryset:  数据库查询集（未切片的完整数据）
        :param page_size: 每页显示多少条数据
        :param page_param: 页码在 URL 中的参数名，默认 ?page=N
        :param max_page:  页码条上最多同时显示多少个页码按钮（滑动窗口大小）
        """
        # ---------- 第一步：算出总页数 ----------
        total_count = queryset.count()                # 数据总条数
        total_page = math.ceil(total_count / page_size)  # 向上取整：如 95 条 / 每页 10 条 = 10 页

        # ---------- 第二步：解析并修正当前页码（防止用户乱传参数）----------
        page = request.GET.get(page_param, "1")       # URL 里没传 page 时默认第 1 页
        page = int(page) if page.isdecimal() else 1   # 传的不是数字（如 ?page=abc）就回退到第 1 页
        # 越界保护：最小不小于 1，最大不超过总页数（空表时 total_page=0，也按第 1 页处理）
        page = max(1, min(page, total_page if total_page > 0 else 1))

        # ---------- 第三步：计算页码条显示范围（滑动窗口）----------
        # 效果：始终显示 max_page 个页码，并随当前页移动。
        # 例：总 50 页、max_page=11、当前在第 25 页 -> 显示 20 ~ 30
        half = max_page // 2                          # 一半 = 5，即当前页前后各显示 5 个页码
        if total_page < max_page:
            # 情况1：总页数不满一屏，直接显示 1 ~ total_page
            page_start, page_end = 1, total_page
        elif page <= half:
            # 情况2：当前页靠前（如第 1~5 页），窗口贴左显示 1 ~ 11
            page_start, page_end = 1, max_page
        elif page + half > total_page:
            # 情况3：当前页靠后，窗口贴右显示最后 11 个页码
            page_start, page_end = total_page - max_page + 1, total_page
        else:
            # 情况4：当前页在中间，以当前页为中心，前后各 half 个页码
            page_start, page_end = page - half, page + half

        # ---------- 第四步：保存结果 + 切片取当前页数据 ----------
        self.page = page
        self.total_page = total_page
        self.page_start = page_start
        self.page_end = page_end
        # Python 切片写法，Django 会自动翻译成 SQL 的 LIMIT 10 OFFSET N：
        # 第 1 页 -> [0:10]，第 2 页 -> [10:20] ...
        self.queryset = queryset[(page - 1) * page_size: page * page_size]

        # ---------- 第五步：保留除 page 外的其他 URL 参数 ----------
        # 目的：翻页时不丢失搜索条件。如当前 URL 是 ?q=138&page=2，
        # 生成的分页链接会带上 &q=138，变成 ?page=3&q=138
        self.query = ""
        for key, value in request.GET.items():
            if key != page_param:
                self.query += "&%s=%s" % (key, value)

    def page_html(self):
        """生成页码条的 HTML 字符串，配合 Bootstrap 的 <ul class="pagination"> 使用"""
        html_list = []
        # 首页：固定跳到第 1 页
        html_list.append('<li><a href="?page=1%s">首页</a></li>' % self.query)

        # 上一页：正常是当前页减 1；已在第 1 页时保持不动（点击无效果）
        prev = self.page - 1 if self.page > 1 else 1
        html_list.append('<li><a href="?page=%d%s">上一页</a></li>' % (prev, self.query))

        # 中间的数字页码：只渲染 page_start ~ page_end 这个窗口内的页码
        for i in range(self.page_start, self.page_end + 1):
            if i == self.page:
                # 当前页：加 class="active" 高亮显示
                html_list.append('<li class="active"><a href="?page=%d%s">%d</a></li>' % (i, self.query, i))
            else:
                html_list.append('<li><a href="?page=%d%s">%d</a></li>' % (i, self.query, i))

        # 下一页：正常是当前页加 1；已在最后一页时保持不动
        next_page = self.page + 1 if self.page < self.total_page else self.total_page
        html_list.append('<li><a href="?page=%d%s">下一页</a></li>' % (next_page, self.query))
        # 末页：固定跳到最后一页（total_page）
        html_list.append('<li><a href="?page=%d%s">末页</a></li>' % (self.total_page, self.query))

        # 用 join 把列表拼成一个完整字符串（比循环 += 拼接效率更高）
        return "".join(html_list)
