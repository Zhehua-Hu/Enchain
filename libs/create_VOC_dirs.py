#!/usr/bin/python
# coding=utf-8
""" """

import argparse
import os, sys
from .pipeline_tools import make_perfect_path


def create_VOC_dirs(dir_name):
	dir_name_ = make_perfect_path(dir_name)
	# print(dir_name_)
	# print(type(dir_name_))
	if not os.path.exists(dir_name_):
		os.system("mkdir " + dir_name_)

	os.system("mkdir " + dir_name_ + "/Annotations")
	os.system("mkdir " + dir_name_ + "/ImageSets")
	os.system("mkdir " + dir_name_ + "/JPEGImages")
	os.system("mkdir " + dir_name_ + "/SegmentationClass")
	os.system("mkdir " + dir_name_ + "/SegmentationObject")
	os.system("mkdir " + dir_name_ + "/ImageSets/Layout")
	os.system("mkdir " + dir_name_ + "/ImageSets/Main")
	os.system("mkdir " + dir_name_ + "/ImageSets/Segmentation")
	print("create_VOC_dirs Done!")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("dir_name_arg", help="Path&Name of directories", type=str)
	args = parser.parse_args()
	create_VOC_dirs(args.dir_name_arg)


#____________________________________
# Demo
# python ./create_VOC_dirs.py /home/zhehua/data/VOC
#____________________________________