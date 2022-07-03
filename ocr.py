import uvicorn
from typing import Optional
from utils import *

from fastapi import FastAPI,File,UploadFile,Query,applications
from fastapi.openapi.docs import get_swagger_ui_html

def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )

applications.get_swagger_ui_html = swagger_monkey_patch

#创建api
app=FastAPI(
    title='多种单据OCR识别接口',
    description=describe_API
    )


# OCR识别
@app.post("/ocr",summary='OCR识别接口',description="通过算法检测单据的每一个字符，按照需求说明书的要求识别特定单据的特定值，并通过API返回结果。")
async def OCR(File: UploadFile = File(...,description=UploadFile_information),ID: Optional[str]=Query(...,description=ID_information)):
    extension = os.path.splitext(File.filename)[-1]

    if extension in imgType_list or extension==".pdf":

        # 检测到是图片类型的
        if extension in imgType_list:
            temp_file = save_file(File)
            pos,value=await detect_img(temp_file)
            result=detect_paper(ID,pos,value)
            return result

        elif extension==".pdf":
            pdf_img_list,page = save_file(File)
            pos_all,value_all=detect_pdf(img_list=pdf_img_list,page_no=page)
            print(value_all)
            result=detect_paper(ID,pos_all,value_all)
            return result
    else:
        return{"上传信息":"上传的文件既不是PDF也不是图片格式","datetime":current_time}
    

if __name__=='__main__':
    uvicorn.run(app="ocr:app",host='114.215.85.130',port=8023,reload=True,debug=True,workers=2)
