
'''
#PDF2img
def pdf2img(pdfPath, imagePath):
    print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 2 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 2
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_%s.png' % pg)#将图片写入指定的文件夹内

def OCR(img_path):
    table_engine = PPStructure(show_log=False)
    img = cv2.imread(img_path)
    result = table_engine(img)
    for line in result:
        pos=line['res'][0]
        value=line['res'][1]
        return pos,value
'''
def match_fahuoren(pos,value):
    for i in range(len(pos)):
            if '发货人' in value[i]:
                return value[i].split('：')[-1]
                # print('发货人:', value[i][0].split('：')[-1])
                break
def match_shouhuoren(pos,value):
    for i in range(len(pos)):
            if '收货人' in value[i]:
                return value[i].split('：')[-1]
                # print('收货人:', value[i][0].split('：')[-1])
                break
def match_chengyunren(pos,value):
    for i in range(len(pos)):
            if '承运人' in value[i]:
                return value[i].split('：')[-1]
                # print('承运人:', value[i][0].split('：')[-1])
                break
def match_hangminghangci(pos,value):
    for i in range(len(pos)):
            if '船名和航次' in value[i]:
                return value[i].split('：')[-1]
                # print('船名和航次:', value[i][0].split('：')[-1])
                break
def match_hangminghangci_english(pos,value):
    for i in range(len(pos)):
            if 'Voyage' in value[i]:
                #[78.0, 346.0, 215.0, 344.0, 216.0, 367.0, 78.0, 369.0]
                for i in range(len(pos)):
                    if 118<pos[i][1][0]-pos[i][0][0]<218 and 6<pos[i][2][1]-pos[i][0][1]< 76 and 48 < pos[i][0][0]< 108 and 340 < pos[i][3][1] < 400:
                        return value[i][0]
                        # print('船名和航次(English):',value[i][0])
                        break
def match_zhuanghuogang(pos,value):
    for i in range(len(pos)):
            if '装货港' in value[i]:
                return value[i].split('：')[-1]
                # print('装货港:', value[i][0].split('：')[-1])
                break
def match_xiehuogang(pos,value):
    for i in range(len(pos)):
            if '卸货港' in value[i]:
                return value[i].split('：')[-1]
                # print('卸货港:', value[i][0].split('：')[-1])
                break
def match_tidanhao(pos,value):
    for i in range(len(pos)):
        if '提单号' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[78.0, 688.0], [246.0, 689.0], [246.0, 714.0], [78.0, 712.0]],
                if 118<pos[i][1][0]-pos[i][0][0]<218 and 6<pos[i][2][1]-pos[i][0][1]< 76 and 48 < pos[i][0][0]< 108 and 658 < pos[i][0][1] < 718:
                    return value[i]
                    # print('提单号:',value[i][0])
                    break
def match_IMO(pos,value):
    for i in range(len(pos)):
        if 'IMO' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[308.0, 533.0], [376.0, 533.0], [376.0, 558.0], [308.0, 558.0]]
                if 18<pos[i][1][0]-pos[i][0][0]<118 and 6<pos[i][2][1]-pos[i][0][1]< 75 and 278 < pos[i][0][0]< 338 and 503 < pos[i][0][1] < 563:
                    return value[i]
                    # print('IMO:',value[i][0])
                    break
def match_UN(pos,value):
    for i in range(len(pos)):
            if 'UN' in value[i]:
                return value[i].split('：')[-1]
                # print('UN:', value[i][0].split('：')[-1])
                break
def match_baozhuanglei(pos,value):
    for i in range(len(pos)):
            if '包装类' in value[i]:
                return value[i].split('：')[-1]
                # print('包装类:', value[i][0].split('：')[-1])
                break
def match_shandian(pos,value):
    for i in range(len(pos)):
        if '闪点' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[310.0, 660.0], [360.0, 660.0], [360.0, 682.0], [310.0, 682.0]]
                if 10<pos[i][1][0]-pos[i][0][0]<100 and 6<pos[i][2][1]-pos[i][0][1]< 75 and 280 < pos[i][0][0]< 340 and 630 < pos[i][0][1] < 690:
                    return value[i]
                    # print('闪点:',value[i][0])
                    break
def match_yingjicuoshi(pos,value):
    for i in range(len(pos)):
            if '应急措施编号' in value[i]:
                return value[i].split('：')[-1]
                # print('应急措施编号:', value[i][0].split('：')[-1])
                break
def match_baojianzhonglei(pos,value):
    for i in range(len(pos)):
            if 'ages' in value[i]:
                #[301.0, 753.0, 484.0, 749.0, 485.0, 771.0, 301.0, 774.0]
                if 160<pos[i][1][0]-pos[i][0][0]<200 and 6<pos[i][2][1]-pos[i][0][1]< 30 and 280 < pos[i][0][0]< 340 and 630 < pos[i][0][1] < 790:
                    return value[i].split('：')[-1]
                    # print('包件种类:',value[i][0].split('：')[-1])
                    break
def match_kongzhiwendu(pos,value):
    for i in range(len(pos)):
            if 'emergency' in value[i]:
                #[311.0, 812.0, 406.0, 816.0, 405.0, 839.0, 310.0, 835.0]
                if 85<pos[i][1][0]-pos[i][0][0]<100 and 6<pos[i][2][1]-pos[i][0][1]< 35 and 290 < pos[i][0][0]< 340 and 790 < pos[i][0][1] < 830:
                    return value[i].split(':')[-1]
                    # print('控制及应急温度:',value[i][0].split(':')[-1])
                    break
def match_haiyangwuranwu(pos,value):
    for i in range(len(pos)):
        if '海洋污染物' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[313.0, 904.0], [331.0, 909.0], [325.0, 929.0], [307.0, 924.0]]
                if 8<pos[i][1][0]-pos[i][0][0]<68 and 5<pos[i][2][1]-pos[i][0][1]< 75 and 280 < pos[i][0][0]< 340 and 874 < pos[i][0][1] < 934:
                    return value[i]
                    # print('海洋污染物:',value[i][0])
                    break
def match_zongzhong(pos,value):
    for i in range(len(pos)):
        if '总重' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[659.0, 439.0], [721.0, 439.0], [721.0, 463.0], [659.0, 463.0]]
                if 12<pos[i][1][0]-pos[i][0][0]<112 and 5<pos[i][2][1]-pos[i][0][1]< 74 and 629 < pos[i][0][0]< 689 and 409 < pos[i][0][1] < 469:
                    return value[i]
                    # print('总重:',value[i][0])
                    break
def match_jingzhong(pos,value):
    for i in range(len(pos)):
        if '净重' in value[i]:
            for i in range(len(pos)):
                # 结果的坐标[[659.0, 533.0], [718.0, 533.0], [718.0, 558.0], [659.0, 558.0]]
                if 8<pos[i][1][0]-pos[i][0][0]<109 and 5<pos[i][2][1]-pos[i][0][1]< 75 and 629 < pos[i][0][0]< 689 and 503 < pos[i][0][1] < 563:
                    return value[i]
                    # print('净重:',value[i][0])
                    break

