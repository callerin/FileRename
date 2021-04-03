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
	
	dest = find_dest(fpath)
	dirs = []
	for i in range(deep - 1):
		for name in dest:
			temp = find_dest(name)
			if i == deep - 2:
				dirs.extend(temp)
			else:
				dest.extend(temp)
	
	for dirname in dirs:
		print('{} is send2trash '.format(dirname))
		send2trash.send2trash(dirname)


def find_dest(fpath: str) -> list:
	dest = []
	dirlist = os.listdir(fpath)
	for dir in dirlist:
		dest.append(os.path.join(fpath, dir))
	# print(dest)
	
	return dest


clean_dir(r'D:\Download\EU\Move',2)
