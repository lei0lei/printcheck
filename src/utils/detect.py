'''Main process of detect difference
'''
import os
import cv2
from natsort import natsorted, ns
from align import align_images
from algos import detect_variance_ssim

def detect_difference(testim, templateim, cfg):
    """_summary_

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




def run():
    pass


if __name__ == '__main__':
    templatepath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmp/2022-10-11'
    testimgpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmptest'
    
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
    