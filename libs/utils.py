#!/usr/bin/python
# coding=utf-8
""" """


import sys

def u(x):
    '''py2/py3 unicode helper'''
    if sys.version_info < (3, 0, 0):
        if type(x) == str:
            return x.decode('utf-8')
        if type(x) == QString:
            return unicode(x)
        return x
    else:
        return x  # py3



if __name__ == "__main__":
	print u("hello")
	print type("hello")
	print type(u"hello")
	print type(r"hello")
	print type(ur"hello")
	print type(u("hello"))