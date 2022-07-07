import re
from cv2 import RNG_NORMAL
from paddleocr import PaddleOCR

province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']


# def match_fahuodanwei(pos,value):
#     for i in range(len(pos)):
#         if '有限公司' in value[i]:
#             print(value[i])
#             return value[i]

def match_fahuodanwei(pos,value):
    for i in range(len(pos)):
        if '计量单' in value[i]:
            jl_pos=pos[i]
            for i in range(len(pos)):
                if jl_pos[0][0]-100<pos[i][0][0]<jl_pos[0][0] and jl_pos[0][1]-100<pos[i][0][1]<jl_pos[0][1]+10:
                    return value[i]
     
def match_shouhuodanwei(pos,value):
    for i in range(len(pos)):
        if '客户' in value[i]:
            kh_pos=pos[i]
            for i in range(len(pos)):
                if kh_pos[1][0]<pos[i][0][0]<kh_pos[1][0]+150 and kh_pos[0][1]-50<pos[i][0][1]<kh_pos[0][1]+50:
                    return value[i]


def match_jinchangzhongliang(pos,value):
    for i in range(len(pos)):
        if '进' in value[i] and '重' in value[i]:
            jc_pos=pos[i]
            for i in range(len(pos)):
                if jc_pos[0][0]-50<pos[i][0][0]<jc_pos[0][0]+50 and jc_pos[2][1]<pos[i][0][1]<jc_pos[2][1]+100:
                    return value[i]

def match_chuchangzhongliang(pos,value):
    for i in range(len(pos)):
        if '出' in value[i] and '重' in value[i]:
            cc_pos=pos[i]
            for i in range(len(pos)):
                if cc_pos[0][0]-50<pos[i][0][0]<cc_pos[0][0]+50 and cc_pos[2][1]<pos[i][0][1]<cc_pos[2][1]+100:
                    return value[i]

def match_jingzhong(pos,value):
    for i in range(len(pos)):
        if '净' in value[i] and '重' in value[i]:
            jz_pos=pos[i]
            for i in range(len(pos)):
                if jz_pos[0][0]-50<pos[i][0][0]<jz_pos[0][0]+50 and jz_pos[2][1]<pos[i][0][1]<jz_pos[2][1]+100:
                    return value[i]
     
def match_wuliao(pos,value):
    for i in range(len(pos)):
        if '物料' in value[i]:
            wl_pos=pos[i]
            for i in range(len(pos)):
                if wl_pos[1][0]<pos[i][0][0]<wl_pos[1][0]+150 and wl_pos[0][1]-50<pos[i][0][1]<wl_pos[0][1]+50:
                    return value[i]
        
        

def match_chehao(pos,value):
    pat=re.compile(r'[\u4e00-\u9fa5]+')

    for i in range(len(pos)):
        if value[i][0] in province:
            print(value[i])
            return value[i]
        elif  len(value[i])==7 and pat.findall(value[i]):
            print(value[i])
            return value[i]