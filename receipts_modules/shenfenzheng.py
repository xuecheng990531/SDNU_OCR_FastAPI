import re
from this import s
from LAC import LAC
from cv2 import add
from idna import valid_contextj
from imageio import RETURN_BYTES
from matplotlib import use
from paddleocr import PaddleOCR
from pydantic import validate_arguments

lac = LAC(mode="lac")
shenfenzheng=r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'
minzu=['汉','蒙古','回','藏','维吾尔','苗','彝','壮','布依','朝鲜','满','侗','瑶','白','土家', '哈尼','哈萨克','傣','黎','傈僳','佤','畲','高山','拉祜','水','东乡','纳西','景颇','柯尔克孜', '土','达斡尔','仫佬','羌','布朗','撒拉','毛南','仡佬','锡伯','阿昌','普米','塔吉克','怒', '乌孜别克', '俄罗斯','鄂温克','德昂','保安','裕固','京','塔塔尔','独龙','鄂伦春','赫哲','门巴','珞巴','基诺']
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

def match_born(pos,value):
    for i in range(len(pos)):
        if '年' in value[i]:
        #    print(value[i][value[i].index('年')-4:])
           return value[i][value[i].index('年')-4:]
            
def match_minzu(pos,value):
    for i in range(len(minzu)):
        for j in range(len(pos)):
            if minzu[i] in value[j]:
                # print(minzu[i])
                return minzu[i]
            
def match_sex(pos,value):
    for i in range(len(pos)):
        if '男' in value[i]:
            # print("男")
            return "男"
        elif '女' in value[i]:
            # print('女')
            return "女" 

def match_address(pos,value):
    for i in range(len(pos)):
        if '省' in value[i] or '县' in value[i] or '市' in value[i] or '区' in value[i] and '局' not in value[i]:
            if '庄' in value[i+1] or '村' in value[i+1] or '室' in value[i+1]:
                return value[i]+value[i+1]
            else:
                return value[i]
        
def match_name(pos,value):
    user_name_list = []
    for i in range(len(pos)):
        lac_result = lac.run(value[i])
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "PER":
                user_name_list.append(lac_result[0][index])

    if len(user_name_list)!=0:
        return user_name_list[0]
    else:
        return -1
        

def match_idnumber(pos,value):
    for i in range(len(pos)):
        if re.match(shenfenzheng,value[i]):
            print(value[i])
            return value[i]

def match_validdate(pos,value):
    for i in range(len(pos)):
        if '有效期限' in value[i]:
            if value[i].split('限')[1] !="":
                return value[i].split('限')[1]
            elif value[i+1][:2].isdigit():
                return value[i+1]

            

def match_qianfa(pos,value):
    for i in range(len(pos)):
        if '公安局' in value[i] or '局' in value[i]:
            return value[i]

if __name__=='__main__':
    dict=OCR('samples/ID_card/3C8C5B451BB4445697730217EC8648E3.jpeg')
    pos=dict[0]
    value=dict[1]
    print(value)
    match_born(pos,value)
    match_address(pos,value)
    match_sex(pos,value)
    match_minzu(pos,value)
    match_name(pos,value)
    match_idnumber(pos,value)
    match_validdate(pos,value)
    match_qianfa(pos,value)