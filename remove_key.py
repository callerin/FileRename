import os
from MoveFile import my_print
from send2trash import send2trash


def removeKey(file_path: str, keyword: tuple) -> None:
	"""
	删除文件夹(path)内部含有部分字段(keyword)的文件,并打印出来
	Args:
		file_path:           文件夹路径
		keyword:        需要删除文件的关键字

	Returns:            None

	"""
	file_remove = []

	for root, dirs, files in os.walk(file_path):
		for file in files:
			file_src = os.path.join(root, file)
			if any(name in file for name in keyword):
				try:
					send2trash(file_src)
					file_remove.append(file)
				except Exception as e:
					print(e)
				continue

	my_print(file_remove, 'is send2trash')


if __name__ == "__main__":

	# file_path = r'D:\Download\Baidu'
	filepath = r'R:\Download'

	end = ('diz', 'nfo', 'exe', 'BANNER', 'txt')

	removeKey(filepath, end)
