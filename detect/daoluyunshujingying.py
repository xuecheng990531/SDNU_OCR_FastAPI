from paddleocr import PaddleOCR
import re

province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']

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


def match_yunshuzhenghao(pos,value):
    a = []
    for i in range(len(pos)):
        if len(value[i])>6 and value[i][3:8].isdigit():
            a = re.findall("\d+\.?\d*", value[i])
            print(a[0])
            return a[0]
        elif '字' in value[i]:
            if value[i].split('字')[1]!="":
                print([int(s) for s in re.findall(r'-?\d+\.?\d*', value[i])][0])
                return [int(s) for s in re.findall(r'-?\d+\.?\d*', value[i])][0]
        elif '号' in value[i]:
            if len(value[i])>2:
                print([int(s) for s in re.findall(r'-?\d+\.?\d*', value[i])][0])
                return [int(s) for s in re.findall(r'-?\d+\.?\d*', value[i])][0]

def match_youxiaoqi(pos,value):
    for i in range(len(pos)):
        if '年' in value[i] and '月' in value[i]:
            print(value[i])
            return value[i]

def match_yehumingcheng(pos,value):
    for i in range(len(pos)):
        # [[990.0, 102.0], [1178.0, 97.0], [1178.0, 126.0], [991.0, 131.0]]
        if '称' in value[i]:
            if value[i].split('称')[1]!="" and len(value[i].split('称')[1])>2:
                print(value[i].split("称")[1])
                return value[i].split("称")[1]
            else:
                print(value[i+1])
                return value[i+1]
        elif 50 < pos[i][1][0]-pos[i][0][0] < 300 and 5 < pos[i][2][1]-pos[i][0][1] < 70  and 50 < pos[i][0][1] < 200 and 300 < pos[i][0][0] < 1300:
            print(value[i])
            return value[i]
            
def match_address(pos,value):
    for i in range(len(pos)):
        if '址' in value[i] and value[i].split('址')[1]!="":
            if '经济性质' not in value[i+1]:
                # print(value[i].split("址")[1])
                print(value[i].split('址')[1]+value[i+1])
                return value[i].split('址')[1]+value[i+1]
            else:
                print(value[i].split('址'))
                return value[i].split('址')

def match_jingjixingzhi(pos,value):
    for i in range(len(pos)):
        # [[993.0, 246.0], [1103.0, 241.0], [1105.0, 273.0], [994.0, 278.0]]
        # if '经济性质' in value[i] and len(value[i])>5:
        #     # print(value[i].split('质')[1])
        #     return value[i].split('质')[1]
        # elif 50 < pos[i][1][0]-pos[i][0][0] < 300 and 5 < pos[i][2][1]-pos[i][0][1] < 70  and 200 < pos[i][0][1] < 300 and 850 < pos[i][0][0] < 1200:
        #     if '经济性质' in value[i]:
        #         print(value[i].split('质')[1])
        #         return value[i].split('质')[1]
        #     else:
        #         print(value[i])
        #         return value[i]
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

def match_jingyingfanwei(pos,value):
    for i in range(len(pos)):
        if '经营范围' in value[i]:
            if value[i].split('围')[1]!="" and len(value[i].split('围')[1])>2:
                print(value[i][4:])
                return value[i][4:]
            else:
                print(value[i+1])
                return value[i+1]
        elif 250 < pos[i][1][0]-pos[i][0][0] < 450 and 5 < pos[i][2][1]-pos[i][0][1] < 70  and 250 < pos[i][0][1] < 390 and 850 < pos[i][0][0] < 1200:
            print(value[i])
            return value[i]
    

if __name__=='__main__':
    dict=OCR('samples/daoluyunshu/截屏2022-06-22 09.10.15.png')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_yunshuzhenghao(pos,value)
    match_yehumingcheng(pos,value)
    match_address(pos,value)
    match_jingjixingzhi(pos,value)
    match_jingyingfanwei(pos,value)
    match_youxiaoqi(pos,value)