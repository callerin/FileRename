# python3
# -*- coding: utf-8 -*-
# Created by calle on 2021/1/1
# Copyright (c) 2021 calle. All rights reserved.


import os
import re
import sys
import time
import logging
from shutil import move
from send2trash import send2trash

# logging.disable(logging.INFO)
# logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format=" %(asctime)s - %(levelname)s - %(message)s")

file_remove = []
count = 0
MinSize = 300


def move_file(origin: str, destination: list, filetype: tuple = ('.mp4', '.jpg', '.nfo', '.MP4'), send_trash=True):
    """
    移动文件夹下所有符合要求的文件到另一文件夹

    args:
        origin (str):           	待转移文件夹位置
        destination ([type]):   	目标文件夹列表
        filetype (tuple, optional): 文件后缀. defaults to ('.mp4', '.jpg', '.nfo').
    """
    global count
    global file_remove
    global OpenPot

    file_downloading = []
    file_moved = []
    file_exists = []
    file_remove = []

    for root, dirs, files in os.walk(origin):
        for file in files:
            if file + '.aria2' in files:
                file_downloading.append(file)
                continue

            if file.endswith('.aria2'):
                continue

            file_t = file_type(file)
            try:
                file_destination = destination[file_t]
            except Exception as e:
                logging.error(e)
                continue

            file_src = os.path.join(root, file)
            file_src = rename_file(file_src)
            file_des = os.path.join(file_destination, file_src.split('\\')[-1])
            file_size = os.path.getsize(file_src) / (1024 * 1024)  # 返回 MB

            if send_trash and file_size < MinSize:
                file_remove.append(file)
                try:
                    send2trash(file_src)
                except Exception as e:
                    logging.info(e)
                    os.remove(file_src)
                continue

            if file_src.endswith(filetype):
                if os.path.exists(file_des):
                    file_exists.append(file_des)
                    continue

                des_split = file_destination.split('\\')[-1]
                print(f'{file} is moving to {des_split}', end='', flush=True)

                # sys.stdout.flush()
                # sys.stdout.write(f'{file} is moving to {des_split}')
                # sys.stdout.flush()
                try:
                    if OpenPot:
                        open_player(file_src)
                    move(file_src, file_des)
                    file_moved.append(file_src.split(
                        '\\')[-1] + ' is moved to ' + des_split)
                except Exception as e:
                    logging.info(f'\n\n{e}')
                # os.remove(os.path.join(file, file_des))
                print('\r', end='')
                print(120 * ' ', end='')
                print('\r', end='', flush=True)

                count += 1

    my_print(file_moved, '')
    my_print(file_downloading, 'is downloading')
    my_print(file_exists, 'exist')
    my_print(file_remove, 'is send2trash')


def rename_file(file: str) -> str:
    """
    重命名文件
    :param file: 文件绝对路径及名称
    :return:

    """
    pattern1 = ['_', '-']
    pattern2 = ['1.', '2.', '3.', '4.', 'A.', 'B.',
                'C.', 'D.', 'E.', 'a.', 'b.', 'c.', 'd.', 'e.']
    number = {
        'A.': '1.',
        'B.': '2.',
        'C.': '3.',
        'D.': '4.',
        'E.': '5.',
        'a.': '1.',
        'b.': '2.',
        'c.': '3.',
        'd.': '4.',
        'e.': '5.',
    }

    result = file
    for pat1 in pattern1:
        for pat2 in pattern2:
            pattern = pat1 + pat2
            if pattern in file:
                series = pattern.replace(pat1, '.CD')
                result = file.replace(pattern, series)
                if pat2 in number:
                    result = result.replace(pat2, number[pat2])
                os.rename(file, result)
                print("{} renamed {}".format(
                    file.split('\\')[-1], result.split('\\')[-1]))
                break

    return result


def remove_null_dirs(origin_dir: str) -> None:
    """
    删除空文件夹
    Args:
        origin_dir:

    Returns:

    """
    global file_remove

    # topdown=False 递归文件夹深度 由下到上
    for root, dirs, files in os.walk(origin_dir, topdown=False):
        for dir1 in dirs:
            dir_path = os.path.join(root, dir1)
            allfiles = os.listdir(dir_path)
            if len(allfiles) == 0:
                # os.removedirs(dir_path)
                send2trash(dir_path)
                file_remove.append('.\\' + dir_path.split('\\')
                                   [-2] + '\\' + dir_path.split('\\')[-1])
    # file_remove.append(dir_path.split('\\')[-1])
    my_print(file_remove, 'is send2trash')


def file_type(filename: str) -> int:
    """
    判断文件名中是否存在特殊字符
    Args:
            filename:  文件名str

    Returns:
        0   eu
        1   single

    """
    pat = r'\d{2}\.\d{2}\.\d{2}|[4|2]k|2160|1080'
    data = re.search(pat, filename)

    if data:
        # print(data.group())
        return 1
    else:
        return 0


def my_print(files: list, ending: str):
    """
    按照固定格式打印文件列表
    Args:
            files:      待打印文件列表
            ending:     后缀

    Returns:

    """
    if not files:
        return
    print(80 * '-')

    for file in files:
        print(f'{file:60}', ending)


# Todo add the method that write the change to file
def write_change(moved: dict):
    pass


def run_period(origin_destination: str, destination: list, minutes: float, run_time: int) -> None:
    """

    Args:
        origin_destination (object):    文件路径
        destination:    				目标路径
        minutes:   						间隔时间
        run_time:          				运行次数

    Returns:

    """

    for i in range(run_time):
        print(
            f'\n{time.strftime("%b-%d %A %H:%M:%S")}  Running {i + 1} OpenPot:{OpenPot} Complet:{count}')
        move_file(origin_destination, destination,
                  filetype=('.mp4', '.mkv', '.wmv'))
        remove_null_dirs(origin_destination)
        time.sleep(int(minutes * 60))


def open_player(filepath: str):
    cmd_open = 'PotPlayerMini64.exe ' + filepath
    r = os.popen(cmd_open)
    r.close()


if __name__ == '__main__':
    ori = r'D:\Download\aria2'
    aria_2 = 'R:\\aria2'
    des = [r'D:\Download\QQDownload\Single', r'D:\Download\EU']
    file_end = ('.mp4', '.jpg', '.wmv', '.mov', '.mkv', 'avi')

    OpenPot = True
    OpenPot = False

    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            ori = sys.argv[1]
        elif sys.argv[1] in ('0', 'False'):
            OpenPot = False

    elif len(sys.argv) == 3:
        if os.path.isdir(sys.argv[2]):
            des[0] = sys.argv[2]
    elif len(sys.argv) == 4:
        if os.path.isdir(sys.argv[3]):
            des[1] = sys.argv[3]

    for item in des:
        if not os.path.exists(item):
            os.makedirs(item)

    print(time.strftime("%b-%d %A %H:%M:%S") + '\n')

    print(f"OpenPot:{OpenPot}")

    run_period(aria_2, des, 1, 600)
    print('\nMoved {0} files\n'.format(count))
