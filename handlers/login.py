# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 21:25'

import json

import common
import optsql.db


class LoginHandler(common.BaseHandler):
    def get(self):
        self.render('login.html')
    def post(self):
    	self.username = self.get_argument("username")
    	self.pwd = self.get_argument("userpassword")
		try:
			student = optsql.db.verify_student(self.username,self.pwd)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			if student:
				self.set_secure_cookie("username", self.username)
				self.set_cookie("app_id",student[1])
				self.set_cookie("app_secret",student[2])
				self.redirect("/students")
			else:
				self.set_header('Content-Type', 'application/json; charset=UTF-8')
				self.write(json.dumps({'status': 'error', 'msg': u'Incorrect password or user does not exist!'}))
				self.finish()


class LogoutHandler(common.BaseHandler):
    def get(self):
        #if(self.get_argument("logout", None)):
        self.clear_cookie("username")
        self.clear_cookie("app_id")
        self.clear_cookie("app_secret")
        self.redirect("/login")
