from pickletools import read_uint1
from paddleocr import PaddleOCR
from LAC import LAC
from pydantic import validate_arguments

lac=LAC(mode='lac')

jiagedanwei=["仟","佰","拾","万","仟","佰","拾","元","角","分","整"]

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value

def match_mingcheng(pos,value):
    for i in range(len(pos)):
        # [[464.0, 947.0], [973.0, 947.0], [973.0, 981.0], [464.0, 981.0]]
        # if 400<pos[i][1][0]-pos[i][0][0]<600 and 6<pos[i][2][1]-pos[i][0][1]< 50 and 380 < pos[i][0][0]< 580 and 880 < pos[i][0][1] < 1000:
        #     print(value[i])
        #     return value[i]
        # elif '称' in value[i]:
        #     if len(value[i])>2:
        #         print(value[i].split('称')[1])
        #         return value[i].split('称')[1]
        #     else:
        #         print(value[i+1])
        #         return value[i+1]
        if '公司' or '有限公司' in value[i]:
            print(value[i])
            return value[i]

def match_daima(pos,value):
    for i in range(len(pos)):
        if '代码' in value[i]:
            if len(value[i])>10:
                print(value[i].split('码')[1])
                return value[i].split('码')[1]
            elif value[i+1][2:7].isdigit():
                print(value[i+1])
                return value[i+1]

def match_leixing(pos,value):
    for i in range(len(pos)):
        if '有限责任' in value[i]:
            print(value[i])
            return value[i]
        elif '股份有限责任' in value[i]:
            print(value[i])
            return value[i]
        elif '个人' in value[i]:
            print(value[i])
            return value[i]
        elif '合伙' in value[i]:
            print(value[i])
            return value[i]
        elif '个体工商户' in value[i]:
            print(value[i])
            return value[i]

def match_daibiaoren(pos,value):
    user_name_lis = []
    for i in range(len(pos)):
        _result = lac.run(value[i])
        for _index, _label in enumerate(_result[1]):
            if _label == "PER":
                user_name_lis.append(_result[0][_index])
    print(user_name_lis[0])
    return user_name_lis[0]


def match_zhucechengben(pos,value):
    for i in range(len(pos)):
        for j in range(len(jiagedanwei)):
            if jiagedanwei[j] in value[i]:
                print(value[i])
                return value[i]

def match_chengliriqi(pos,value):
    for i in range(len(pos)):
        if '成立日期' in value[i]:
            if value[i].split('期')[1]!="":
                print(value[i].split('期')[1])
                return value[i].split('期')[1]
            elif value[i+1][:3].isdigit() and '年' in value[i+1]:
                print(value[i+1])
                return value[i+1]

def match_yingyeqixian(pos,value):
    for i in range(len(pos)):
        if '营业期限' in value[i]:
            if value[i].split('限')[1]!="":
                print(value[i].split('限')[1])
                return value[i].split('限')[1]
            elif '年' in value[i+1]:
                if '至' in value[i+1]:
                    print(value[i+1])
                    return value[i+1]
                elif '至' in value[i+2]:
                    if value[i+2].split('至')[1]!="":
                        print(value[i+1]+value[i+2])
                        return value[i+1]+value[i+2]
                    elif value[i+3][:3].isdigit() and '年' in value[i+3]:
                        print(value[i+1]+'至'+value[i+3])
                        return value[i+1]+'至'+value[i+3]
        elif '年' in value[i+1] and '月' in value[i+1] and '至' in value[i+1]:
            print(value[i+1])
            return value[i+1]

def match_jingyingfanwei(pos,value):
    for i in range(len(pos)):
        if '经营范围' in value[i]:
            if value[i].split('围')[1]!="":
                print(value[i].split('围')[1])
                return value[i].split('围')[1]
            else:
                print(value[i+1])
                return value[i+1]

if __name__=='__main__':

    dict=OCR('samples/yingyezhizhao/R-C.jpeg')
    pos=dict[0]
    value=dict[1]
    print(value)
    print("______________________________________________")
    match_mingcheng(pos,value)
    match_daima(pos,value)
    match_leixing(pos,value)
    match_daibiaoren(pos,value)
    match_zhucechengben(pos,value)
    match_chengliriqi(pos,value)
    match_yingyeqixian(pos,value)
    match_jingyingfanwei(pos,value)