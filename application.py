# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 18:37'

'''
    完成tornado.web.Application()的实例化
'''

from url import url

import tornado.web
import base64
import os

BasePath = os.path.dirname(__file__)

# 配置信息
setting = dict(
    #Debug=True,
    template_path=os.path.join(BasePath, "templates"),
    static_path=os.path.join(BasePath, "static"),
    cookie_secret=base64.b64encode(u'nobita'),
    login_url='/login'
)

application = tornado.web.Application(
    handlers=url,
    **setting
)
