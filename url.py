# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 18:37'

'''
    记录项目中所有URL和映射的类
'''

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.login import LoginHandler, LogoutHandler
from handlers.students import StudnetsHandler,AddStudentHandler,DeleteStudentHandler,UpdateStudentHandler,SearchStudentHandler,ErrorHandler


url = [
    # 登陆界面
    (r'^/login$', LoginHandler),
    # 注销
    (r'^/logout$', LogoutHandler),
    # 显示学生列表
    (r'^/students$', StudnetsHandler),
    # 添加学生信息
    (r'^/student/add$', AddStudentHandler),
    # 修改学生信息
    (r'^/student/(?P<studentId>.*)/modify$',UpdateStudentHandler),
    # 删除学生信息
    (r'^/student/(?P<studentId>.*)/delete$',DeleteStudentHandler),
    # 搜索学生
    (r'^/search$', SearchStudentHandler),
    # 配置错误页面
    (r'.*',ErrorHandler)

]
