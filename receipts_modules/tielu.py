import re
from idna import valid_contextj
from paddleocr import PaddleOCR
from LAC import LAC

lac = LAC(mode="lac")
tiaoxingma='^[A-Z0-9]*$'

PATTERN = r'([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|镇|街道)){1}'

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr(img_path, cls=False)
    pos = []
    value = []
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos, value

def match_tiaoxingmabianhao(pos,value):
    for i in range(len(pos)):
        if re.match(tiaoxingma,value[i]):
            print(value[i])
            return value[i]

def match_renming(pos,value):
    user_name_list = []
    for i in range(len(pos)):
        lac = LAC(mode="lac")
        lac_result = lac.run(value[i])
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "PER":
                user_name_list.append(lac_result[0][index])
    return user_name_list

def match_dizhi(pos,value):
    for i in range(len(pos)):
        pattern = re.compile(PATTERN)
        m = pattern.search(value[i])
    return m

def match_xuqiuhao(pos,value):
    for i in range(len(pos)):
        if "需求号" in value[i]:
            if value[i].split('号')[1][3:5].isdigit():
                return value[i].split('号')[1]
            elif value[i+1][3:5].isdigit() and len(value[i+1])>8:
                return value[i+1]
            elif value[i-1][3:5].isdigit() and len(value[i-1])>8:
                return value[i-1]

def match_fazhan(pos,value):
    for i in range(len(pos)):
        # [[659,391],[907,391],[907,464],[659,464]]
        if '发站' in value[i] and '公司' in value[i]:# [[214.0, 391.0], [517.0, 391.0], [517.0, 464.0], [214.0, 464.0]]
            print(pos[i])
            fazhan_pos=pos[i]
            for i in range(len(pos)):
                if fazhan_pos[2][0]+60<pos[i][0][0]<fazhan_pos[2][0]+210 and fazhan_pos[0][1]-20<pos[i][0][1]<fazhan_pos[0][1]+20:
                    return value[i]


def match_mingcheng(pos,value):
    for i in range(len(pos)):
        # [[554.0, 601.0], [1365.0, 601.0], [1365.0, 657.0], [554.0, 657.0]]
        if 700<pos[i][1][0]-pos[i][0][0]<900 and 40<pos[i][2][1]-pos[i][0][1]< 70 and 500 < pos[i][0][0]< 600 and 500 < pos[i][0][1] < 660 and value[i]!="":
            print(value[i])
            return value[i]
        elif value[i]=="名称" and len(value[i])>2:
            print(value[i].split('称')[1])
            return value[i].split('称')[1]
        elif value[i]=="名称":
            print(value[i+1])
            return value[i+1]

def match_daozhan(pos,value):
    for i in range(len(pos)):
        if '到站' in value[i] and '公司' in value[i]:
            daozhan_pos=pos[i]
            for i in range(len(pos)):
                if daozhan_pos[2][0]<pos[i][0][0]<daozhan_pos[2][0]+300 and daozhan_pos[0][1]-40<pos[i][0][1]<daozhan_pos[0][1]+40:
                    return value[i]

    
def match_phone_tuoyun(pos,value):
    for i in range(len(pos)):
        if '车种车号' in value[i]:
            # [[2948.0, 644.0], [3154.0, 644.0], [3154.0, 704.0], [2948.0, 704.0]]
            chehao_pos=pos[i]
            for i in range(len(pos)):
                # [[2537.0, 653.0], [2814.0, 653.0], [2814.0, 700.0], [2537.0, 700.0]]
                if chehao_pos[0][0]-250<pos[i][2][0]<chehao_pos[0][0] and chehao_pos[0][1]-30<pos[i][0][1]<chehao_pos[0][1]+40:
                    return value[i]

def match_phone_shouhuo(pos,value):
    for i in range(len(pos)):
        if '布号' in value[i]:
            bu_pos=pos[i]
            for i in range(len(pos)):
                if bu_pos[0][0]-250<pos[i][2][0]<bu_pos[0][0] and bu_pos[0][1]-30<pos[i][0][1]<bu_pos[0][1]+30:
                    return value[i]


def match_huowumingcheng(pos,value):
    huowu=[]
    for i in range(len(pos)):
        # [[151.0, 1400.0], [311.0, 1400.0], [311.0, 1465.0], [151.0, 1465.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1300 < pos[i][0][1] < 1500:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1500 < pos[i][0][1] < 1800:
            huowu.append(value[i])
        elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1800 < pos[i][0][1] < 2100:
            huowu.append(value[i])
    print(huowu)
    return huowu

# def match_jianshu(pos,value):
#     huowu=[]
#     for i in range(len(pos)):
#         # [[151.0, 1400.0], [311.0, 1400.0], [311.0, 1465.0], [151.0, 1465.0]]
#         if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1300 < pos[i][0][1] < 1500:
#             huowu.append(value[i])
#         elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1500 < pos[i][0][1] < 1800:
#             huowu.append(value[i])
#         elif  100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 100 < pos[i][0][0]< 200 and 1800 < pos[i][0][1] < 2100:
#             huowu.append(value[i])
        
#     print(str(len(huowu))+'件')
#     return str(len(huowu))+'件'

def match_jianshu(pos,value):
    for i in range(len(pos)):
        if '合计' in value[i]:
            heji_pos=pos[i]
            for i in range(len(pos)):
                if heji_pos[2][0]<pos[i][0][0]<heji_pos[2][0]+300 and heji_pos[0][1]-30<pos[i][0][1]<heji_pos[0][1]+30:
                    return value[i]+'件'

def match_zhongliang(pos,value):
    for i in range(len(pos)):
        if '合计' in value[i]:
            heji_pos=pos[i]
            for i in range(len(pos)):
                if heji_pos[2][0]+400<pos[i][0][0]<heji_pos[2][0]+1500 and heji_pos[0][1]-30<pos[i][0][1]<heji_pos[0][1]+30:
                    return value[i]

def match_xianghao(pos,value):
    xianghao=[]
    for i in range(len(pos)):
        if value[i][:3].isalpha() and re.sub('[\u4e00-\u9fa5]', '', value[i][:3]) and len(value[i])==11:
            xianghao.append(value[i])
    return xianghao
                
                    

# def match_xianghao(pos,value):
#     xianghao=[]
#     for i in range(len(pos)):
#         # [[2171.0, 1387.0], [2449.0, 1387.0], [2449.0, 1448.0], [2171.0, 1448.0]]
#         if 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1100 < pos[i][0][1] < 1480:
#             xianghao.append(value[i])
#         elif 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1480 < pos[i][0][1] < 1680:
#             xianghao.append(value[i])
#         elif 200<pos[i][1][0]-pos[i][0][0]<340 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1900 < pos[i][0][0]< 2240 and 1680 < pos[i][0][1] < 1700:
#             xianghao.append(value[i])

#     print(xianghao)
#     return xianghao

def match_shifenghao(pos,value):
    return 0

def match_quedingzhongliang(pos,value):
    for i in range(len(pos)):
        # [[1604.0, 1649.0], [1743.0, 1649.0], [1743.0, 1714.0], [1604.0, 1714.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<300 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1550 < pos[i][0][0]< 1700 and 1550 < pos[i][0][1] < 1700:
            print(value[i]+"KG")
            return value[i]+'KG'

def match_feimu(pos,value):
    feimu=[]
    for i in range(len(pos)):
        # [[1747.0, 1791.0], [1898.0, 1791.0], [1898.0, 1851.0], [1747.0, 1851.0]]
        if 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1680 < pos[i][0][1] < 1840:
            feimu.append(value[i])
            # [[1743.0, 1886.0], [2050.0, 1886.0], [2050.0, 1959.0], [1743.0, 1959.0]]
        elif 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1840 < pos[i][0][1] < 2240:
            feimu.append(value[i])
        elif 100<pos[i][1][0]-pos[i][0][0]<400 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 1680 < pos[i][0][0]< 1880 and 1900  < pos[i][0][1] < 2100:
            feimu.append(value[i])

        # [[2734.0, 1787.0], [3171.0, 1787.0], [3171.0, 1847.0], [2734.0, 1847.0]] 这是第二列费目

        elif 300<pos[i][1][0]-pos[i][0][0]<500 and 40<pos[i][2][1]-pos[i][0][1]< 80 and 2600 < pos[i][0][0]< 2880 and 1680  < pos[i][0][1] < 2000:
            feimu.append(value[i])
    return feimu

                    

def match_feiyongheji(pos,value):
    for i in range(len(pos)):
        if '费用合计' in value[i]:
            feiyong_pos=pos[i]
            for i in range(len(pos)):
                if feiyong_pos[2][0]<pos[i][0][0]<feiyong_pos[2][0]+400 and feiyong_pos[0][1]-30<pos[i][0][1]<feiyong_pos[0][1]+30:
                    return value[i]


def match_shuie(pos,value):
    print('0')
    return 0

def match_jine(pos,value):
    return 0