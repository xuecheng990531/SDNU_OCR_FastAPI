from idna import valid_contextj
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


def match_tidanhao(pos,value):
    for i in range(len(pos)):
        if 'MEDUQ' in value[i] and value[i].isalnum():
            print(value[i])
            return value[i]

def match_dingcanghao(pos,value):
    for i in range(len(pos)):
        # [[189.0, 1233.0], [436.0, 1233.0], [436.0, 1272.0], [189.0, 1272.0]]
        if re.findall(r'[0-9A-Z]', value[i]) and '177' in value[i]: 
            print(value[i])
            return value[i]



if __name__ == '__main__':
    dict = OCR('save_files/20220606-01600019.jpg')
    print(dict[1])
    pos = dict[0]
    value = dict[1]
    print(value)
    match_tidanhao(pos,value)
    match_dingcanghao(pos,value)
