import cv2
from skimage.metrics import structural_similarity
import numpy as np
import os

def detect_variance_ssim(imgGray, templateGray, ssim_cfg):
    """detect different area

    Args:
        imgGray (_type_): 灰度测试图像
        templateGray (_type_): 灰度标准图像
        ssim_cfg (_type_): ssim参数

    Returns:
        ndarray: 有偏差区域的roi
    """    
    (score, diff) = structural_similarity(imgGray, 
                                          templateGray, 
                                          full=True)
    diff = (diff * 255).astype("uint8")

    thresh0 = cv2.threshold(diff, 
                            ssim_cfg["thresh"], 
                            255, 
                            cv2.THRESH_BINARY)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                       (ssim_cfg["kernel"][0], 
                                        ssim_cfg["kernel"][1]))

    thresh1 = cv2.dilate(thresh0, 
                         kernel, 
                         iterations=ssim_cfg["dilate_ite"])
    thresh = cv2.bitwise_not(thresh1)

    return thresh

