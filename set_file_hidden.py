from calendar import c
import os
import win32api
import win32con
import logging

# logging.disable(logging.INFO)
# logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def win_hidden(filepath: str, ftype=('.jpg', '.nfo'), hidden=True):  # 设置文件为隐藏 True 隐藏文件，False 显示文件
	if hidden:
		file_attr = win32con.FILE_ATTRIBUTE_HIDDEN
		message = 'hidden'
	else:
		file_attr = win32con.FILE_ATTRIBUTE_NORMAL
		message = 'normal'

	for root, dirs, files in os.walk(filepath):
		for file in files:
			try:
				file_src = os.path.join(root, file)
				attr = win32api.GetFileAttributes(file_src)
				if file_src.endswith(ftype) and attr != file_attr:
					win32api.SetFileAttributes(
						file_src, file_attr)
					logging.info(f'{file} is {message}')
			except Exception as e:
				logging.error(f'set file hidden error{e}')
				continue


if __name__ == '__main__':
	file_type = ('.jpg', '.nfo')
	filepath = r'R:\aria2'
	win_hidden(filepath, file_type, False)
