#!/usr/bin/env python
# encoding: utf-8

"""
@author: lvguangchao
@email: guangchao.lv@qq.com
@file: permision.py
@time: 2018/1/8 14:21
"""
import functools
import urllib.parse as urlparse


# 权限注解
def permision(method):
    """Decorate methods with this to require that
       the user must be permissed for this method. """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            menu_resource = self.current_user['menu_scource']
            method_url = self.request.path
            role_id = self.current_user['role_id']

            if urlparse.urlsplit(method_url).scheme:
                method_url = self.request.full_url()
            else:
                method_url = self.request.uri
            if "?" in method_url:
                index = method_url.find('?')
                method_url = method_url[0:index]
            if method_url in menu_resource or role_id == 0:
                return method(self, *args, **kwargs)
            else:
                head = self.request.headers
                if 'XMLHttpRequest' == head.get('X-Requested-With'):
                    self.write_json(-3, '您没有此操作权限')
                    return
                else:
                    self.redirect('/not_permiss')
        else:
            raise Exception(403)
    return wrapper
