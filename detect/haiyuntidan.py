from logging import root
import sys, fitz
import os
import datetime
import cv2
import time
import paddle

from paddleocr import PPStructure, draw_structure_result, save_structure_res, PaddleOCR, draw_ocr


# #PDF2img
# def pdf2img(pdfPath, imagePath):
#     print("imagePath="+imagePath)
#     pdfDoc = fitz.open(pdfPath)
#     for pg in range(pdfDoc.pageCount):
#         page = pdfDoc[pg]
#         rotate = int(0)
#         # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
#         # 此处若是不做设置，默认图片大小为：792X612, dpi=96
#         zoom_x = 2 #(1.33333333-->1056x816)   (2-->1584x1224)
#         zoom_y = 2
#         mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
#         pix = page.getPixmap(matrix=mat, alpha=False)

#         if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
#             os.makedirs(imagePath) # 若图片文件夹不存在就创建

#         pix.writePNG(imagePath+'/'+'images_%s.png' % pg)#将图片写入指定的文件夹内


# OCR识别
def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos = []
    value = []
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos, value


def match_bianhao(pos, value):
    for i in range(len(pos)):
        if '编号' in value[i]:
            if value[i + 1].isdigit():
                return value[i + 1]
                # print(value[i+1])
                break
            else:
                return value[i][2:]
                # print(value[i].split('：')[-1])
                break


def match_shouhuoren(pos, value):
    for i in range(len(pos)):
        if '收货人' in value[i]:
            for i in range(len(pos)):
                # 下面的坐标是收货人结果的坐标，预留20个坐标的宽容度
                # 收货人结果的坐标[[294.0, 318.0], [585.0, 318.0], [585.0, 340.0], [294.0, 340.0]]
                if 241 < pos[i][1][0] - pos[i][0][0] < 341 and 6 < pos[i][2][1] - pos[i][0][1] < 72 and 288 < pos[i][0][
                    1] < 348:
                    return value[i]
                    # print('收货人:',value[i])
                    break


def match_fahuoren(pos, value):
    for i in range(len(pos)):
        if '发货人' in value[i]:
            for i in range(len(pos)):
                # [[275.0, 396.0], [587.0, 400.0], [587.0, 425.0], [275.0, 421.0]]
                if 214 < pos[i][1][0] - pos[i][0][0] < 414 and 7 < pos[i][2][1] - pos[i][0][1] < 50 and 350 < pos[i][0][
                    1] < 500:
                    return value[i]
                    # print('发货人:',value[i])
                    break


def match_pinming(pos, value):
    for i in range(len(pos)):
        if '品名' in value[i]:
            for i in range(len(pos)):
                # [[288.0, 470.0], [415.0, 474.0], [414.0, 500.0], [287.0, 496.0]]
                if 27 < pos[i][1][0] - pos[i][0][0] < 227 and 2 < pos[i][2][1] - pos[i][0][1] < 80 and 440 < pos[i][0][
                    1] < 500 and 258 < pos[i][0][0] < 318:
                    # print('品名:',value[i])
                    return value[i]
                    break


def match_zhongliang(pos, value):
    for i in range(len(pos)):
        if '报检数/重量' in value[i]:
            for i in range(len(pos)):
                if 65 < pos[i][1][0] - pos[i][0][0] < 265 and 2 < pos[i][2][1] - pos[i][0][1] < 180 and 442 < pos[i][0][
                    1] < 502 and 864 < pos[i][1][0] < 1024:
                    # print('报检数/重量:',value[i])
                    return value[i]
                    break


def match_shuchuguojia(pos, value):
    for i in range(len(pos)):
        if '输出国家或地区' in value[i]:
            if len(value[i]) > 7:
                # print('输出国家或地区:',value[i][7:])
                return value[i][7:]
            else:
                for i in range(len(pos)):
                    if 30 < pos[i][1][0] - pos[i][0][0] < 100 and 5 < pos[i][2][1] - pos[i][0][1] < 50 and 540 < \
                            pos[i][0][1] < 580 and 700 < pos[i][0][0] < 780:
                        # print('输出国家或地区:',value[i][0])
                        return value[i]


def match_jizhuangxiang(pos, value):
    for i in range(len(pos)):
        if '集装箱号' in value[i]:
            if value[i - 1][:8].isalnum():
                # print('集装箱号:',value[i][5:]+value[i+1][0])
                return value[i][5:] + value[i - 1]
                break
            else:
                # print('集装箱号:',value[i][5:])
                return value[i][5:]
                break


def match_shengchanriqi(pos, value):
    for i in range(len(pos)):
        if '生产日期' in value[i]:
            # print('生产日期:',value[i].split('：')[-1])
            return value[i].split('：')[-1]
            break


def match_shengchanchangjia(pos, value):
    for i in range(len(pos)):
        if '生产厂家' in value[i]:
            # print('生产厂家:',value[i][5:])
            return value[i].split('：')[-1]


def match_pinpai(pos, value):
    for i in range(len(pos)):
        if '品牌' in value[i]:
            # print('品牌:',value[i][3:])
            return value[i][3:]


def match_guige(pos, value):
    for i in range(len(pos)):
        if '规格' in value[i]:
            # print('规格:',value[i][3:])
            return value[i][3:]


def match_hetonghao(pos, value):
    for i in range(len(pos)):
        if '合同号' in value[i]:
            for i in range(len(pos)):
                # 下面的坐标是合同号结果的坐标
                # [[289.0, 633.0], [365.0, 633.0], [365.0, 660.0], [289.0, 660.0]]
                if 10 < pos[i][1][0] - pos[i][0][0] < 176 and 5 < pos[i][2][1] - pos[i][0][1] < 127 and 603 < pos[i][0][
                    1] < 663 and 259 < pos[i][0][0] < 319:
                    # print('合同号:',value[i])
                    return value[i]


def match_tiyundanhao(pos, value):
    for i in range(len(pos)):
        # if 'HLCURTM200715342' in value[i]:
        #     print(pos[i])
        if '提/运单号' in value[i]:
            for i in range(len(pos)):
                # 下面的坐标是提/运单号结果的坐标
                # [[288.0, 714.0], [387.0, 718.0], [386.0, 744.0], [287.0, 740.0]]
                # [[268.0, 717.0], [437.0, 721.0], [436.0, 746.0], [268.0, 742.0]]
                if 49 < pos[i][1][0] - pos[i][0][0] < 180 and 1 < pos[i][2][1] - pos[i][0][1] < 30 and 684 < pos[i][0][
                    1] < 744 and 258 < pos[i][0][0] < 318:
                    # print('提/运单号:',value[i])
                    return value[i]
                    break


def match_rujingkouan(pos, value):
    for i in range(len(pos)):
        if '口岸' in value[i]:
            for i in range(len(pos)):
                # 下面的坐标是入境口岸结果的坐标
                # [[289.0, 793.0], [333.0, 793.0], [333.0, 819.0], [289.0, 819.0]]
                if 9 < pos[i][1][0] - pos[i][0][0] < 144 and 5 < pos[i][2][1] - pos[i][0][1] < 126 and 763 < pos[i][0][
                    1] < 823 and 259 < pos[i][0][0] < 319:
                    # print('入境口岸:',value[i])
                    return value[i]
                    break


def match_rujingriqi(pos, value):
    for i in range(len(pos)):
        if '人境日期' in value[i]:
            return value[i + 1]
            break
            # for i in range(len(pos)):
            #     # 下面的坐标是入境口岸结果的坐标
            #     # [[194.0, 583.0], [292.0, 583.0], [292.0, 599.0], [194.0, 599.0]]
            #     # [[287.0, 874.0], [436.0, 874.0], [436.0, 898.0], [287.0, 898.0]]
            #     if 49 < pos[i][1][0]-pos[i][0][0] < 249 and 5 < pos[i][2][1]-pos[i][0][1] < 124  and 834 < pos[i][0][1] < 904 and 257 < pos[i][0][0] < 317:
            #         #print('入境日期:',value[i])
            #         return value[i]
            #         break


def match_biaoji(pos, value):
    for i in range(len(pos)):
        if '标记及号码' in value[i]:
            for i in range(len(pos)):
                if 4 < pos[i][1][0] - pos[i][0][0] < 54 and 4 < pos[i][2][1] - pos[i][0][1] < 51 and 610 < pos[i][0][
                    1] < 670 and 575 < pos[i][0][0] < 635:
                    # print('标记及号码:',value[i])
                    return value[i]
                    break


def match_baozhuangzhonglei(pos, value):
    for i in range(len(pos)):
        if '包装种类及数量' in value[i]:
            for i in range(len(pos)):
                # 下面的坐标是包装种类及数量结果的坐标
                # [[194.0, 368.0], [264.0, 368.0], [264.0, 385.0], [194.0, 385.0]]
                if 10 < pos[i][1][0] - pos[i][0][0] < 307 and 5 < pos[i][2][1] - pos[i][0][1] < 124 and 523 < pos[i][0][
                    1] < 583 and 259 < pos[i][0][0] < 319:
                    # print('包装种类及数量:',value[i])
                    return value[i]
                    break


def match_beizhu(pos, value):
    for i in range(len(pos)):
        if '备注' in value[i]:
            # print('备注:',value[i][2:])
            return value[i][2:]
            break


if __name__ == '__main__':
    # dict = OCR('/Users/xuecheng/Desktop/paddle/samples/OCR_Test/52351656133919_.pic.jpg')
    # print(dict[1])
    # pos = dict[0]
    # value = dict[1]

    root_path='samples/OCR_Test2'
    name=os.listdir(root_path)
    length=len(os.listdir(root_path))
    for i in range(len(name)):
        dict=OCR(os.path.join(root_path,name[i]))
        print('--------------------------------')
        print(dict[1])
