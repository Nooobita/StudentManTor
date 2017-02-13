# coding: utf-8
# !/usr/bin/env python
__author__ = 'nobita'
__date__ = '2/9/2017 21:25'

import md5
import random

# password encryption
def md5_encrypt(content):
	m = md5.new()
	m.update(content+'xenos')
	return m.hexdigest()


# generate sign
def verify_sign(args,secret):
	sc = secret
	str = ""
	narg = sorted(args.items(), key=lambda asd:asd[0])
	for k,v in narg:
		if k == 'sign':
			continue
		if v[0].decode('utf-8') == "":
			continue
		str += k+v[0].decode('utf-8')
	m = md5.new()
	m.update(sc+str)
	return m.hexdigest()

# app_id app_secret
def make_secret(length):
	member = "abcdefjhijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ0123456789"
	men = [member[random.randint(0, len(member)-1)] for _ in range(length)]
	return "".join(men)
