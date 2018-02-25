# -*- coding: utf-8 -*-

import peewee

class PageInfo(object):
    """
    分页器
    """
    __slots__ = (
        '__cur_page',
        '__count_per_page',
        '__total_object_count',
    )
    def __init__(self, cur_page=1, count_per_page=25):
        """
        一旦初始化，属性及属性值不可变
        """
        self.__total_object_count = 0
        self.__cur_page = int(cur_page)
        self.__count_per_page = int(count_per_page)

    @property
    def has_prev(self):
        return False if self.__cur_page == 1 else True

    @property
    def has_next(self):
        return False if self.__cur_page >= self.__total_object_count else True

    @property
    def has_head(self):
        return False if self.__cur_page == 1 else True

    @property
    def has_tail(self):
        return False if self.__cur_page == self.__total_object_count else True

    @property
    def next(self):
        return self.__cur_page + 1 if self.has_next else self.max_page

    @property
    def prev(self):
        return self.__cur_page - 1 if self.has_prev else 1

    @property
    def max_page(self):
        if self.__total_object_count % self.__count_per_page == 0:
            total_page = self.__total_object_count / self.__count_per_page
            if total_page == 0:
                total_page = 1
        else:
            total_page = self.__total_object_count / self.__count_per_page + 1

        return total_page

    @property
    def display_pages(self):
        display_pages = []
        cur_page = self.__cur_page
        max_page = self.max_page
        if max_page <= 5:
            display_pages = range(1, max_page + 1)
        elif cur_page + 2 <= max_page:
            if cur_page >= 3:
                display_pages = range(cur_page - 2, cur_page + 3)
            else:
                display_pages = range(1, 6)
        else:
            if cur_page >= 5:
                display_pages = range(max_page - 5, max_page + 1)

        return display_pages

    def __get_page_range(self):
        """
        获得当前页显示的item集合的范围
        """
        start = (self.__cur_page - 1) * self.__count_per_page
        end = start + self.__count_per_page
        return start, end

    def paginate(self, objects):
        # 计算总页数
        try:
            item_count = objects.count()
        except:
            item_count = len(objects)
        self.__total_object_count = item_count
        total_page_count = self.max_page

        # 如果浏览页数超过最大页数，则显示最后一页数据
        if self.__cur_page > total_page_count:
            self.__cur_page = total_page_count

        if isinstance(objects, peewee.SelectQuery):
            paged_objects = objects.paginate(self.__cur_page, self.__count_per_page)
        else:
            start, end = self.__get_page_range()
            paged_objects = objects[start:end]

        return paged_objects

    def to_dict(self):
        return {
            'cur_page': self.__cur_page,
            'count_per_page': self.__count_per_page,
            'total_object_count': self.__total_object_count,
            'display_pages': self.display_pages,
            'has_head': self.has_head,
            'has_tail': self.has_tail,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'prev': self.prev,
            'next': self.next,
            'max_page': self.max_page,
        }