# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 19:10'

import tornado.web

import json

import common
from util import util
from optsql import db

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# student list
class StudnetsHandler(common.BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.cur_page = self.get_argument("page",1)
		self.pagesize = 3
		self.recordTotal = db.get_record_nums()
		self.pagecount = (self.recordTotal+ self.pagesize-1)//self.pagesize
		try:
			students = db.get_all_student(int(self.cur_page), self.pagesize)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			self.render('students.html',students=students,cur_user=self.current_user,pagecount=self.pagecount)


# add student
class AddStudentHandler(common.BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('student_add.html')
	@tornado.web.authenticated
	def post(self):
		self.username = self.get_argument("username")
		self.pwd = self.get_argument("password")
		self.age = self.get_argument("age")
		self.sex = self.get_argument("sex").decode('utf-8')
		self.app_id = util.make_secret(16)
		self.app_secret = util.make_secret(32)
		try:
			db.add_student(self.username, self.pwd, self.age, self.sex, self.app_id,self.app_secret)
		except Exception,e:
			self.render('error.html',Exception=Exception,e=e)
		else:
			self.redirect('/students')



# delete student
class DeleteStudentHandler(common.BaseHandler):
	@tornado.web.authenticated
	def get(self, studentId):
		try:
			db.del_student(studentId)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			self.redirect('/students')



# update student
class UpdateStudentHandler(common.BaseHandler):
	@tornado.web.authenticated
	def get(self, studentId):
		try:
			self.student = db.get_student(studentId)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			self.render("student_modify.html", student=self.student)
	@tornado.web.authenticated
	def post(self, studentId):
		self.username = self.get_argument('username')
		self.age = self.get_argument('age')
		self.sex = self.get_argument('sex')
		try:
			db.update_student(studentId, self.username, self.age, self.sex)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			self.redirect('/students')


# search student
class SearchStudentHandler(common.BaseHandler):
	@tornado.web.authenticated
	def post(self):
		self.sign = self.get_argument('sign',"")
		self.searchname = self.get_argument('searchname',"")
		self.appid = str(self.get_cookie("app_id"))
		try:
			self.app_secret = db.verify_appid(self.appid)
		except Exception,e:
			self.render("error.html",Exception=Exception,e=e)
		else:
			# 判断appid是否存在
			if self.app_secret:
				self.ver_sign = util.verify_sign(self.request.arguments,self.app_secret)
				if self.sign == self.ver_sign:
					try:
						students = db.search_student(self.searchname)
					except Exception,e:
						self.render("error.html",Exception=Exception,e=e)
					self.set_header('Content-Type', 'application/json; charset=UTF-8')
            		self.write(json.dumps({'status': 'success', 'content': json.dumps(students)}))
            		self.finish()
            	# else:
            	# 	self.set_header('Content-Type', 'application/json; charset=UTF-8')
            	# 	self.write(json.dumps({'status': 'fail', 'msg': 'sign verify fail'}))
            	# 	self.finish()

# error page
class ErrorHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("404.html")
