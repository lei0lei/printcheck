import cv2
import imutils
import numpy as np
import math
import time
import os

def align_images(image, template, maxFeatures=3000,
                 keepPercent=0.2, debug=False):
    """align image with template

    Args:
        image (_type_): 要对齐的图片
        template (_type_): 模板图片
        maxFeatures (int, optional): _description_. Defaults to 3000.
        keepPercent (float, optional): _description_. Defaults to 0.2.
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        ndarray: 对齐后的图片
    """     
    # use grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    
    # match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)
 
    matchesort = sorted(matches, key=lambda x: x.distance)

    keep = int(len(matchesort) * keepPercent)
    matches = matchesort[:keep]

    # if debug:
    #     matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,
    #                                  matches, None)
    #     matchedVis = imutils.resize(matchedVis, width=1000)
    #     cv2.imshow("Matched Keypoints", matchedVis)
    #     cv2.waitKey(0)

    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")

    for (i, m) in enumerate(matches):
        # indicate that the two keypoints in the respective images
        # map to each other
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt

    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)

    (h, w) = template.shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    
    return aligned



def align_check(img, template):
    """check if img is aligned to template

    Args:
        img (ndarray): 测试图片
        template (ndarray): 模板图片

    Returns:
        Bool: True/False
    """    
    aligned = False
    
    return aligned


if __name__ == "__main__":
    templatepath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmp/2022-10-11'
    testimgpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmptest'
    
    ims = os.listdir(testimgpath)
    im = cv2.imread(os.path.join(testimgpath, ims[4]))
    template = os.listdir(templatepath)
    templateim = cv2.imread(os.path.join(templatepath,template[4]))
    
    align_images(im, templateim)
    