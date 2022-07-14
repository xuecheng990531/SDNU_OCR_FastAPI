
def match_hangming(pos, value):
    for i in range(len(pos)):
        if '(Vessel)' in value[i] and len(value[i].split(')'))>6:
            result=value[i].split(')')[1] 
            hangming=result.split('/')[0]
            hangci=result[len(hangming):]
            return hangming,hangci
        elif '(Vessel)' in value[i]:
            vessel_pos=pos[i]
            for i in range(len(pos)):
                if vessel_pos[1][0]<pos[i][0][0]<vessel_pos[1][0]+200 and vessel_pos[0][1]-30<pos[i][0][1]<vessel_pos[0][1]+30:
                    hangming=value[i].split('/')[0]
                    hangci=value[i][len(hangming):]
                    return hangming,hangci

def match_tidanhao(pos,value):
    for i in range(len(pos)):
        # [[225.0, 151.0], [363.0, 151.0], [363.0, 175.0], [225.0, 175.0]]
        if 80 < pos[i][1][0]-pos[i][0][0] < 200 and 10 < pos[i][2][1]-pos[i][0][1] < 40  and 90 < pos[i][0][1] < 200 and 170 < pos[i][0][0] < 300:
            print(value[i])
            return value[i]
        
def match_xiangxing(pos,value):
    for i in range(len(pos)):
        if 'DRY' in value[i]:
            return 'DRY'

def match_zhongliang(pos,value):
    for i in range(len(pos)):
        if 'KGS' in value[i]:
            return value[i]

def match_chaozhongxiang(pos,value):
    return "None"

def match_mudigang(pos,value):
    for i in range(len(pos)):
        if 'Booked by' in value[i] and 'Ref' in value[i]:
            mudi_pos=pos[i]
            for i in range(len(pos)):
                if mudi_pos[1][0]+600<pos[i][0][0]<mudi_pos[1][0]+2500 and mudi_pos[0][1]-15<pos[i][0][1]<mudi_pos[0][1]+20:
                    return value[i]
        elif '交货' in value[i]:
            mudi_pos=pos[i]
            for i in range(len(pos)):
                if mudi_pos[1][0]<pos[i][0][0]<mudi_pos[1][0]+150 and mudi_pos[0][1]-30<pos[i][0][1]<mudi_pos[0][1]+30:
                    return value[i]

def match_zhongzhuangang(pos,value):
    return "None"

def match_huoming(pos,value):
    return "None"

def match_jianshu(pos,value):
    for i in range(len(pos)):
        if 'Piece(s)' in value[i]:
            return value[i]
        elif 'Pack' in value[i] or 'Qty' in value[i]:
            pieces_pos=pos[i]
            for i in range(len(pos)):
                if pieces_pos[0][0]-30<pos[i][0][0]<pieces_pos[0][0]+30 and pieces_pos[0][1]<pos[i][0][1]<pieces_pos[0][1]+100:
                    return value[i]

def match_chicun(pos,value):
    for i in range(len(pos)):
        if 'DRY' in value[i]:
            if value[i].split('Y')[1]!="":
                return value[i].split('Y')[1]
            else:
                return value[i+1]

def match_wendu(pos,value):
    return 'None'

def match_shidu(pos,value):
    return 'None'

def match_weixiandengji(pos,value):
    for i in range(len(pos)):
        if 'IMO Class' in value[i]:
            print(pos[i])

def match_weixianfudengji(Pos,value):
    return 'None'

def match_weiguihao(pos,value):
    return "None"

def match_xuqiu(pos,value):
    return "None"
