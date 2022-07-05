from curses.ascii import isdigit
from random import random
import re
from typing import ValuesView
from paddleocr import PaddleOCR
from LAC import LAC
lac = LAC(mode="lac")

zhunjia=['A1','A2','A3','B1','B2','C1','C2','C3','C4','D','E','F','M','N','P']

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value

def match_name(pos,value):
    user_name_lis = []
    for i in range(len(pos)):
            _result = lac.run(value[i])
            for _index, _label in enumerate(_result[1]):
                if _label == "PER":
                    user_name_lis.append(_result[0][_index])
    print(user_name_lis[0])
    return user_name_lis[0]

def match_jiashizhenghao(pos,value):
    for i in range(len(pos)):
        if len(value[i])==15 or len(value[i])==18:
            print(value[i])
            return value[i]
        elif '证号' in value[i]:
            if len(value[i])>2:
                print(value[i].split('号')[1])
                return value[i].split('号')[1]
            elif value[i+1].isdigit() and len(value[i+1])>=15:
                print(value[i+1])
                return value[i+1]
            elif value[i-1].isdigit() and len(value[i-1])>=15:
                print(value[i-1])
                return value[i-1]
            
def match_sex(pos,value):
    if ("男" in value):
        # print("nan")
        return "男"
    else:
        # print("nv")
        return "女"


def match_address(pos,value):
    for i in range(len(pos)):
        if ("省" in value[i] and "县" in value[i] or "市" in value[i]):
            print(value[i])
            return value[i]

def match_chexing(pos,value):
    for i in range(len(pos)):
        if value[i] in zhunjia:
            print(value[i])
            return value[i]


def match_valid_date(pos,value):
    for i in range(len(value)):
        if '至' in value[i]:
            print(value[i])
            return value[i]


if __name__=='__main__':
    dict=OCR('samples/jiashizheng/21655527733_.pic.jpg')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_name(pos,value)
    match_jiashizhenghao(pos,value)
    match_sex(pos,value)
    match_address(pos,value)
    match_valid_date(pos,value)