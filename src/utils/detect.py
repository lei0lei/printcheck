'''Main process of detect difference
'''
import os
import cv2
from natsort import natsorted, ns
from align import align_images
from algos import detect_variance_ssim
from utils import checkfile, checkdir
from pdf2jpg import pdf_to_img
import time 
from watchdog.observers import Observer
# from utils import FileHandler
from watchdog.events import FileSystemEventHandler
from pathlib import Path   
    
def detect_difference(testim, templateim, cfg):
    """detect difference for two images

    Args:
        testim (string): 待测图片路径
        templateim (string): 标准图片路径
        cfg (dict): 算法参数

    Returns:
        contours: 区域边界
        hierarchy: 区域边界
    """    
    im = cv2.imread(testim)
    templateim = cv2.imread(templateim)
    
    templateGray = cv2.cvtColor(templateim, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.bilateralFilter(templateGray, 30, 75,75)
    aligned = align_images(im, templateim)
    alignedGray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    alignedGray = cv2.bilateralFilter(alignedGray, 30, 75,75)
    
    ssim_cfg = {
        "thresh": 40,
        "kernel": [3, 3],
        "dilate_ite": 7,
    }
    
    difference = detect_variance_ssim(alignedGray, templateGray, ssim_cfg)
    cv2.imwrite('roi.jpg', difference)
    contours, hierarchy = cv2.findContours(difference, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(aligned, contours, -1, (0, 0, 255), 3)
    cv2.imwrite('11.jpg', aligned)
    return contours, hierarchy

class FileHandler(FileSystemEventHandler):
    def __init__(self, savepdfpath, savetestpath, saveresultpath, cfg):
        self.testim = savetestpath
        self.tasks = os.listdir(self.testim)
        
        self.templatedir = savepdfpath
        self.cfg = cfg
        self.result = saveresultpath
        
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        print (f'Got event for file {event.src_path}')
        detect_difference(os.path.join(self.testim, event.src_path), 
                          os.path.join(self.templatedir, Path(event.src_path).name), self.cfg)
        print(f'----------')
        return True





def runs(pdfpath, savedir, cfg):
    """run program

    Args:
        pdfpath (string): pdf ifle path
        savedir (string): result save path
        cfg (_type_): cfg dict

    Returns:
        True: detect success
    """    
    assert checkfile(pdfpath), f'wrong input pdf path'
    checkdir(savedir, 1)
    assert checkdir(savedir, 0), f'save dir not exists'
    
    savepdfpath = os.path.join(savedir,'pdf')
    savetestpath = os.path.join(savedir,'test')
    saveresultpath = os.path.join(savedir,'result')
    savecfgpath = os.path.join(savedir,'cfg')
    
    # 创建结果保存路径
    checkdir(savepdfpath, 1)
    checkdir(savetestpath, 1)
    checkdir(saveresultpath, 1)
    checkdir(savecfgpath, 1)
    
    # pdf拆分
    pdf_to_img(pdfpath, savepdfpath)

    tasks = os.listdir(savetestpath)
    
    if len(tasks)>0:
        for k, task in enumerate(tasks):
            testim = os.path.join(savetestpath, task)
            templateim = os.path.join(savepdfpath, task)
            
            detect_difference(testim, templateim, {})
        
    
    # 逐文件检测
    observer = Observer()
    cfg = {}
    
    event_handler = FileHandler(savepdfpath, savetestpath, saveresultpath, cfg)
    observer.schedule(event_handler, path=savetestpath)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    return True

if __name__ == '__main__':
    templatepath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmp'
    testimgpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmptest'
    pdfpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/test.pdf'
    
    runs(pdfpath, templatepath, {})
    # pdf_to_img(pdfpath, templatepath)
    # ims = os.listdir(testimgpath)
    # ims = natsorted(ims)
    # im = cv2.imread(os.path.join(testimgpath, ims[3]))
    # template = os.listdir(templatepath)
    # template = natsorted(template)
    # templateim = cv2.imread(os.path.join(templatepath,template[3]))
    # # templateim = cv2.bilateralFilter(templateim, 15, 75,75)
    # # imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # templateGray = cv2.cvtColor(templateim, cv2.COLOR_BGR2GRAY)
    # templateGray = cv2.bilateralFilter(templateGray, 30, 75,75)
    # aligned = align_images(im, templateim)
    # alignedGray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    # alignedGray = cv2.bilateralFilter(alignedGray, 30, 75,75)
   
    # ssim_cfg = {
    #     "thresh": 40,
    #     "kernel": [3, 3],
    #     "dilate_ite": 7,
    # }
    
    # difference = detect_variance_ssim(alignedGray, templateGray, ssim_cfg)
    # cv2.imwrite('roi.jpg', difference)
    # contours, hierarchy = cv2.findContours(difference, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(aligned, contours, -1, (0, 0, 255), 3)
    # cv2.imwrite('contour.jpg', aligned)
    