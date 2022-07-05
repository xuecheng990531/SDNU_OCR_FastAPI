import re
from cv2 import RNG_NORMAL
from paddleocr import PaddleOCR

province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value

def match_fahuodanwei(pos,value):
    for i in range(len(pos)):
        if '有限公司' in value[i]:
            print(value[i])
            return value[i]
    
def match_shouhuodanwei(pos,value):
    for i in range(len(pos)):
        if '客户' in value[i]:
            if '有' in value[i-1]:
                print(value[i-1])
                return value[i-1]
            elif '有' in value[i+1]:
                print(value[i+1])
                return value[i+1]
            elif '限' in value[i+1]:
                print(value[i+1])
                return value[i+1]
            elif '限' in value[i-1]:
                print(value[i-1])
                return value[i+1]
            elif '集团' in value[i+1]:
                print(value[i+1])
                return value[i+1]
            elif '集团' in value[i-1]:
                print(value[i-1])
                return value[i-1]


def match_jinchangzhongliang(pos,value):
    for i in range(len(pos)):
        if 50<pos[i][1][0]-pos[i][0][0]<300 and 7<pos[i][2][1]-pos[i][0][1]<80 and 900<pos[i][0][1]<1100 and 60<pos[i][0][0]<200:
            print(value[i])
            return  value[i]

def match_chuchangzhongliang(pos,value):
    for i in range(len(pos)):
        if 50<pos[i][1][0]-pos[i][0][0]<300 and 7<pos[i][2][1]-pos[i][0][1]<80 and 900<pos[i][0][1]<1100 and 150<pos[i][0][0]<2000:
            print(value[i])
            return  value[i]

def match_jingzhong(pos,value):
    for i in range(len(pos)):
        if 50<pos[i][1][0]-pos[i][0][0]<300 and 7<pos[i][2][1]-pos[i][0][1]<80 and 900<pos[i][0][1]<1100 and 350<pos[i][0][0]<2000:
            print(value[i])
            return  value[i]
    
def match_wuliao(pos,value):
    pat=re.compile(r'[\u4e00-\u9fa5]+')
    for i in range(len(pos)):
        if pat.findall(value[i]) and '.' in value[i]:
            print(value[i])
            return value[i]
        
        

def match_weight_all(pos,value):
    a=[]
    for i in range(len(pos)):
        if '.' in value[i]:
            a.append(value[i])
    
    return a[1],a[2],a[3],a[4]

def match_chehao(pos,value):
    pat=re.compile(r'[\u4e00-\u9fa5]+')

    for i in range(len(pos)):
        if value[i][0] in province:
            print(value[i])
            return value[i]
        elif  len(value[i])==7 and pat.findall(value[i]):
            print(value[i])
            return value[i]

if __name__=='__main__':

    dict=OCR('save_files/微信图片_20220704095447.jpg')
    pos=dict[0]
    value=dict[1]
    print("______________________________________________")
    print(value)
    print("______________________________________________")
    match_fahuodanwei(pos,value)
    match_shouhuodanwei(pos,value)
    match_wuliao(pos,value)
    match_chehao(pos,value)
    match_weight_all(pos,value)