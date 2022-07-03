# SDNU_OCR_FastAPI
学校的OCR单据识别项目

一共做了12个特定单据的识别，常用的单据识别包括身份证，行驶证等。根据坐标的形式返回特定要求的字段值，分别使用了 FastAPI，PaddleOCR 和 Uvicorn技术。

## 更新内容
1.本次更新修复了之前上传PDF识别失败的问题。2.对身份证等通用单据做了进一步优化。3.允许上传的pdf多于一页，如果单据的内容太多会导致识别速度可能会很慢

![image](https://github.com/xuecheng990531/SDNU_OCR_FastAPI/blob/main/save_files/%E6%88%AA%E5%B1%8F2022-07-03%2018.51.47.png)
