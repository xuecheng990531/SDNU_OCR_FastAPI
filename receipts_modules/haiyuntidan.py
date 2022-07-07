from paddleocr import PaddleOCR
import re

def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr(img_path, cls=False)
    pos = []
    value = []
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos, value


# def match_tidanhao(pos,value):
#     for i in range(len(pos)):
#         if 'MEDUQ' in value[i] and value[i].isalnum():
#             print(value[i])
#             return value[i]

def match_tidanhao(pos,value):
    for i in range(len(pos)):
        if 'BILL' in value[i] and 'OF' in value[i]:
            BILL_pos=pos[i]
            for i in range(len(pos)):
                if BILL_pos[2][0]-10<pos[i][0][0]<BILL_pos[2][0]+300 and BILL_pos[0][1]-40<pos[i][0][1]<BILL_pos[0][1]+40:
                    return value[i]

# def match_dingcanghao(pos,value):
#     for i in range(len(pos)):
#         # [[189.0, 1233.0], [436.0, 1233.0], [436.0, 1272.0], [189.0, 1272.0]]
#         if re.findall(r'[0-9A-Z]', value[i]) and '177' in value[i]: 
#             print(value[i])
#             return value[i]

def match_dingcanghao(pos,value):
    for i in range(len(pos)):
        if 'OOKING' in value[i] or 'REF' in value[i]:
            BOOKING_pos=pos[i]
            #[[197.0, 1179.0], [382.0, 1179.0], [382.0, 1222.0], [197.0, 1222.0]]
            for i in range(len(pos)):
                if BOOKING_pos[0][0]-20<pos[i][0][0]<BOOKING_pos[0][0]+20 and BOOKING_pos[2][1]<pos[i][0][1]<BOOKING_pos[2][1]+400:
                    return value[i]



if __name__ == '__main__':
    dict = OCR('save_files/20220606-01600019.jpg')
    print(dict[1])
    pos = dict[0]
    value = dict[1]
    print(value)
    match_tidanhao(pos,value)
    match_dingcanghao(pos,value)
