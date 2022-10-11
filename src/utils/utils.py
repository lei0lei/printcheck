import os
from pathlib import Path
import shutil

def file_monitor(path):
    pass


def checkfile(file):
    """check if file exists

    Args:
        file (string): 文件路径字符串

    Returns:
        Bool: True/False
    """    
    exists = False
    my_file = Path(file)
    if my_file.is_file():
        exists = True
        
    return exists
    
def checkdir(dir, mode):
    """check dir exist

    Args:
        dir (string): 目录路径
        mode (int): 0: 检测路径是否存在
                    1: 检测路径是否存在，存在则删除重建，不存在则创建
                    2： 检测路径是否存在，存在则直接返回，不存在则创建

    Returns:
        Bool: True/False
    """    
    exists = False
    my_file = Path(dir)
    if mode == 0:
        # if exist return True
        if my_file.is_dir():
            exists = True
        return exists
    elif mode == 1:
        # if exist, remove and mkdir,return True
        if my_file.is_dir():
            exists = True
            shutil.rmtree(dir)
            
        os.mkdir(dir)
        return True
    elif mode == 2:
        # if exist, return ,else make dir
        if my_file.is_dir():
            exists = True
        else:
            os.mkdir(dir)
            exists = True
        return exists