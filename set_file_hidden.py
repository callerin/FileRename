from calendar import c
import os
import win32api
import win32con
import logging

# logging.disable(logging.INFO)
# logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format=" %(asctime)s - %(levelname)s - %(message)s")


def win_hidden(filepath: str, type: tuple):  # 设置文件为隐藏

	for root, dirs, files in os.walk(filepath):
		for file in files:
			try:
				file_src = os.path.join(root, file)
				attr = win32api.GetFileAttributes(file_src)
				if file_src.endswith(file_type) and attr != win32con.FILE_ATTRIBUTE_HIDDEN:
					win32api.SetFileAttributes(
						file_src, win32con.FILE_ATTRIBUTE_HIDDEN)
					logging.info(f'{file} is hidden')
			except Exception as e:
				logging.error(e)
				continue


if __name__ == '__main__':
	file_type = ('.jpg', '.nfo')
	filepath = r'W:\JAV\QQ2021'
	win_hidden(filepath, file_type)
