'''Main process of detect difference
'''
import os
import cv2
from natsort import natsorted, ns
from align import align_images
from algos import detect_variance_ssim
from utils import checkfile, checkdir
from pdf2jpg import pdf_to_img


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
    
    return contours, hierarchy




def runs(pdfpath, savedir, cfg):
    """run program

    Args:
        pdfpath (string): pdf ifle path
        savedir (string): result save path
        cfg (_type_): cfg dict

    Returns:
        _type_: _description_
    """    
    assert checkfile(pdfpath), f'wrong input pdf path'
    checkdir(savedir, 1)
    assert checkdir(savedir, 0)
    
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

    tasks = os.listdir(savepdfpath)
    # 逐文件检测
    
    
    
    return True

if __name__ == '__main__':
    templatepath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmp'
    testimgpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmptest'
    pdfpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/test.pdf'
    pdf_to_img(pdfpath, templatepath)
    ims = os.listdir(testimgpath)
    ims = natsorted(ims)
    im = cv2.imread(os.path.join(testimgpath, ims[3]))
    template = os.listdir(templatepath)
    template = natsorted(template)
    templateim = cv2.imread(os.path.join(templatepath,template[3]))
    # templateim = cv2.bilateralFilter(templateim, 15, 75,75)
    # imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
    contours, hierarchy = cv2.findContours(difference, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(aligned, contours, -1, (0, 0, 255), 3)
    cv2.imwrite('contour.jpg', aligned)
    