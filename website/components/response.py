
# https://juejin.cn/post/7307502467826008091
from abc import ABC
from collections.abc import MutableMapping


class BaseResult(dict):

    def __init__(self, message='成功', data=None, *args, **kwargs):
        super(BaseResult, self).__init__()
        if kwargs:
            data = self.get('data') or dict()
            data.update(kwargs)
        self.update(success=True, message=message, data=data)

    def success(self, message='操作成功', data=None):
        self.update(message=message, data=data)

    def failure(self, message='操作失败', data=None):
        self.update(success=False, message=message, data=data)

    @property
    def ok(self):
        return self.get('success')

    @property
    def data(self):
        return self.get('data')
