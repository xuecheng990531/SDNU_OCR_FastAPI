from random import randrange
from paddleocr import PaddleOCR
import re
jingyingfanwei=['货运','客运','国际运输','站场','机动车维修','机动车驾驶员培训']
chepai = r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁台琼使领军北南成广沈济空海]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂领学警港澳]{1}(?!\d)'
province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']
id_zhengze=r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value


def match_zhenghao(pos,value):
    for i in range(len(pos)):
        if re.findall(id_zhengze,value[i]):
            print(value[i])
            return value[i]
        elif '号' in value[i]:
            if value[i].split('号')[1]!="" and value[i].split('号')[1][2:8].isdigit():
                if len(value[i].split('号')[1])>=15 and len(value[i].split('号')[1])<=19:
                    print(value[i].split('号')[1])
                    return value[i].split('号')[1]
        elif value[i][2:6].isdigit():
            print(value[i])
            return value[i]

def match_yehumingcheng(pos,value):
    for i in range(len(pos)):
        if '称' in value[i]:
            if value[i].split('称')[1]!="":
                print(value[i].split('称')[1])
                return value[i].split('称')[1]
            elif '公司' in value[i+1]:
                print(value[i+1])
                return value[i+1]
        elif '公司' in value[i+1]:
                print(value[i+1])
                return value[i+1]


def match_dizhi(pos,value):
    for i in range(len(pos)):
        if '省' in value[i] or '市' in value[i] or '区' in value[i]:
            print(value[i])
            return value[i]
        elif '址' in value[i]:
            if value[i].split('址')[1]!="":
                print(value[i].split('址')[1])
                return value[i].split('址')[1]

def match_chepaihaoma(pos,value):
    for i in range(len(pos)):
        all_car_id = re.findall(chepai, value[i])
        car_id = []
        car_id1 = ""
        if all_car_id:
            for i in all_car_id:
                if not i in car_id:
                    car_id.append(i)
            for i in car_id:
                car_id1 = car_id1 + ' ' + "".join(tuple(i))   #将列表转字符串
            print(car_id1)
            return car_id1            #返回字符串

        elif '号牌' in value[i]:
            if len(value[i].split('牌')[1])>3:
                print(value[i].split('牌')[1])
                return value[i].split('牌')[1]

def match_jingyingxukezheng(pos,value):
    for i in range(len(pos)):
        if '许可证号' in value[i]:
            if len(value[i].split('号')[1])>3:
                print(value[i].split('号')[1])
                return value[i].split('号')[1]
            elif value[i+1][3:5].isdigit():
                print(value[i+1])
                return value[i+1]
            
def match_jingyingleixing(pos,value):
    for i in range(len(pos)):
        if '有限责任' in value[i]:
            print(value[i])
            return value[i]
        elif '无限公司' in value[i]:
            print(value[i])
            return value[i]
        elif '股份有限' in value[i]:
            print(value[i])
            return value[i]
        elif '股份两合' in value[i]:
            print(value[i])
            return value[i]

def match_cheliangleixing(pos,value):
    for i in range(len(pos)):
        if '牌' in value[i] and '号' not in value[i]:
            print(value[i])
            return value[i]

def match_dunwei(pos,value):
    for i in range(len(pos)):
        if '吨' in value[i] and value[i].split('吨')[0].isdigit():
            print(value[i])
            return value[i]

def match_chicun(pos,value):
    return -1

if __name__=='__main__':
    dict=OCR('samples/daoluyunshu/截屏2022-06-22 09.10.15.png')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_zhenghao(pos,value)
    match_yehumingcheng(pos,value)
    match_dizhi(pos,value)
    match_chepaihaoma(pos,value)
    match_jingyingxukezheng(pos,value)
    match_jingyingleixing(pos,value)
    match_cheliangleixing(pos,value)
    match_dunwei(pos,value)
    match_chicun(pos,value)