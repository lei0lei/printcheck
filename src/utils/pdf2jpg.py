import fitz
import os
from utils import checkfile, checkdir
import datetime

def pdf_to_img(pdf_path, orig_dir, start=-1, end=-1):
    """convert pdf to images
        将pdf文件转化成图片，支持页数选择

    Args:
        pdf_path (_type_): pdf文件路径
        orig_dir (_type_): 存放图片的目录
        start (int): 起始页
        end (int): 终止页

    Returns:
        _type_: 图片目录路径字符串
    """    
    # pdffile = "升腾使用说明书.pdf"
    assert checkfile(pdf_path), f'wrong pdf file path'
    assert start<=end, f'wrong pages selection'
    assert checkdir(orig_dir,1), f'wrong image output dir, and cant make dir'
    
    # 尺寸缩放，从300dpi转到72dpi
    dpi = 300
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)
    
    doc = fitz.open(pdf_path)
    pages = os.listdir(orig_dir)
    pdflen = len(doc)
    
    assert len(pages)<1, f'target dir is non empty'
     
    # make tmp save dir
    assert checkdir(os.path.join(orig_dir,str(datetime.date.today())),1)
    for i in range(pdflen):
        page = doc[i]
        pix = page.get_pixmap(matrix=magnify)
        
        # 图片明明采用自然排序
        pix.save(os.path.join(orig_dir,str(datetime.date.today()),f'IMG_{str(i).zfill(4)}.jpg'))
    
    imgpath = orig_dir
    return imgpath      
        
if __name__ == '__main__':
    pdfpath = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/test.pdf'
    outdir = '/home/znzz/Desktop/Data/mfl/CODE/printcheck/tmp'
    pdf_to_img(pdfpath, outdir)
    print(f'hello')