import sys, fitz
from tkinter.messagebox import RETRY
import os
import re
from paddleocr import PaddleOCR
from urllib3 import Retry



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


# OCR识别
def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    pos = []
    value = []
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos, value


def match_hangming(pos, value):
    for i in range(len(pos)):
        if '请不要凭此订舱确认提箱' in value[i]:
            return "None"
        else:
            # [[62.0, 458.0], [611.0, 458.0], [611.0, 481.0], [62.0, 481.0]]
            if '(Vessel)' in value[i]:
                print(value[i+1].split('/')[0])
                return value[i+1].split('/')[0]

            elif 400 < pos[i][1][0]-pos[i][0][0] < 650 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 380 < pos[i][0][1] < 520 and 30 < pos[i][0][0] < 90 and value[i]!="":
                if '：' in value[i]:
                    print(value[i].split('：')[1].split('/')[0])
                    value[i].split('：')[1].split('/')[0]
                else:
                    print(value[i].split('/')[0])
                    return value[i].split('/')[0]


def match_hangci(pos, value):
    for i in range(len(pos)):
        if '请不要凭此订舱确认提箱' in value[i]:
            return "None"
        else:
            if '(Vessel)' in value[i]:
                print(value[i+1].split('//')[1])
                return value[i+1].split('//')[1]
            # [[62.0, 458.0], [611.0, 458.0], [611.0, 481.0], [62.0, 481.0]]
            elif 400 < pos[i][1][0]-pos[i][0][0] < 650 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 380 < pos[i][0][1] < 520 and 30 < pos[i][0][0] < 90 and value[i]!="":
                if '：' in value[i]:
                    print(value[i].split('：')[1].split('/')[1])
                    return value[i].split('：')[1].split('/')[1]
                else:
                    print(value[i].split('/')[1])
                    return value[i].split('/')[1]
        

def match_tidanhao(pos,value):
    for i in range(len(pos)):
        # [[225.0, 151.0], [363.0, 151.0], [363.0, 175.0], [225.0, 175.0]]
        if 80 < pos[i][1][0]-pos[i][0][0] < 200 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 90 < pos[i][0][1] < 200 and 170 < pos[i][0][0] < 300:
            print(value[i])
            return value[i]
        
def match_xiangxing(pos,value):
    for i in range(len(pos)):
        if 'DRY' in value[i]:
            if value[i].split('D')[0]!="":
                return value[i].split('D')[1]
            else:
                return value[i]
        # # [[232.0, 1268.0], [298.0, 1268.0], [298.0, 1286.0], [232.0, 1286.0]]
        # elif 30 < pos[i][1][0]-pos[i][0][0] < 100 and 5 < pos[i][2][1]-pos[i][0][1] < 30  and 1000 < pos[i][0][1] < 1500 and 170 < pos[i][0][0] < 300:
        #     s2 = ''.join(re.findall(r'[A-Za-z]', value[i]))
        #     print(s2)
        #     return s2

def match_zhongliang(pos,value):
    for i in range(len(pos)):
        # [[584.0, 1268.0], [699.0, 1268.0], [699.0, 1288.0], [584.0, 1288.0]]
        # if 90 < pos[i][1][0]-pos[i][0][0] < 180 and 5 < pos[i][2][1]-pos[i][0][1] < 30  and 1250 < pos[i][0][1] < 1300 and 540 < pos[i][0][0] < 700:
        #     print(value[i])
        #     return value[i]
        if 'KGS' in value[i]:
            return value[i]

def match_chaozhongxiang(pos,value):
    return "None"

def match_mudigang(pos,value):
    for i in range(len(pos)):
        # [[820.0, 230.0], [1004.0, 230.0], [1004.0, 253.0], [820.0, 253.0]]
        if 160 < pos[i][1][0]-pos[i][0][0] < 280 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 160 < pos[i][0][1] < 300 and 750 < pos[i][0][0] < 900:
            print(value[i])
            return value[i]

def match_zhongzhuangang(pos,value):
    return "None"

def match_huoming(pos,value):
    return "None"

def match_jianshu(pos,value):
    for i in range(len(pos)):
        if 'Piece(s)' in value[i]:
            return value[i]
        # [[779.0, 1267.0], [861.0, 1267.0], [861.0, 1291.0], [779.0, 1291.0]]
        # if 40 < pos[i][1][0]-pos[i][0][0] < 110 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 1000 < pos[i][0][1] < 1400 and 700 < pos[i][0][0] < 900:
        #     print(value[i])
        #     return value[i]
def match_chicun(pos,value):
    for i in range(len(pos)):
        # [[232.0, 1268.0], [298.0, 1268.0], [298.0, 1286.0], [232.0, 1286.0]]
        # if 30 < pos[i][1][0]-pos[i][0][0] < 100 and 5 < pos[i][2][1]-pos[i][0][1] < 30  and 1000 < pos[i][0][1] < 1500 and 170 < pos[i][0][0] < 300:
        #     print(value[i+1])
        #     return value[i+1]
        if 'DRY' in value[i]:
            if value[i].split('Y')[1]!="":
                return value[i].split('Y')[1]
            else:
                return value[i+1]

def match_wendu(pos,value):
    return '该单据未指定温度'

def match_shidu(pos,value):
    return '该单据未指定湿度'

def match_weixiandengji(pos,value):
    for i in range(len(pos)):
        if 'IMO Class' in value[i]:
            print(pos[i])

def match_weixianfudengji(Pos,value):
    return '该单据没有副等级划分'

def match_weiguihao(pos,value):
    return "None"

def match_xuqiu(pos,value):
    return "None"

if __name__ == '__main__':

    dict = OCR('save_files/216039218_0.png')
    pos = dict[0]
    value = dict[1]
    
    print('----------------------------------------------------------------')
    print(value)
    print('----------------------------------------------------------------')
    match_hangming(pos,value)
    match_hangci(pos,value)
    match_tidanhao(pos,value)
    match_xiangxing(pos,value)
    match_zhongliang(pos,value)
    match_chaozhongxiang(pos,value)
    match_mudigang(pos,value)
    match_huoming(pos,value)
    match_jianshu(pos,value)
    match_chicun(pos,value)
    match_wendu(pos,value)
    match_shidu(pos,value)
    match_weixiandengji(pos,value)
    match_weixianfudengji(pos,value)
