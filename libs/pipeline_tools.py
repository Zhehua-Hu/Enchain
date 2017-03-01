#!/usr/bin/python
# coding=utf-8
""" """

import os

def make_perfect_path(path):
	# print(path)
	# print(type(path))
	# print(type(path))
	if type(path) != str and type(path) != unicode:
		print('"%s" is not valid path!' % path)
		return
	if path[-1] == '/':
		return path[:-1]
	return path


def make_if_not_exist(path):
	if not os.path.exists(path):
		os.system("mkdir " + path)
	return path


def find_suffix_files(path, suffix):
	ret = []
	for root, dirs, filenames in os.walk(path):
		for filename in filenames:
			if not filename.startswith('.'): # not hiden file
				if filename.endswith(suffix):
					ret.append(filename)
	return ret
