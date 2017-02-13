# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 21:25'

import psycopg2
from util import util
import config
'''
	对数据库的操作
'''


# connect postgreDB
def connSQL():
	return psycopg2.connect(**config.Config_db)


# add student into db
def add_student(username,pwd,age,sex,appid,appsecret):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		pwd = util.md5_encrypt(pwd)
		cur.execute("INSERT INTO student(name,pwd,age,sex,appid,appsecret) VALUES (%s, %s, %s, %s,%s,%s)",(username, pwd, age, sex,appid,appsecret))
		conn.commit()
	finally:
		conn.close()


# get all student from db
def get_all_student(cur_page,pagesize):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT id,name,pwd,age,sex,appid,appsecret FROM student ORDER BY id LIMIT %s OFFSET %s",(pagesize,(cur_page-1)*pagesize))
		all_students = cur.fetchall()
	finally:
		conn.close()
		return all_students

# get student by id
def get_student(student_id):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT id,name,pwd,age,sex,appid,appsecret FROM student WHERE id=%s",(student_id,))
		student = cur.fetchone()
	finally:
		conn.close()
		return student


# delet student from db
def del_student(student_id):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("DELETE FROM student WHERE id=%s",(student_id,))
		conn.commit()
	finally:
		conn.close()


# update student
def update_student(student_id,name,age,sex):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:		
		cur = conn.cursor()
		cur.execute("UPDATE student set name=%s,age=%s,sex=%s WHERE id=%s",(name,age,sex,student_id))
		conn.commit()
	finally:
		conn.close()

# verify student by namm and password
def verify_student(name,password):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT pwd,appid,appsecret FROM student WHERE name=%s",(name,))
		student = cur.fetchone()
	
		if not student:
			return None
		if util.md5_encrypt(password) == student[0]:
			return student
		else:
			return None
	finally:
		conn.close()

# get total data nums
def get_record_nums():
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT COUNT(*) FROM student")
		nums = cur.fetchone()
	finally:
		conn.close()
		return nums[0]

# search student
def search_student(name):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT id,name,pwd,age,sex,appid,appsecret FROM student WHERE name LIKE '%"+name+"%';")
		students = cur.fetchall()
	finally:
		conn.close()
		return students

# verify appid
def verify_appid(appid):
	try:
		conn = connSQL()
	except Exception:
		raise Exception(u'连接数据库失败')
	else:
		cur = conn.cursor()
		cur.execute("SELECT appsecret FROM student WHERE appid=%s",(appid,))
		appsecret = cur.fetchone()
	finally:
		conn.close()
		return appsecret[0]