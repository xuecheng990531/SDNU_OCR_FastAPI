
'''                                                                          
   SSSSSSSSSSSSSSS DDDDDDDDDDDDD        NNNNNNNN        NNNNNNNNUUUUUUUU     UUUUUUUU
 SS:::::::::::::::SD::::::::::::DDD     N:::::::N       N::::::NU::::::U     U::::::U
S:::::SSSSSS::::::SD:::::::::::::::DD   N::::::::N      N::::::NU::::::U     U::::::U
S:::::S     SSSSSSSDDD:::::DDDDD:::::D  N:::::::::N     N::::::NUU:::::U     U:::::UU
S:::::S              D:::::D    D:::::D N::::::::::N    N::::::N U:::::U     U:::::U 
S:::::S              D:::::D     D:::::DN:::::::::::N   N::::::N U:::::D     D:::::U 
 S::::SSSS           D:::::D     D:::::DN:::::::N::::N  N::::::N U:::::D     D:::::U 
  SS::::::SSSSS      D:::::D     D:::::DN::::::N N::::N N::::::N U:::::D     D:::::U 
    SSS::::::::SS    D:::::D     D:::::DN::::::N  N::::N:::::::N U:::::D     D:::::U 
       SSSSSS::::S   D:::::D     D:::::DN::::::N   N:::::::::::N U:::::D     D:::::U 
            S:::::S  D:::::D     D:::::DN::::::N    N::::::::::N U:::::D     D:::::U 
            S:::::S  D:::::D    D:::::D N::::::N     N:::::::::N U::::::U   U::::::U 
SSSSSSS     S:::::SDDD:::::DDDDD:::::D  N::::::N      N::::::::N U:::::::UUU:::::::U 
S::::::SSSSSS:::::SD:::::::::::::::DD   N::::::N       N:::::::N  UU:::::::::::::UU  
S:::::::::::::::SS D::::::::::::DDD     N::::::N        N::::::N    UU:::::::::UU    
 SSSSSSSSSSSSSSS   DDDDDDDDDDDDD        NNNNNNNN         NNNNNNN      UUUUUUUUU                                                                                   
'''


import imghdr
import sys, fitz
import os
import time
import uvicorn
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from typing import Optional
from detect.paper_id_2_name import *
from detect.all_in_one import match_congyezigezheng, match_daoluyunshu, match_daoluyunshujingyingzigezheg, match_haiyuntidan, match_id_card,match_jianyi, match_jiashizheng,match_jinkou, match_tielu,match_weixian, match_xingshizheng, match_yingyezhizhao
from fastapi import FastAPI,Request,File,UploadFile,Query,applications
from fastapi.openapi.docs import get_swagger_ui_html

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )

applications.get_swagger_ui_html = swagger_monkey_patch

#创建api
app=FastAPI(title='多种单据OCR识别接口')

#实例化paddleocr
ocr = PaddleOCR(use_angle_cls=False, lang="ch",workers=8)

# OCR识别
@app.post(
    "/ocr",
    summary='OCR识别接口',
    description="1.上传的图片需要摆正，不能存在未经过旋转的图片。2.上传的PDF不应该超过一页，上传的身份证等证件正反面都需要放在一个照片之内。3.上传单据的同时需要确定其ID值.id=1-->危险货物,id=2-->检验检疫,id=3-->进口货物,id=4-->身份证,id=5-->行驶证,id=6--驾驶证,id=7-->铁路货运单,id=8-->海运提单,id=9-->道路运输经营许可证,id=10-->营业执照,id=11-->从业资格证,id=12-->道路运输证",
    tags=['识别接口'],
    )
async def OCR(file: UploadFile = File(...),Paper_ID: Optional[str]=Query()):

    # 返回日期时间
    current_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    # 目前常用的图片格式，方便后面判断是否为图片
    imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'jfif'}

    content = await file.read()
    # with open(f'./save_files/{file.filename}', 'wb') as f:
    #     f.write(content)
    #     f.close()


    #判断是不是pdf
    if '.pdf' in file.filename[-4:]:
        save_path='./save_files/'
        save_img_path=os.path.join(save_path,file.filename[:-4])
        post_path=os.path.join(save_path,file.filename)


        pdfDoc = fitz.open(os.path.join('save_files',file.filename))
        if pdfDoc.pageCount>1:
            return {"错误信息":"PDF的页码大于1","datetime":current_time}
        else:
            for pg in range(pdfDoc.pageCount):
                page = pdfDoc[pg]
                rotate = int(0)

                zoom_x = 2 
                zoom_y = 2
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
                pix = page.getPixmap(matrix=mat, alpha=False)
                
                if not os.path.exists(save_path):#判断存放图片的文件夹是否存在
                    os.makedirs(save_path) # 若图片文件夹不存在就创建
                pix.writePNG(save_img_path+'.png')#将图片写入指定的文件夹内
                os.remove(post_path)
            
            #当上传的文件时pdf格式的时候
            img_path = np.array(Image.open(save_img_path+'.png').convert("RGB"))

    #如果上传的是图片格式
    elif file.filename[-3:] or file.filename[-4:] in imgType_list:
        img_path = np.array(Image.open(file.file).convert("RGB"))
            
        result = ocr.ocr(img_path, cls=False)
        pos=[]
        value=[]
        for i in range(len(result)):
            pos.append(result[i][0])
            value.append(result[i][1][0])

    
    # 如果不是图片也不是pdf，返回1错误
    else:
        return{"上传信息":"上传的文件既不是PDF也不是图片格式","datetime":current_time}


    if Paper_ID=="1":
        result=match_weixian(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="2":
        result=match_jianyi(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="3":
        result=match_jinkou(pos, value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="4":
        result=match_id_card(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="5":
        result=match_xingshizheng(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}    
    elif Paper_ID=="6":
        result=match_jiashizheng(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="7":
        result=match_tielu(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="8":
        result=match_haiyuntidan(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="9":
        result=match_daoluyunshujingyingzigezheg(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="10":
        result=match_yingyezhizhao(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="11":
        result=match_congyezigezheng(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    elif Paper_ID=="12":
        result=match_daoluyunshu(pos,value)
        return {"上传类型":get_paper_name(Paper_ID),"信息":"返回成功","检测日期":current_time,"检测结果":result}
    else:
        return {"上传类型":get_paper_name(Paper_ID),"检测日期":current_time,"检测结果":value}
    

if __name__=='__main__':
    uvicorn.run(app="main:app",host='172.27.127.27',port=8088,reload=True,debug=True,workers=8)
