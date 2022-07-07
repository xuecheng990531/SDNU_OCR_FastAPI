import re
from tempfile import TemporaryDirectory
import turtle
from fastapi import FastAPI
from paddleocr import PaddleOCR
from PIL import Image
from component_modules.paper_id_2_name import *
from component_modules.all_in_one import *
import cv2
import os
import shutil
import numpy as np
import time
import fitz


#实例化paddleocr
ocr = PaddleOCR(use_angle_cls=True, lang="ch",workers=8)
# 当前日期时间
current_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


#-------------------------------------------------detect_pic-----------------------------------
def detect_img(img_path):
    result =ocr.ocr(img_path, cls=True)
    pos=[]
    value=[]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    return pos,value
#-------------------------------------------------detect_pic-----------------------------------


#-------------------------------------------------detect_pdf-----------------------------------
def detect_pdf(img_list,page_no):
    print('ahsgdjagsjkdgilquwyeqowieuio',img_list)
    value_all=[]
    pos_all=[]
    for index in range(page_no):
        pos,value=detect_img(img_list[index])
        value_all.extend(value)
        pos_all.extend(pos)
    return pos_all,value_all
#-------------------------------------------------detect_pdf-----------------------------------



#-------------------------------------------------information-----------------------------------
describe_API='更新时间：2022年7月7日  \n   \n 更新内容：提高检测精度'
UploadFile_information='该处上传PDF或者图片,格式为:  \n   \n jpg、bmp、png、jpeg、jfif  \n   \n 为了尽可能提高检测的准确率，应确保：  \n   \n 1.上传的图片需要摆正，不能存在未经过旋转的图片。  \n   \n 2.上传的PDF尽量不要超过一页，上传的身份证等证件正反面都需要放在一个照片之内。  \n   \n 3.上传单据的同时需要确定其ID值'
ID_information='每个ID都唯一代表对应的单据，每个ID对应的单据如下：  \n   \n ID=1---------------------------->危险货物安全适运说明书  \n   \n ID=2---------------------------->入境货物检验检疫证明  \n   \n ID=3---------------------------->进口报关单  \n   \n ID=4---------------------------->身份证  \n   \n ID=5---------------------------->行驶证  \n   \n ID=6---------------------------->驾驶证  \n   \n ID=7---------------------------->铁路货运单  \n   \n ID=8---------------------------->地中海提单  \n   \n ID=9---------------------------->道路运输经营许可证  \n   \n ID=10--------------------------->营业执照  \n   \n ID=11--------------------------->从业资格证  \n   \n ID=12--------------------------->道路运输证  \n   \n ID=13--------------------------->订舱下货纸（MKL)  \n   \n ID=14--------------------------->过磅单（特定公司）  \n   \n ID=15--------------------------->集装箱信息'
#-------------------------------------------------information-----------------------------------



#-------------------------------------------------PDF Compose-----------------------------------
def PDF_Concate(imgs, direction="vertical", gap=0):
    imgs=[cv2.imread(img) for img in imgs]
    imgs = [Image.fromarray(img) for img in imgs]
    w, h = imgs[0].size
    if direction == "horizontal":
        result = Image.new(imgs[0].mode, ((w+gap)*len(imgs)-gap, h))
        for i, img in enumerate(imgs):
            result.paste(img, box=((w+gap)*i, 0))
    elif direction == "vertical":
        result = Image.new(imgs[0].mode, (w, (h+gap)*len(imgs)-gap))
        for i, img in enumerate(imgs):
            result.paste(img, box=(0, (h+gap)*i))
    else:
        raise ValueError("The direction parameter has only two options: horizontal and vertical")
    return np.array(result)
#-------------------------------------------------PDF Compose-------------------------------------

#-------------------------------------------------PDF Compose-------------------------------------
def pyMuPDF_fitz(pdfPath, imagePath,img_name):    
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
        
        pix.writePNG(imagePath+'/'+img_name+'_%s.png' %pg)#将图片写入指定的文件夹内
    return pdfDoc.pageCount
#-------------------------------------------------PDF Compose-------------------------------------

#-------------------------------------------------save-------------------------------------
imgType_list = {'.jpg', '.bmp', '.png', '.jpeg', '.jfif'}

def save_file(uploaded_file, path="save_files"):
    # 分离拓展名和名字
    extension = os.path.splitext(uploaded_file.filename)[-1]
    name=os.path.splitext(uploaded_file.filename)[0]
    temp_file = os.path.join(path,name+extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    if extension in imgType_list:
        return temp_file
    elif extension=='.pdf':
        pdf_page_list=[]
        # 转换为图片格式
        page=pyMuPDF_fitz(str(os.path.join(path,name+extension)),path,name)

        # 返回一个列表
        for index in range(page):
            temp_file = os.path.join(path,name+'_'+str(index)+'.png')
            pdf_page_list.append(temp_file)
        return pdf_page_list,page
#-------------------------------------------------save-------------------------------------



#-------------------------------------------------which paper-------------------------------------
def detect_paper(ID,pos,value):
    if ID=="1":
        result=match_weixian(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="2":
        result=match_jianyi(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="3":
        result=match_jinkou(pos, value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="4":
        result=match_id_card(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="5":
        result=match_xingshizheng(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}    
    elif ID=="6":
        result=match_jiashizheng(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="7":
        result=match_tielu(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="8":
        result=match_haiyun(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="9":
        result=match_daoluyunshujingyingzigezheg(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="10":
        result=match_yingyezhizhao(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="11":
        result=match_congyezigezheng(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="12":
        result=match_daoluyunshu(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="13":
        result=match_xiahuozhi(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="14":
        result=match_guobangdan(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    elif ID=="15":
        result=match_jizhuangxiang(pos,value)
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":result,"所有检测结果":''.join(value)}
    else:
        return {"上传类型":get_paper_name(ID),"信息":"返回成功","检测日期":current_time,"检测结果":''.join(value)} 
#-------------------------------------------------which paper-------------------------------------