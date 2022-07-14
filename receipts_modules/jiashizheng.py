from pydoc import importfile


import multiprocessing
pool=multiprocessing.Pool(processes=4)
from LAC import LAC
lac = LAC(mode="lac")

zhunjia=['A1','A2','A3','B1','B2','C1','C2','C3','C4','D','E','F','M','N','P']

def match_name(pos,value):
    user_name_lis = []
    for i in range(len(pos)):
            _result = lac.run(value[i])
            for _index, _label in enumerate(_result[1]):
                if _label == "PER":
                    user_name_lis.append(_result[0][_index])
    print(user_name_lis[0])
    return user_name_lis[0]

def match_jiashizhenghao(pos,value):
    for i in range(len(pos)):
        if len(value[i])==15 or len(value[i])==18:
            print(value[i])
            return value[i]
        elif '证号' in value[i]:
            if len(value[i])>2:
                print(value[i].split('号')[1])
                return value[i].split('号')[1]
            elif value[i+1].isdigit() and len(value[i+1])>=15:
                print(value[i+1])
                return value[i+1]
            elif value[i-1].isdigit() and len(value[i-1])>=15:
                print(value[i-1])
                return value[i-1]
            
def match_sex(pos,value):
    for i in range(len(pos)):
        if '男' in value[i]:
            return '男'
        else:
            return '女'


def match_address(pos,value):
    for i in range(len(pos)):
        if ("省" in value[i] and "县" in value[i] or "市" in value[i]):
            print(value[i])
            return value[i]

def match_chexing(pos,value):
    for i in range(len(pos)):
        if value[i] in zhunjia:
            print(value[i])
            return value[i]
        elif 'Cl' in value[i]:
            return 'C1'


def match_valid_date(pos,value):
    for i in range(len(pos)):
        if '至' in value[i] and value[i].split('至')[1]!="":
            return value[i].split('至')[1]
