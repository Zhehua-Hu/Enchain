#!/usr/bin/env python
# coding=utf-8
"""
Provide FileList Class
"""

import os
import argparse

class FileList():
	"""
	class: provide file(eg.images,videos) list management
	"""

	cur_idx = 0
	file_cnt = 0

	def __init__(self, folder, search_type="NotRecursive", supported_file_suffix=None):
		self.file_dirname = folder
		self.file_suffix = supported_file_suffix
		self.files_path, self.file_cnt = self.getContainedfiles(folder, type=search_type)


	def isEmpty(self):
		if self.file_cnt > 0:
			return False
		else:
			return True

	def getContainedfiles(self, folder, type="NotRecursive"):
		"""
		get Contained files
		:param folder: searched folder
		:param type: determine if search sub-folder
		:return: full path list, list length
		"""
		files_name = []
		files_path = []
		ret_cnt = 0
		for root, dirs, filenames in os.walk(folder):
			if type == "Recursive":
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if self.file_suffix is not None:
							if filename.split(".")[-1].upper() in self.file_suffix:
								files_name.append(filename)
								ret_cnt += 1
						else:
							files_name.append(filename)
							ret_cnt += 1
			else:
				for filename in filenames:
					if not filename.startswith('.'): # not hiden file
						if self.file_suffix is not None:
							if filename.split(".")[-1].upper() in self.file_suffix:
								files_name.append(filename)
						else:
							files_name.append(filename)
				ret_cnt = len(files_name)
				break

		files_name.sort()  # from 000001 to increase
		for item in files_name:
			files_path.append(os.path.join(self.file_dirname, item))
		return files_path, ret_cnt

	def getFilesPathList(self):
		return self.files_path

	def firstFile(self):
		return self.files_path[0]

	def nextFile(self):
		self.cur_idx += 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.files_path[self.cur_idx]

	def previousFile(self):
		self.cur_idx -= 1
		self.cur_idx = self.safeLimit(self.cur_idx)
		return self.files_path[self.cur_idx]

	def getCurFilePath(self):
		return self.files_path[self.cur_idx]

	def safeLimit(self, idx):
		if idx > self.file_cnt-1:
			return self.file_cnt-1
		elif idx < 0:
			return 0
		else:
			return idx

	def __repr__(self):
		for item in self.__dict__.items():
			print("%s : %s" % item)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("files_path_arg", help="Path of files", type=str)
	args = parser.parse_args()
	flist = FileList(args.files_path_arg)

	# flist = FileList("/home/zhehua/Github/Enchain/libs")
	# for item in flist.getFilesPathList():
	# 	print(item)