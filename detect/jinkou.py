
import sys, fitz
import os
import datetime
import cv2
import time
import paddle

from paddleocr import PPStructure,draw_structure_result,save_structure_res,PaddleOCR, draw_ocr
from typing import Optional
'''
#PDF2img
def pdf2img(pdfPath, imagePath):
    print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_%s.png' % pg)#将图片写入指定的文件夹内
'''

#OCR识别
def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value


def match_bianhao(pos,value):
    for i in range(len(pos)):
        if '预录入编号' in value[i]:
            return value[i].split('：')[-1]
            #print('预录入编号:',value[i][0].split('：')[-1])

def match_shouhuoren(pos,value):
    for i in range(len(pos)):

        if '境内收货人' in value[i]:
            for i in range(len(pos)):
                #[[86.0, 296.0], [351.0, 296.0], [351.0, 313.0], [86.0, 313.0]]
                if 100 < pos[i][1][0]-pos[i][0][0] < 300 and 10 < pos[i][2][1]-pos[i][0][1] < 30  and 280 < pos[i][0][1] < 320 and 70 < pos[i][0][0] < 100:
                    return value[i]
                    #print('境内收货人:',value[i])
                    break

def match_shenbaoriqi(pos,value):
    for i in range(len(pos)):
        if '申报日期' in value[i]:
            for i in range(len(pos)):
                if 60 < pos[i][1][0]-pos[i][0][0] < 160 and 10 < pos[i][2][1]-pos[i][0][1] < 25  and 190 < pos[i][0][1] < 210 and 900 < pos[i][0][0] < 1100:
                    return value[i]
                    #print('申报日期:',value[i][0])
                    break

def match_jinjingguanbie(pos,value):
    for i in range(len(pos)):
        if '进境关别' in value[i]:
            #print(pos[i])#[517.0, 226.0, 608.0, 226.0, 608.0, 244.0, 517.0, 244.0]
            #[1038.0, 249.0, 1147.0, 249.0, 1147.0, 266.0, 1038.0, 266.0]
            for i in range(len(pos)):
                if 60 < pos[i][1][0]-pos[i][0][0] < 160 and 10 < pos[i][2][1]-pos[i][0][1] < 25  and 198 < pos[i][0][1] < 210 and 500 < pos[i][0][0] < 700:
                    return value[i]
                    #print('进境关别:',value[i][0])
                    break

def match_yunshufangshi(pos,value):
    for i in range(len(pos)):
        if '运输方式' in value[i]:
            #print(pos[i])#[517.0, 226.0, 608.0, 226.0, 608.0, 244.0, 517.0, 244.0]
            for i in range(len(pos)):
                if 60 < pos[i][1][0]-pos[i][0][0] < 160 and 10 < pos[i][2][1]-pos[i][0][1] < 25  and 230 < pos[i][0][1] < 250 and 500 < pos[i][0][0] < 700:
                    return value[i]
                    # print('运输方式:',value[i][0])
                    break

def match_tiyundanhao(pos,value):
    for i in range(len(pos)):
        if '提运单号' in value[i]:
            #print(pos[i])#[517.0, 226.0, 608.0, 226.0, 608.0, 244.0, 517.0, 244.0]
            #[1038.0, 249.0, 1147.0, 249.0, 1147.0, 266.0, 1038.0, 266.0]
            for i in range(len(pos)):
                if 60 < pos[i][1][0]-pos[i][0][0] < 160 and 10 < pos[i][2][1]-pos[i][0][1] < 25  and 230 < pos[i][0][1] < 250 and 900 < pos[i][0][0] < 1100:
                    return value[i]
                    # print('提运单号:',value[i][0])
                    break

def match_shenbaodanwei(pos,value):
    for i in range(len(pos)):
        if '申报单位' in value[i]:
            return value[i][4:]
            # print('申报单位:',value[i][0][4:])
            break

if __name__=='__main__':
    dict=OCR('save_files/images_0.png')
    pos=dict[0]
    value=dict[1]
    print(value)
    result=match_shenbaoriqi(pos, value)
    print(result)