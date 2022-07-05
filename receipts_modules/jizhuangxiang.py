import re
from paddleocr import PaddleOCR


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

def match_xianghao(pos,value):
    number=''
    english=''
    for i in range(len(pos)):
        if 6<=len(value[i])<=7 and value[i].isdigit():
            if len(value[i+1])==2 and value[i+1][0]==1:
                number=value[i]+value[i+1][1]
            else:
                number=value[i]
        if len(value[i])==4 and value[i].isalpha() and 'TARE' not in value[i] and re.sub('[\u4e00-\u9fa5]', '', value[i]):
            english=value[i]
    
    print(english+number)
    return english+number



# def match_zhongliang(pos,value):
#     LBS=[]
#     KGS=[]
#     MAX_Gross=[]
#     TARE=[]
#     for i in range(len(pos)):
#         if 'L' in value[i] and len(value[i])>4 and '.' in value[i]:
#             LBS.append(value[i])
#         elif 'K' in value[i] and len(value[i])>4 and '.' in value[i]:
#             KGS.append(value[i])
    

#     KGS_num1=float(KGS[0].split('K')[0])
#     KGS_num2=float(KGS[1].split('K')[0])
    
#     if KGS_num1>KGS_num2:
#         MAX_Gross.append(str(KGS_num1)+'KGS')
#         TARE.append(str(KGS_num2)+'KGS')
#     else:
#         MAX_Gross.append(str(KGS_num2)+'KGS')
#         TARE.append(str(KGS_num1)+'KGS')

#     LBS_num1=float(LBS[0].split('L')[0])
#     LBS_num2=float(LBS[1].split('L')[0])

#     if LBS_num1>LBS_num2:
#         MAX_Gross.append(str(LBS_num1)+'LBS')
#         TARE.append(str(LBS_num2)+'LBS')
#     else:
#         MAX_Gross.append(str(LBS_num2)+'LBS')
#         TARE.append(str(LBS_num1)+'LBS')
        
#     print(MAX_Gross,TARE)
#     return MAX_Gross,TARE

def match_MAXGROSS(pos,value):
    for i in range(len(pos)):
        if 'MAX' in value[i]:
            return value[i+1],value[i+2]

def match_TARE(pos,value):
    for i in range(len(pos)):
        if 'TARE' in value[i]:
            return value[i+1],value[i+2]

def match_NET(pos,value):
    for i in range(len(pos)):
        if 'NET' in value[i]:
            return value[i+1],value[i+2]


if __name__=='__main__':
    dict=OCR('save_files/R-C (1).jpeg')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_xianghao(pos,value)
    match_MAXGROSS(pos,value)
    match_TARE(pos,value)
    match_NET(pos,value)