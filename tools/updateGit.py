# coding=utf-8
""" """

import argparse
import os

def updateGit(comment=None):
	os.system(u"git add *")
	os.system(u"git commit -m \"" + comment + u"\"")
	os.system(u"git push origin master")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--m", "-m", help="git commit", type=str)
	args = parser.parse_args()

	if args.m:
		updateGit(args.m)
	else:
		updateGit(ur"default update")

