
import json
import os
from utils.run import run
from datetime import datetime
from pynput import keyboard
import toml

def on_press(key):
    if key == keyboard.Key.end:
        print("结束程序")
        os.system('taskkill /f /im DeliCamera.exe')
        os._exit(0)
        return True

def _loadtoml(tomlfile):
    '''
    parse tomlfile
    '''
    print(f'now we hace args')
    args = None
    args = toml.load(tomlfile)
    return args

def _checkdir(dir, mode):
    '''
    check if dir exist
    '''
    if mode == 0:
        # if exist return True
        pass
    elif mode == 1:
        # if exist, remove and mkdir,return True
        pass
    elif mode == 2:
        # if not exist, return False
        pass
    elif mode == 3:
        # if not exist, mkdir and return True
        pass

if __name__ == '__main__':
    
    # 读取配置文件
    args = _loadtoml('./configs/appconfig.toml')

    
    
    
    # 删除多余目录
    
    