import re
from LAC import LAC
from idna import valid_contextj
from paddleocr import PaddleOCR
import pandas as pd

lac=LAC(mode='lac')
VIN='^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$'
Engine_no='^(?![0-9]+)(?![A-Z]+)[0-9A-Z]{7,10}$'
date='^((([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29))\\s+([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']


lists = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "J": 1,
    "K": 2,
    "L": 3,
    "M": 4,
    "N": 5,
    "P": 7,
    "R": 9,
    "S": 2,
    "T": 3,
    "U": 4,
    "V": 5,
    "W": 6,
    "X": 7,
    "Y": 8,
    "Z": 9,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}
df = pd.DataFrame(lists,index=[0])

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value

def match_haoma(pos,value):
    for i in range(len(pos)):
        if value[i][0] in province:
            print(value[i])
            return value[i]
        elif '码' in value[i]:
            if value[i].split('码')[1]!="":
                print(value[i])
                return value[i]
            elif value[i+1][0] in province or value[i+1][1] in province:
                print(value[i+1])
                return value[i+1]

def match_cheliangleixing(pos,value):
    for i in range(len(pos)):
        if '轿车' in value[i]:
            print(value[i])
            return value[i]
        elif '牵引车' in value[i]:
            print(value[i])
            return value[i]
        elif '汽车' in value[i]:
            print(value[i])
            return value[i]
        elif '客车' in value[i]:
            print(value[i])
            return value[i]
        elif '半挂车' in value[i]:
            print(value[i])
            return value[i]
        elif '货车' in value[i]:
            print(value[i])
            return value[i]
        
def match_suoyouren(pos,value):
    user_name_list = []
    for i in range(len(pos)):
        lac_result = lac.run(value[i])
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "PER":
                user_name_list.append(lac_result[0][index])
    print(user_name_list[0])
    return user_name_list[0]
            
def match_address(pos,value):
    for i in range(len(pos)):
        if '省' and '市' in value[i]:
            #print(value[i])
            return value[i]

def match_shiyongxingzhi(pos,value):
    for i in range(len(pos)):
        if '营运' in value[i]:
            print("营运")
            return "营运"
        else:
            print("非营运")
            return "非营运"

def match_pinpaixinghao(pos,value):
    for i in range(len(pos)):
        if '牌' in value[i] and re.match('[0-9A-Z]',value[i].split('牌')[1]):
            print(value[i])
            return value[i]


def match_cheliangshibiedaihao(pos,value):
    for i in range(len(pos)):
        text=value[i]
        if len(text) == 17:#判断它是否为17位数
            text = text.upper()#小写字母转化为大写字母
            text1 = text.replace("Q","0").replace("O","0").replace("I","1")#替换文本中的字母
            num1 = int(df[text1[0]].to_string()[-1])#第一位
            num2 = int(df[text1[1]].to_string()[-1])#第二位
            num3 = int(df[text1[2]].to_string()[-1])#第三位
            num4 = int(df[text1[3]].to_string()[-1])#第四位
            num5 = int(df[text1[4]].to_string()[-1])#第五位
            num6 = int(df[text1[5]].to_string()[-1])#第六位
            num7 = int(df[text1[6]].to_string()[-1])#第七位
            num8 = int(df[text1[7]].to_string()[-1])#第八位
            num10 = int(df[text1[-8]].to_string()[-1])#第九位
            num11 = int(df[text1[-7]].to_string()[-1])#第十位
            num12 = int(df[text1[-6]].to_string()[-1])#第十一位
            num13 = int(df[text1[-5]].to_string()[-1])#第十二位
            num14 = int(df[text1[-4]].to_string()[-1])#第十三位
            num15 = int(df[text1[-3]].to_string()[-1])#第十四位
            num16 = int(df[text1[-2]].to_string()[-1])#第十五位
            num17 = int(df[text1[-1]].to_string()[-1])#第十六位
            Num1 = num1 * 8 + num2 * 7 + num3 * 6 + num4 * 5 + num5 * 4 + num6 * 3 + num7 * 2 + num8 * 10#前8位的和
            Num2 = num10 * 9 + num11 * 8 + num12 * 7 + num13 * 6 + num14 * 5 + num15 * 4 + num16 * 3 + num17 * 2#后8位的和
            Nums = Num1 + Num2
            if Nums % 11 == int(text1[8]):
                print("VIN正确：",text1)
                return text1
    

def match_fadongjihaoma(pos,value):
    for i in range(len(value)):
        if len(value[i])>=7 and len(value[i])<=8:
            if '.' not in value[i] and re.match('[0-9A-Z]',value[i]):
                print(value[i])
                return value[i]

def match_zhucedate(pos,value):
    for i in range(len(pos)):
        if re.match(r"(\d{4}-\d{1,2}-\d{1,2})",value[i]):
            print(value[i])
            return value[i]
                

def match_zairenshu(pos,value):
    for i in range(len(value)):
        if '人' in value[i]:
            print(value[i])

            return value[i]

def match_weight_sum(pos,value):
    for i in range(len(value)):
        if '总质量' in value[i]:
            if len(value[i])>3:
                print(value[i].split('量')[1])
                return value[i][3:]
                
            else:
                print(value[i+1])
                return value[i+1]
                

def match_weight_zhengbei(pos,value):
    for i in range(len(value)):
        if '整' in value[i]:
            if len(value[i])>4 and value[i][3:4].isdigit():
                return value[i][3:]
            elif value[i-1][:3].isdigit():
                print(value[i-1])
                return value[i-1]
            else:
                print(value[i+1])
                return value[i+1]

def match_weight_heding(pos,value):
    for i in range(len(value)):
        if '核定载质量' in value[i]:
            if len(value[i])>5:
                print(value[i].split('量')[1])
                return value[i][5:]
            elif value[i+1][:2].isdigit():
                print(value[i+1])
                return value[i+1]
            elif value[i-1][:2].isdigit():
                print(value[i-1])
                return value[i-1]
            else:
                return -1

def match_chicun(pos,value):
    for i in range(len(value)):
        if 'mm' in value[i]:
            if len(value[i])>2:
                print(value[i].split('寸')[1])
                return value[i].split('寸')[1]

def match_valid_date(pos,value):
    for i in range(len(value)):
        if '有效期' in value[i]:
            print(value[i].split('至')[1].split('月')[0]+'月')
            return value[i].split('至')[1].split('月')[0]+'月'

if __name__=='__main__':
    dict=OCR('samples/ID_drive/4d086e061d950a7b4961b20207d162d9f3d3c9a4.jpeg')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_haoma(pos,value)
    match_cheliangleixing(pos,value)
    match_suoyouren(pos,value)
    match_address(pos,value)
    match_shiyongxingzhi(pos,value)
    match_pinpaixinghao(pos,value)
    match_cheliangshibiedaihao(pos,value)
    match_fadongjihaoma(pos,value)
    match_zhucedate(pos,value)
    match_zairenshu(pos,value)
    match_weight_sum(pos,value)
    match_weight_heding(pos,value)
    match_weight_zhengbei(pos,value)
    match_chicun(pos,value)
    match_valid_date(pos,value)


