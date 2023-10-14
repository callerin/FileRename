# python3
# -*- coding: utf-8 -*-
# Created by calle on 2021/1/1
# Copyright (c) 2021 calle. All rights reserved.


import os
import re
import sys
import time
import logging
import argparse
from shutil import move
from send2trash import send2trash

# from playsound import playsound

# logging.disable(logging.INFO)
# logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s - %(message)s")

file_remove = []
count = 0
MinSize = 300


def move_file(origin: str, destination: list, filetype: tuple = (
        '.mp4', '.jpg', '.nfo', '.MP4'), send_trash=True):
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
    del_deny = ('fanart', 'poster', 'landscape', '.tmp',
                '.mkv', '.nfo', 'poster', 'landscape')

    for root, dirs, files in os.walk(origin):
        for file in files:
            if file + '.aria2' in files:
                file_downloading.append(file)
                continue

            if file.endswith('.aria2'):
                continue

            file_src = os.path.join(root, file)
            file_des = os.path.join(destination, file_src.split('\\')[-1])
            try:
                file_size = os.path.getsize(file_src) / (1024 * 1024)  # 返回 MB
            except Exception as e:
                logging.error(f'get file size error {e}')

            if send_trash and file_size < MinSize:
                del_flag = True
                if 'IMAGESET' in root or 'IMAGESET' in file :
                    continue

                for arg in del_deny:
                    if arg in file_src:
                        del_flag = False
                        break

                if del_flag:
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

                des_split = destination.split('\\')[-1]
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
                    rename_file(file_des)
                # playsound(
                #     'd:/Data/User/Python/Practice/source/download-complete.wav')

                except Exception as e:
                    # os.remove(os.path.join(file, file_des))
                    logging.info(f'\n\n{e}')

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
    file_path = os.path.split(file)[0]
    file_name = os.path.split(file)[1]
    file_sname = os.path.splitext(file_name)[0]
    for pat1 in pattern1:
        for pat2 in pattern2:
            pattern = pat1 + pat2
            if pattern in file_name:
                series = pattern.replace(pat1, '-CD')
                result = file_name.replace(pattern, series)
                if pat2 in number:
                    result = result.replace(pat2, number[pat2])

                len_part = len(pattern) - 1
                temp_name = file_sname[:-len_part]
                des_path = os.path.join(file_path, temp_name)
                if not os.path.exists(des_path):
                    os.mkdir(des_path)

                des = os.path.join(des_path, result)
                move(file, des)
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


def run_period(origin_destination: str, destination: list,
               minutes: float, run_time: int) -> None:
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
                  filetype=('.mp4', '.mkv', '.wmv', 'avi'))
        remove_null_dirs(origin_destination)
        time.sleep(int(minutes * 60))


def open_player(filepath: str):
    cmd_open = 'PotPlayerMini64.exe ' + filepath
    r = os.popen(cmd_open)
    r.close()


def main():
    parser = argparse.ArgumentParser(description='Organize video files.')
    parser.add_argument('-o', '--src_dir', type=str, default='./', help='Source directory.')
    parser.add_argument('-d', '--dest_dir', type=str, default='./', help='Destination directory.')
    parser.add_argument('-p', '--openpot', type=bool, default=False, help='Open Potplayer.')

    args = parser.parse_args()

    global OpenPot

    src_dir = os.path.abspath(args.src_dir)
    dest_dir = os.path.abspath(args.dest_dir)
    OpenPot = args.openpot

    file_end = ('.mp4', '.jpg', '.wmv', '.mov', '.mkv', 'avi')

    print(time.strftime("%b-%d %A %H:%M:%S") + '\n')

    print(f"OpenPot:{OpenPot}")

    run_period(src_dir, dest_dir, 0.3, 10000)
    print('\nMoved {0} files\n'.format(count))


if __name__ == '__main__':
    main()
