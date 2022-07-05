from curses.ascii import isdigit
from pickletools import read_uint1
from random import random
import re

from typing import ValuesView
from paddleocr import PaddleOCR
from LAC import LAC

lac = LAC(mode="lac")

tiaoxingma='^[A-Z0-9]*$'

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr(img_path, cls=False)
    pos = []
    value = []
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos, value

def match_tiaoxingmabianhao(pos,value):
    for i in range(len(pos)):
        if re.match(tiaoxingma,value[i]):
            print(value[i])
            return value[i]

def match_xuqiuhao(pos,value):
    for i in range(len(pos)):
        if "需求号" in value[i]:
            if len(value[i])>3:
                if '：' in value[i]:
                    print(value[i].split('：')[1])
                    return value[i].split('：')[1]
                else:
                    print(value[i].split('号')[1])
                    return value[i].split('号')[1]
            elif len(value[i+1]) and value[i+1].isdigit():
                print(value[i+1])
                return value[i+1]
            else:
                return value[i-1]

def match_fazhan(pos,value):
    for i in range(len(pos)):
        #[[659.0, 472.0], [899.0, 472.0], [899.0, 520.0], [659.0, 520.0]]
        if 200<pos[i][1][0]-pos[i][0][0]<300 and 38<pos[i][2][1]-pos[i][0][1]< 58 and 600 < pos[i][0][0]< 700 and 400 < pos[i][0][1] < 820:
            print(value[i])
            return value[i]

def match_mingcheng(pos,value):
    for i in range(len(pos)):
        # [[554.0, 601.0], [1365.0, 601.0], [1365.0, 657.0], [554.0, 657.0]]
        if 700<pos[i][1][0]-pos[i][0][0]<900 and 40<pos[i][2][1]-pos[i][0][1]< 70 and 500 < pos[i][0][0]< 600 and 500 < pos[i][0][1] < 660 and value[i]!="":
            print(value[i])
            return value[i]
        elif value[i]=="名称" and len(value[i])>2:
            print(value[i].split('称')[1])
            return value[i].split('称')[1]
        elif value[i]=="名称":
            print(value[i+1])
            return value[i+1]

def match_daozhan(pos,value):
    for i in range(len(pos)):
        # [[668.0, 825.0], [911.0, 825.0], [911.0, 885.0], [668.0, 885.0]]
        if 200<pos[i][1][0]-pos[i][0][0]<320 and 30<pos[i][2][1]-pos[i][0][1]< 80 and 600 < pos[i][0][0]< 800 and 760 < pos[i][0][1] < 900:
            print(value[i])
            return value[i]

def match_tuoyun_jingbanren(pos,value):
    for i in range(len(pos)):
        # [[2621.0, 554.0], [2734.0, 554.0], [2734.0, 619.0], [2621.0, 619.0]]
        if 90<pos[i][1][0]-pos[i][0][0]<120 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2400 < pos[i][0][0]< 2700 and 480 < pos[i][0][1] < 600:
            print(value[i])
            return value[i]
def match_tuoyun_shoujihaoma(pos,value):
    for i in range(len(pos)):
        # [[2537.0, 649.0], [2818.0, 649.0], [2818.0, 709.0], [2537.0, 709.0]]
        if 200<pos[i][1][0]-pos[i][0][0]<320 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2400 < pos[i][0][0]< 2700 and 600 < pos[i][0][1] < 800:
            print(value[i])
            return value[i]

def match_shouhuo_jiangbanren(pos,value):
    for i in range(len(pos)):
        # [[2600.0, 911.0], [2747.0, 911.0], [2747.0, 971.0], [2600.0, 971.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2400 < pos[i][0][0]< 2700 and 890 < pos[i][0][1] < 930:
            print(value[i])
            return value[i]

def match_shouhuo_dianhuahaoma(pos,value):
    for i in range(len(pos)):
        # [[2528.0, 1001.0], [2814.0, 1001.0], [2814.0, 1061.0], [2528.0, 1061.0]]
        if 230<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2400 < pos[i][0][0]< 2700 and 990 < pos[i][0][1] < 1100:
            print(value[i])
            return value[i]

def match_huowumingcheng(pos,value):
    huowu=[]
    for i in range(len(pos)):
        # [[151.0, 1400.0], [311.0, 1400.0], [311.0, 1465.0], [151.0, 1465.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1300 < pos[i][0][1] < 1500:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1500 < pos[i][0][1] < 1800:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1800 < pos[i][0][1] < 2100:
            huowu.append(value[i])
    print(huowu)
    return huowu

def match_jianshu(pos,value):
    huowu=[]
    for i in range(len(pos)):
        # [[151.0, 1400.0], [311.0, 1400.0], [311.0, 1465.0], [151.0, 1465.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1300 < pos[i][0][1] < 1500:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1500 < pos[i][0][1] < 1800:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1800 < pos[i][0][1] < 2100:
            huowu.append(value[i])
        
    print(str(len(huowu))+'件')
    return str(len(huowu))+'件'
 
def match_zhongliang(pos,value):
    for i in range(len(pos)):
        # [[1604.0, 1649.0], [1743.0, 1649.0], [1743.0, 1714.0], [1604.0, 1714.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1550 < pos[i][0][0]< 1700 and 1550 < pos[i][0][1] < 1700:
            print(value[i]+"KG")
            return value[i]+'KG'

def match_xianghao(pos,value):
    xianghao=[]
    for i in range(len(pos)):
        # [[2171.0, 1387.0], [2449.0, 1387.0], [2449.0, 1448.0], [2171.0, 1448.0]]
        if 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1100 < pos[i][0][1] < 1480:
            xianghao.append(value[i])
        elif 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1480 < pos[i][0][1] < 1680:
            xianghao.append(value[i])
        elif 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1680 < pos[i][0][1] < 1700:
            xianghao.append(value[i])

    print(xianghao)
    return xianghao

def match_shifenghao(pos,value):
    shifenghao=[]
    for i in range(len(pos)):
        if 10<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2449 < pos[i][0][0]< 2640 and 1100 < pos[i][0][1] < 1480:
            shifenghao.append(value[i])
        elif 10<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2449 < pos[i][0][0]< 2640 and 1480 < pos[i][0][1] < 1680:
            shifenghao.append(value[i])
        elif 10<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2449 < pos[i][0][0]< 2640 and 1680 < pos[i][0][1] < 1700:
            shifenghao.append(value[i])
    print(shifenghao)

def match_quedingzhongliang(pos,value):
    for i in range(len(pos)):
        # [[1604.0, 1649.0], [1743.0, 1649.0], [1743.0, 1714.0], [1604.0, 1714.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1550 < pos[i][0][0]< 1700 and 1550 < pos[i][0][1] < 1700:
            print(value[i]+"KG")
            return value[i]+'KG'

def match_feimu(pos,value):
    feimu=[]
    for i in range(len(pos)):
        # [[1747.0, 1791.0], [1898.0, 1791.0], [1898.0, 1851.0], [1747.0, 1851.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1680 < pos[i][0][1] < 1840:
            feimu.append(value[i])
            # [[1743.0, 1886.0], [2050.0, 1886.0], [2050.0, 1959.0], [1743.0, 1959.0]]
        elif 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1840 < pos[i][0][1] < 2240:
            feimu.append(value[i])
        elif 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1900  < pos[i][0][1] < 2100:
            feimu.append(value[i])

        # [[2734.0, 1787.0], [3171.0, 1787.0], [3171.0, 1847.0], [2734.0, 1847.0]] 这是第二列费目

        elif 300<pos[i][1][0]-pos[i][0][0]<500 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2600 < pos[i][0][0]< 2880 and 1680  < pos[i][0][1] < 2000:
            feimu.append(value[i])
    print(feimu)
    return feimu

def match_feiyongheji(pos,value):
    for i in range(len(pos)):
        # [[2297.0, 2332.0], [2558.0, 2332.0], [2558.0, 2380.0], [2297.0, 2380.0]]
        if 230<pos[i][1][0]-pos[i][0][0]<340 and 30<pos[i][2][1]-pos[i][0][1]< 80 and 2000 < pos[i][0][0]< 2400 and 2200 < pos[i][0][1] < 2400:
            print(value[i])
            return value[i]


def match_shuie(pos,value):
    print('0')
    return 0

def match_jine(pos,value):
    return 0


if __name__ == '__main__':
    dict = OCR('samples/tielu/微信图片_202206061636085.jpg')
    pos = dict[0]
    value = dict[1]
    print(value)
    match_xuqiuhao(pos,value)
    match_fazhan(pos,value)
    match_mingcheng(pos,value)
    match_daozhan(pos,value)
    match_tuoyun_jingbanren(pos,value)
    match_tuoyun_shoujihaoma(pos,value)
    match_shouhuo_jiangbanren(pos,value)
    match_shouhuo_dianhuahaoma(pos,value)
    match_huowumingcheng(pos,value)
    match_jianshu(pos,value)
    match_zhongliang(pos,value)
    match_xianghao(pos,value)
    match_shifenghao(pos,value)
    match_quedingzhongliang(pos,value)
    match_feimu(pos,value)
    match_feiyongheji(pos,value)
    match_shuie(pos,value)