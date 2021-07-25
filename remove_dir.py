import os
import send2trash


def clean_dir(fpath: str, deep: int = 2) -> None:
	"""
	清理指定深度的文件夹，移除文件
	Args:
		fpath:
		deep:

	Returns:

	"""
	
	dest = []
	dirs = []
	dest.append(fpath)
	
	for i in range(deep):
		for name in dest:
			if os.path.isdir(name):
				temp = find_dest(name)
			else:
				continue
			
			if i == deep - 2:
				dirs.extend(temp)
			else:
				dest = temp
	
	for dirname in dirs:
		print('{} is send2trash '.format(dirname))
		send2trash.send2trash(dirname)


def find_dest(f_path: str) -> list:
	dest = []
	dir_list = os.listdir(f_path)
	for dir in dir_list:
		dest.append(os.path.join(f_path, dir))
	# print(dest)
	
	return dest


dir1 = r'D:\Download\Move'

clean_dir(dir1, 3)
