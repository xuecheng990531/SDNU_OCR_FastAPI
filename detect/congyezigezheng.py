import  re
from idna import valid_contextj
from paddleocr import PaddleOCR
from LAC import LAC
lac=LAC(mode='lac')


id_zhengze=r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'

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


def match_name(pos,value):
    user_name_lis = []
    for i in range(len(pos)):
        _result = lac.run(value[i])
        for _index, _label in enumerate(_result[1]):
            if _label == "PER":
                user_name_lis.append(_result[0][_index])
    print(user_name_lis[0])
    return user_name_lis[0]

def match_sex(pos,value):
    for i in range(len(pos)):
        if '男' in value[i]:
            print('男人')
            return "男"
        elif '女' in value[i]:
            print("女人")
            return "女"   

def match_shenfenzhenghao(pos,value):
    for i in range(len(pos)):
        if re.findall(id_zhengze,value[i]):
            print(value[i])
            return value[i]
        elif '号' in value[i]:
            if value[i].split('号')[1]!="" and value[i].split('号')[1][2:8].isdigit():
                if len(value[i].split('号')[1])>=15 and len(value[i].split('号')[1])<=19:
                    print(value[i].split('号')[1])
                    return value[i].split('号')[1]

def match_danganhao(pos,value):
    for i in range(len(pos)):
        if '档案号' in value[i]:
            if value[i].split('号')[1][1:4].isdigit():
                if '：' in value[i]:
                    print(value[i].split('号')[1][1:])
                    return value[i].split('号')[1][1:]
                else:
                    print(value[i].split('号')[1])
                    return value[i].split('号')[1]
            elif value[i+1][2:4].isdigit():
                print(value[i+1])
                return value[i+1]

def match_congyezigeleibie(pos,value):
    for i in range(len(pos)):
        if '经营性'in value[i] or '道路' in value[i] or '驾驶' in value[i]:
            # print('经营性道路旅客运输驾驶员')
            print(value[i])
            return value[i]


def match_chucilingzhengriqi(pos,value):
    return -1

def match_validate_date(pos,value):
    for i in range(len(pos)):
        if '至' in value[i]:
            print(value[i])
            return value[i]

if __name__=='__main__':
    dict=OCR('samples/congyezige/1.png')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_name(pos,value)
    match_sex(pos,value)
    match_shenfenzhenghao(pos,value)
    match_danganhao(pos,value)
    match_congyezigeleibie(pos,value)
    match_validate_date(pos,value)