import sys, fitz
import os
from paddleocr import PaddleOCR



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
        # [[62.0, 458.0], [611.0, 458.0], [611.0, 481.0], [62.0, 481.0]]
        if 400 < pos[i][1][0]-pos[i][0][0] < 650 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 380 < pos[i][0][1] < 520 and 30 < pos[i][0][0] < 90:
            if '：' in value[i]:
                print(value[i].split('：')[1].split('/')[0])
                value[i].split('：')[1].split('/')[0]
            else:
                print(value[i].split('/')[0])
                return value[i].split('/')[0]


def match_hangci(pos, value):
    for i in range(len(pos)):
        # [[62.0, 458.0], [611.0, 458.0], [611.0, 481.0], [62.0, 481.0]]
        if 400 < pos[i][1][0]-pos[i][0][0] < 650 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 380 < pos[i][0][1] < 520 and 30 < pos[i][0][0] < 90:
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
        


if __name__ == '__main__':
    value_all=[]
    pos_all=[]

    img_list=['save_files/DB_aabgefejbafe0x0102_0.png','save_files/DB_aabgefejbafe0x0102_1.png','save_files/DB_aabgefejbafe0x0102_2.png']
    for i in range(len(img_list)):
        dict = OCR(img_list[i])
        pos = dict[0]
        value = dict[1]
        value_all.extend(value)
        pos_all.extend(pos)
    
    print('----------------------------------------------------------------')
    print(value_all)
    print('----------------------------------------------------------------')
    # match_hangming(pos,value)
    # match_hangci(pos,value)
    # match_tidanhao(pos,value)