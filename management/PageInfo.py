# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, Page  # 导入django分页模块

class PageInfo(object):
    def __init__(self, current_page, all_count, base_url, per_page=20, show_page=3):
        """

        :param current_page: 当前页
        :param all_count: 总页数
        :param base_url: 模板
        :param per_page: 每页显示数据条数
        :param show_page: 显示链接页个数
        """
        # 若url错误，默认显示第一页（错误类型可能为：空页面编号，非整数型页面编号）
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1

        # 根据数据库信息条数得出总页数
        a, b = divmod(all_count, per_page)
        if b:
            a += 1
        self.all_page = a

        self.base_url = base_url
        self.per_page = per_page
        self.show_page = show_page

    # 当前页起始数据id
    def start_data(self):
        return (self.current_page - 1) * self.per_page

    # 当前页结束数据id
    def end_data(self):
        return self.current_page * self.per_page

    # 动态生成前端html
    def pager(self):
        page_list = []
        half = int((self.show_page - 1) / 2)
        # 如果：总页数 < show_page，默认显示页数范围为： 1~总页数
        if self.all_page < self.show_page:
            start_page = 1
            end_page = self.all_page + 1
        # 如果：总页数 > show_page
        else:
            # 如果：current_page - half <= 0，默认显示页数范围为：1~show_page
            if self.current_page <= half:
                start_page = 1
                end_page = self.show_page + 1
            else:
                # 如果：current_page + half >总页数，默认显示页数范围为：总页数 - show_page ~ 总页数
                if self.current_page + half > self.all_page:
                    end_page = self.all_page + 1
                    start_page = end_page - self.show_page
                else:
                    start_page = self.current_page - half
                    end_page = self.current_page + half + 1

        # 首页
        first_page = "<li><a href='%s?page=%s'>Index</a></li>" % (self.base_url, 1)
        page_list.append(first_page)

        # 上一页（若当前页等于第一页，则上一页无链接，否则链接为当前页减1）
        if self.current_page <= 1:
            prev_page = "<li><a href='#'><<<</a></li>"
        else:
            prev_page = "<li><a href='%s?page=%s'><<<</a></li>" % (self.base_url, self.current_page - 1)
        page_list.append(prev_page)

        # 动态生成中间页数链接
        for i in range(start_page, end_page):
            if i == self.current_page:
                temp = "<li class='active'><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
            page_list.append(temp)

        # 下一页（若当前页等于最后页，则下一页无链接，否则链接为当前页加1）
        if self.current_page >= self.all_page:
            next_page = "<li><a href='#'>>>></a></li>"
        else:
            next_page = "<li><a href='%s?page=%s'>>>></a></li>" % (self.base_url, self.current_page + 1)
        page_list.append(next_page)

        # 末页（若总页数只有一页，则无末页标签）
        if self.all_page > 1:
            last_page = "<li><a href='%s?page=%s'>End</a></li>" % (self.base_url, self.all_page)
            page_list.append(last_page)

        return ''.join(page_list)