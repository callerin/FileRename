# python3
# -*- coding: utf-8 -*-
# Created by calle on 2021/1/1
# Copyright (c) 2021 calle. All rights reserved.

import os
from shutil import move


def move_file(origin, destination, filetype=('.mp4', '.jpg', '.nfo')):
	"""
	移动文件夹下所有符合要求的文件到另一文件夹

	Args:
			origin (str):           	待转移文件夹位置
			destination ([type]):   	目标文件夹
			filetype (tuple, optional): 文件后缀. Defaults to ('.mp4', '.jpg', '.nfo').
	"""

	count = 0
	for foldername, subfolder, filename in os.walk(origin):
		for file in filename:
			file_src = os.path.join(foldername, file)
			file_src = rename_file(file_src)
			file_des = os.path.join(destination, file_src.split('\\')[-1])
			if file_src.endswith(filetype):
				if os.path.exists(file_des):
					print('Failed {0} is exist'.format(file_src))
					continue
				move(file_src, destination)
				count += 1
				print('Success {0} is moved to {1}'.format(
					file_src.split('\\')[-1], destination.split('\\')[-1]))

	print('Moved {0} files to {1}'.format(count, destination.split('\\')[-1]))


def rename_file(file):
	"""
	:param file: 文件绝对路径及名称
	:return:
	"""
	pattern1 = ['_', '-']
	pattern2 = ['1.', '2.', '3.', '4.', 'A.', 'B.', 'C.', 'D.']
	number = {
		'A.': '1.',
		'B.': '2.',
		'C.': '3.',
		'D.': '4.',
	}

	result = file
	for pat1 in pattern1:
		for pat2 in pattern2:
			pattern = pat1 + pat2
			if pattern in file:
				series = pattern.replace(pat1, '-part')
				result = file.replace(pattern, series)
				if pat2 in number:
					result = result.replace(pat2, number[pat2])
				os.rename(file, result)
				print("{} renamed {}".format(
					file.split('\\')[-1], result.split('\\')[-1]))
				break

	return result


if __name__ == '__main__':
	ori = r'D:\Download\QQDownload\aria2'
	des = r'D:\Download\QQDownload\Single'
	file_end = ('.mp4', '.nfo')

	if not os.path.exists(des):
		os.makedirs(des)

	move_file(ori, des, file_end)
