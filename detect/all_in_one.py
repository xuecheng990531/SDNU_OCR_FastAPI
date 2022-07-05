from detect import daoluyunshujingying, jinkou,jianyi,shenfenzheng,weixianhuowu,xingshizheng,jiashizheng,tielu,yingyezhizhao,haiyuntidan,congyezigezheng,daoluyunshu,dingcangxiahuozhi

def match_jinkou(pos,value):
    bianhao=jinkou.match_bianhao(pos, value)
    shouhuoren=jinkou.match_shouhuoren(pos,value)
    shenbaoriqi=jinkou.match_shenbaoriqi(pos, value)
    jinjingguanbie=jinkou.match_jinjingguanbie(pos, value)
    yunshufangshi=jinkou.match_yunshufangshi(pos, value)
    yundanhao=jinkou.match_tiyundanhao(pos, value)
    shenbaodanwei=jinkou.match_shenbaodanwei(pos, value)

    return {
        "编号":bianhao,"收货人":shouhuoren,"申报日期":shenbaoriqi,
        "进境关别":jinjingguanbie,"运输方式":yunshufangshi,
        "运单号":yundanhao,"申报单位":shenbaodanwei
        }

def match_jianyi(pos,value):
    bianhao=jianyi.match_bianhao(pos, value)
    shouhuoren=jianyi.match_shouhuoren(pos,value)
    fahuoren=jianyi.match_fahuoren(pos, value)
    pinming=jianyi.match_pinming(pos, value)
    zhongliang=jianyi.match_zhongliang(pos, value)
    shuchuguojia=jianyi.match_shuchuguojia(pos, value)
    jizhuangxiang=jianyi.match_jizhuangxiang(pos, value)
    shengchanriqi=jianyi.match_shengchanriqi(pos, value)
    shengchanchangjia=jianyi.match_shengchanchangjia(pos, value)
    pinpai=jianyi.match_pinpai(pos, value)
    guige=jianyi.match_guige(pos, value)
    hetonghao=jianyi.match_hetonghao(pos, value)
    yundanhao=jianyi.match_tiyundanhao(pos, value)
    rujingkouan=jianyi.match_rujingkouan(pos, value)
    rujingriqi=jianyi.match_rujingriqi(pos, value)
    biaoji=jianyi.match_biaoji(pos, value)
    baozhuangzhonglei=jianyi.match_baozhuangzhonglei(pos, value)
    beizhu=jianyi.match_beizhu(pos, value)

    return {
        "编号":bianhao,"收货人":shouhuoren,"发货人":fahuoren,
        "品名":pinming,"报检数/重量":zhongliang,"输出国家":shuchuguojia,
        "集装箱号":jizhuangxiang,"生产日期":shengchanriqi,"生产厂家":shengchanchangjia,
        "品牌":pinpai,"规格":guige,"合同号":hetonghao,"运单号":yundanhao,
        "入境口岸":rujingkouan,"入境日期":rujingriqi,
        "标记":biaoji,"包装种类":baozhuangzhonglei,"备注":beizhu
        }

def match_weixian(pos,value):
    fahuoren=weixianhuowu.match_fahuoren(pos, value)
    shouhuoren=weixianhuowu.match_shouhuoren(pos, value)
    chengyunren=weixianhuowu.match_chengyunren(pos, value)
    hangminghangci=weixianhuowu.match_hangminghangci(pos, value)
    hangminghangci_english=weixianhuowu.match_hangminghangci_english(pos, value)
    zhuanghuogang=weixianhuowu.match_zhuanghuogang(pos, value)
    xiehuogang=weixianhuowu.match_xiehuogang(pos, value)
    tidanhao=weixianhuowu.match_tidanhao(pos, value)
    IMO=weixianhuowu.match_IMO(pos, value)
    UN=weixianhuowu.match_UN(pos, value)
    baozhuanglei=weixianhuowu.match_baozhuanglei(pos, value)
    shandian=weixianhuowu.match_shandian(pos, value)
    yingjicuoshi=weixianhuowu.match_yingjicuoshi(pos, value)
    baojianzhonglei=weixianhuowu.match_baojianzhonglei(pos, value)
    kongzhiwendu=weixianhuowu.match_kongzhiwendu(pos, value)
    haiyangwuranwu=weixianhuowu.match_haiyangwuranwu(pos, value)
    zongzhong=weixianhuowu.match_zongzhong(pos, value)
    jingzhong=weixianhuowu.match_jingzhong(pos, value)

    return {
        "发货人":fahuoren,"收货人":shouhuoren,
        "承运人":chengyunren,"航名航次":hangminghangci,"航名航次(English)":hangminghangci_english,
        "装货港":zhuanghuogang,"卸货港":xiehuogang,"提运单号":tidanhao,"IMO":IMO,"UN":UN,
        "包装种类":baozhuanglei,"闪电":shandian,"应急措施":yingjicuoshi,"包件种类":baojianzhonglei,
        "控制温度":kongzhiwendu,"海洋污染物":haiyangwuranwu,"总重":zongzhong,"净重":jingzhong
        }

def match_id_card(pos,value):
    born_date=shenfenzheng.match_born(pos,value)
    minzu=shenfenzheng.match_minzu(pos,value)
    sex=shenfenzheng.match_sex(pos,value)
    address=shenfenzheng.match_address(pos,value)
    name=shenfenzheng.match_name(pos,value)
    id_number=shenfenzheng.match_idnumber(pos,value)
    validate_date=shenfenzheng.match_validdate(pos,value)
    qianfa=shenfenzheng.match_qianfa(pos,value)

    return{
        "姓名":name,"性别":sex,"民族":minzu,
        "出生日期":born_date,"住址":address,"身份证号":id_number,
        "签发机关":qianfa,"证件有效期":validate_date
        }


def match_xingshizheng(pos,value):
    chepaihaoma=xingshizheng.match_haoma(pos,value)
    cheliangleixing=xingshizheng.match_cheliangleixing(pos,value)
    suoyouren=xingshizheng.match_suoyouren(pos,value)
    zhuzhi=xingshizheng.match_address(pos,value)
    shiyongxingzhi=xingshizheng.match_shiyongxingzhi(pos,value)
    pinpaixinghao=xingshizheng.match_pinpaixinghao(pos,value)
    cheliangshibiedaihao=xingshizheng.match_cheliangshibiedaihao(pos,value)
    fadongjihao=xingshizheng.match_fadongjihaoma(pos,value)
    zhuceriqi=xingshizheng.match_zhucedate(pos,value)
    hedingzairenshu=xingshizheng.match_weight_heding(pos,value)
    zongzhiliang=xingshizheng.match_weight_sum(pos,value)
    zhengbeizhiliang=xingshizheng.match_weight_zhengbei(pos,value)
    hedingzaizhiliang=xingshizheng.match_weight_heding(pos,value)
    chicun=xingshizheng.match_chicun(pos,value)
    youxiaoqi=xingshizheng.match_valid_date(pos,value)

    return {
        "车牌号码":chepaihaoma,"车辆类型":cheliangleixing,
        "所有人":suoyouren,"住址":zhuzhi,"使用性质":shiyongxingzhi,
        "品牌型号":pinpaixinghao,"车辆识别代号":cheliangshibiedaihao,
        "发动机号":fadongjihao,"注册日期":zhuceriqi,"核定载人数":hedingzairenshu,
        "总质量":zongzhiliang,"整备质量":zhengbeizhiliang,"核定载质量":hedingzaizhiliang,
        "外廓尺寸":chicun,"有效期":youxiaoqi
        }

def match_jiashizheng(pos,value):
    name=jiashizheng.match_name(pos,value)
    sex=jiashizheng.match_sex(pos,value)
    address=jiashizheng.match_address(pos,value)
    chexing=jiashizheng.match_chexing(pos,value)
    zhenghao=jiashizheng.match_jiashizhenghao(pos,value)
    youxiaoqi=jiashizheng.match_valid_date(pos,value)

    return {
        "姓名":name,"性别":sex,"住址":address,
        "准驾车型":chexing,"证号":zhenghao,"有效期":youxiaoqi
    }

def match_tielu(pos,value):
    xuqiuhao=tielu.match_xuqiuhao(pos,value)
    fazhan=tielu.match_fazhan(pos,value)
    mingcheng=tielu.match_mingcheng(pos,value)
    daozhan=tielu.match_daozhan(pos,value)
    tuoyun_jingbanren=tielu.match_tuoyun_jingbanren(pos,value)
    tuioyun_shoujihaoma=tielu.match_tuoyun_shoujihaoma(pos,value)
    shouhuo_jingbanren=tielu.match_shouhuo_jiangbanren(pos,value)
    shouhuo_dianhuahaoma=tielu.match_shouhuo_dianhuahaoma(pos,value)
    huowumingcheng=tielu.match_huowumingcheng(pos,value)
    jianshu=tielu.match_jianshu(pos,value)
    zhongliang=tielu.match_zhongliang(pos,value)
    xianghao=tielu.match_xianghao(pos,value)
    shifenghao=tielu.match_shifenghao(pos,value)
    quedingzhongliang=tielu.match_quedingzhongliang(pos,value)
    feimu=tielu.match_feimu(pos,value)
    feiyongheji=tielu.match_feiyongheji(pos,value)
    shuie=tielu.match_shuie(pos,value)
    jine=tielu.match_jine(pos,value)

    return {
        "需求号":xuqiuhao,"发站":fazhan,"名称":mingcheng,
        "托运经办人":tuoyun_jingbanren,"托运经办人联系电话":tuioyun_shoujihaoma,
        "到站":daozhan,"到站经办人":shouhuo_jingbanren,"到站经办人联系电话":shouhuo_dianhuahaoma,
        "货物名称":huowumingcheng,"件数":jianshu,"重量":zhongliang,"厢号":xianghao,
        "集装箱施封号":shifenghao,"确定重量":quedingzhongliang,"费目":feimu,"金额":jine,
        "税额":shuie,"费用合计":feiyongheji,"value":value
    }

def match_daoluyunshujingyingzigezheg(pos,value):
    haoma=daoluyunshujingying.match_yunshuzhenghao(pos,value)
    yehu=daoluyunshujingying.match_yehumingcheng(pos,value)
    dizhi=daoluyunshujingying.match_address(pos,value)
    jingjixingzhi=daoluyunshujingying.match_jingjixingzhi(pos,value)
    jingyingfanwei=daoluyunshujingying.match_jingyingfanwei(pos,value)
    youxiaoqi=daoluyunshujingying.match_youxiaoqi(pos,value)

    return {
        '号码':haoma,"业户名称":yehu,"地址":dizhi,"经济性质":jingjixingzhi,
        "经营范围":jingyingfanwei,"有效期":youxiaoqi,"value":value
    }

def match_haiyuntidan(pos,value):
    return {"消息":"我没做"}

def match_yingyezhizhao(pos,value):
    mingcheng=yingyezhizhao.match_mingcheng(pos,value)
    daima=yingyezhizhao.match_daima(pos,value)
    leixing=yingyezhizhao.match_leixing(pos,value)
    daibiaoren=yingyezhizhao.match_daibiaoren(pos,value)
    zhucechengben=yingyezhizhao.match_zhucechengben(pos,value)
    chengliriqi=yingyezhizhao.match_chengliriqi(pos,value)
    yingyeqixian=yingyezhizhao.match_yingyeqixian(pos,value)
    jingyingfanwei=daoluyunshujingying.match_jingyingfanwei(pos,value)

    return {
        "名称":mingcheng,"代码":daima,"类型":leixing,"代表人":daibiaoren,"注册成本":zhucechengben,
        "成立日期":chengliriqi,"营业期限":yingyeqixian,"经营范围":jingyingfanwei,"value":value
    }

def match_congyezigezheng(pos,value):
    
    xingming=congyezigezheng.match_name(pos,value)
    xingbie=congyezigezheng.match_sex(pos,value)
    shenfenzhenghao=congyezigezheng.match_shenfenzhenghao(pos,value)
    danganhao=congyezigezheng.match_danganhao(pos,value)
    congyeleibie=congyezigezheng.match_congyezigeleibie(pos,value)
    youxiaoqi=congyezigezheng.match_validate_date(pos,value)

    return {
        "姓名":xingming,"性别":xingbie,"身份证号":shenfenzhenghao,
        "档案号":danganhao,"从业类别":congyeleibie,"有效期":youxiaoqi,"value":value
    }

def match_daoluyunshu(pos,value):
    
    yunshuzhenghao=daoluyunshu.match_zhenghao(pos,value)
    yehumingcheng=daoluyunshu.match_yehumingcheng(pos,value)
    dizhi=daoluyunshu.match_dizhi(pos,value)
    chepaihaoma=daoluyunshu.match_chepaihaoma(pos,value)
    jingyingxukezhenghao=daoluyunshu.match_jingyingxukezheng(pos,value)
    jingyingleixing=daoluyunshu.match_jingyingleixing(pos,value)
    cheliangleixing=daoluyunshu.match_cheliangleixing(pos,value)
    dunwei=daoluyunshu.match_dunwei(pos,value)
    chicun=daoluyunshu.match_chicun(pos,value)

    return {
        "运输证号":yunshuzhenghao,"业户名称":yehumingcheng,"地址":dizhi,"车牌号码":chepaihaoma,
        "经营许可证号":jingyingxukezhenghao,"经营类型":jingyingleixing,"车辆类型":cheliangleixing,
        "吨位":dunwei,"尺寸":chicun
    }

def match_xiahuozhi(pos,value):
    hangming=dingcangxiahuozhi.match_hangming(pos,value)
    hangci=dingcangxiahuozhi.match_hangci(pos,value)
    tidanhao=dingcangxiahuozhi.match_tidanhao(pos,value)
    xiangxing=dingcangxiahuozhi.match_xiangxing(pos,value)
    zhongliang=dingcangxiahuozhi.match_zhongliang(pos,value)
    chaozhongxiang=dingcangxiahuozhi.match_chaozhongxiang(pos,value)
    mudigang=dingcangxiahuozhi.match_mudigang(pos,value)
    zhongzhuan=dingcangxiahuozhi.match_zhongzhuangang(pos,value)
    huoming=dingcangxiahuozhi.match_huoming(pos,value)
    jianshu=dingcangxiahuozhi.match_jianshu(pos,value)
    chicun=dingcangxiahuozhi.match_chicun(pos,value)
    wendu=dingcangxiahuozhi.match_wendu(pos,value)
    shidu=dingcangxiahuozhi.match_shidu(pos,value)
    weixiandengji=dingcangxiahuozhi.match_weixiandengji(pos,value)
    weixianfudengji=dingcangxiahuozhi.match_weixianfudengji(pos,value)
    weiguihao=dingcangxiahuozhi.match_weiguihao(pos,value)
    xuqiu=dingcangxiahuozhi.match_xuqiu(pos,value)

    return {
        "航名":hangming,"航次":hangci,"提单号":tidanhao,"箱型":xiangxing,"重量":zhongliang,"超重箱":chaozhongxiang,
        "目的港":mudigang,"中转港":zhongzhuan,"货名":huoming,"件数":jianshu,"尺寸":chicun,"温度":wendu,"湿度":shidu,
        "危险等级":weixiandengji,"副危险等级":weixianfudengji,"违规号":weiguihao,"特殊需求":xuqiu
    }
