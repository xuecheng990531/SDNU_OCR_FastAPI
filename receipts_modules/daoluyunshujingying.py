from paddleocr import PaddleOCR
import re


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
            return a[0]
        elif '字' in value[i] and '许可' in value[i]:
            if value[i].split('字')[1]!="":
                return [str(s) for s in re.findall(r'-?\d+\.?\d*', value[i])][0]

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
        if '有限责任' in value[i]:
            if '：' in value[i]:
                return value[i].split(':')[1]
            else:
                return value[i]
        elif '无限公司' in value[i]:
            if '：' in value[i]:
                return value[i].split('：')[1]
            else:
                return value[i]
        elif '股份有限' in value[i]:
            if '：' in value[i]:
                return value[i].split('：')[1]
            else:
                return value[i]
        elif '股份两合' in value[i]:
            if '：' in value[i]:
                return value[i].split('：')[1]
            else:
                return value[i]
        elif '国有' in value[i]:
            if '：' in value[i]:
                return value[i].split('：')[1]
            else:
                return value[i]

def match_jingyingfanwei(pos,value):
    for i in range(len(pos)):
        if '范围' in value[i]:
            fanwei_pos=pos[i]
            if value[i].split('围')[1]!="" and len(value[i].split('围')[1])>2:
                print(value[i][4:])
                return value[i][4:]
            else:
                for index in range(len(pos)):
                    if fanwei_pos[2][0]<pos[index][0][0]<fanwei_pos[2][0]+60 and fanwei_pos[0][1]-40<pos[index][0][1]<fanwei_pos[0][1]+40:
                        return value[index]

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