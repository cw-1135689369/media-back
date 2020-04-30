import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project")
import DoMysql
import ReporterAnalysisDao
from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from collections import Counter
from tkinter import _flatten
import pylab as pl
import jieba
from wordcloud import WordCloud
from PIL import Image
import matplotlib.image as mpimg
import time
import datetime
import chinese_calendar

# 根据date获取 当天日期和date天之前日期的列表
def getDateList(date):
    before_n_days = []
    before_n_days.append(str(datetime.date.today()))
    before_n_days.append((str(datetime.date.today() - datetime.timedelta(days=date))))
    return before_n_days

# 获取全部数据的方法
def getDataByDate(date):
    # 获取数据
    df = pd.read_csv("C:/Users/admin/Desktop/Flask_Project/Flask_Project/static/datas/reporter_analysis.csv")
    # 新增时间类型的列
    df.loc[:, "date_date"] = pd.to_datetime(df['str_date'], format='%Y%m%d')
    # 获取date天前的时间列表
    date_list = getDateList(date)
    count_index = pd.date_range(start=date_list[1], end=date_list[0])
    # 选取时间列表相等的数据
    data = df.loc[df['date_date'].isin(count_index)]
    data = data[~df['reporter'].isin(['-1'])]
    data = data[~df['reporter'].isin([''])]
    return data


# 将dataframe 转化成 json
def to_json(df,orient='split'):
    df_json = df.to_json(orient = "records", force_ascii = False)
    return json.loads(df_json)
# 分页获取首页发文量前五十的记者相关信息
def getData(date):
    # 获取数据
    df = getDataByDate(date)
    # 删除没有记者的数据
    start = time.clock()
    df = df[~df['reporter'].isin([''])]
    df = df[~df['reporter'].isin(['-1'])]
    # 合并媒体，记者  （不同媒体可能存在同名记者）
    df["media_reporter"] = df["media"] + "|" + df["reporter"]
    # 获得发文量前五十的记者，媒体，发文数。
    reporterData = df["media_reporter"].value_counts()
    reporter_data = list(reporterData.items())
    # 列表处理
    data = []
    for reporter in reporter_data:
        a = []
        a = reporter[0].split("|")
        a.append(reporter[1])
        data.append(a)
    return data

# 记者详情页页面数据获取
# 记者关注的基金公司
def getReporterConcernCompany(date,media,reporter):
    # 获取数据
    df = getDataByDate(date)
    # 选取媒体  符合条件的记者
    copy = df.query("media == %s" % (media))
    copy = copy.query("reporter == %s" % (reporter))
    # 对记者关注的基金公司进行分析
    str = ''
    company_data = copy["key1"].values.tolist()
    # 对字符串进行处理,得到列表中所有字符串
    for company in company_data:
        str = str + company
    # 去除字符串的开头的空白
    str = str[1:len(str)]
    # 将字符串切割插入列表
    data = str.split(" ")
    # 统计基金公司出现次数
    result = Counter(data)
    return result

# 获取记者负面关注的基金公司
def getReporterHostilityCompany(date,media,reporter):
    # 获取数据
    df = getDataByDate(date)
    # 选取媒体  符合条件的记者
    copy = df.query("media == %s" % (media))
    copy = copy.query("reporter == %s" % (reporter))
    # 对记者关注的基金公司进行分析
    str = ''
    company_data = copy.query(("scores ==-2"))["key1"].values.tolist()
    if len(company_data) == 0:
        return "无负面新闻"
    # 对字符串进行处理,得到列表中所有字符串
    for company in company_data:
        str = str + company
    # 去除字符串的开头的空白
    str = str[1:len(str)]
    # 将字符串切割插入列表
    data = str.split(" ")
    # 统计基金公司出现次数
    result = Counter(data)
    return result

# 获取记者发表的负面文章
def getMediaNegativeNewsListByreporter(reporter, date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("reporter == %s" % (reporter))
    # 获取负面新闻呢
    news_data_negative = copy.query("scores == -2")
    data = news_data_negative.loc[:, ['post_id', 'media', 'title', 'link', 'grp_copy', 'str_date']]
    return to_json(data)
# 获取记者正面新闻
def getMediapositiveNewsListByreporter(reporter, date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("reporter == %s" % (reporter))
    # 获取负面新闻呢
    news_data_negative = copy.query("scores == 2")
    data = news_data_negative.loc[:, ['post_id', 'media', 'title', 'link', 'grp_copy', 'str_date']]
    return to_json(data)
# 获取记者关注话题
def getConversationtListByreporter(media, date):
    # 获取全部数据
    df = getDataByDate(date)

# 获取记者发文性格
import time
def getCharacter(reporter, media):
    df = getDataByDate(180)
    # 获取所有记者的列表
    rep_list = df["reporter"].values.tolist()
    rep_list = set(rep_list)
    rep_list = list(rep_list)
    del rep_list[0]
    print(rep_list)
    print(len(rep_list))
    # 获取单个记者的全部数据
    i = 0
    rep_list1 = rep_list[0:500]
    rep_list2 = rep_list[500:1000]
    rep_list3 = rep_list[1000:len(rep_list)]
    a = []
    for repo in rep_list :
        Total_reprint = 0
        average_reprint = 0
        heigh_reprint = 0
        effecte = 0
        meida_data = df.query("reporter =='%s'" % (repo))
        # 获取总转载数
        Total_reprint = meida_data['grp_copy'].sum()
        # 平均转载数
        average_reprint = Total_reprint / meida_data['post_id'].size
        # 最高转载数
        heigh_reprint = meida_data['grp_copy'].max()
        # 获取影响力 计算方法：传播效果=0.6*文章总转载数+0.2*最高转载数+0.2*篇均转载数
        effecte = 0.6 * Total_reprint + 0.2 * Total_reprint + 0.2 * average_reprint
        i +=1
        print(i)
        print(repo)
        b = [ repo,str(effecte),str(Total_reprint),str(average_reprint),str(heigh_reprint),]
        a.append(b)
        time.sleep(0.01)
    print(a)
    c = pd.DataFrame(a)
    c.to_csv("C:/Users/admin/Desktop/Flask_Project/Flask_Project/static/datas/reporter.csv")
    return "a"


















#获得饼状图
def get_cakeimg(reporter):
    sql = "SELECT b.scores FROM news2019 a LEFT JOIN news2019_dyn b ON a.`post_id`=b.post_id WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= STR_TO_DATE(str_date,'%%Y%%m%%d') AND a.`reporter`='%s' " % (reporter)
    u = DoMysql.fetch_chall(sql)
    arr1 = np.array(u, dtype=int)

    positiveNum = 0
    negativeNum = 0
    nonePositiveNegative = 0
    for i in arr1:
        if i > 0:
            positiveNum = positiveNum + 1
        elif i < 0:
            negativeNum = negativeNum + 1
        else:
            nonePositiveNegative = nonePositiveNegative + 1
    # 定义饼状图的标签，标签是列表
    plt.cla()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    labels = ['正面新闻', '负面新闻', '中性新闻']
    # 每个标签占多大，会自动去算百分比
    sizes = [positiveNum, negativeNum, nonePositiveNegative, ]
    colors = ['green', 'red', 'lightskyblue']
    # 将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
    explode = (0.1, 0, 0)

    plt.pie(sizes, explode=explode,
            labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True,
            startangle=90)

    plt.axis('equal')
    # figure 保存为二进制文件
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # 将matplotlib图片转换为HTML
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

#获得条形图
def get_histogramimg(reporter):
    sql = "SELECT a.key1 FROM news2019 a WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= STR_TO_DATE(str_date,'%%Y%%m%%d') AND a.`reporter`='%s' " % (reporter)
    v= DoMysql.fetch_chall(sql)
    media = []
    for i in v:
        media.append(i[0][1:].split(" "))
    list(_flatten(media))
    b = str(media)
    b = b.replace('[', '')  # 删除"["
    b = b.replace(']', '')  # 删除"]"
    b = b.replace('\'', '')  # 删除"'"

    media = b.split(",")

    result = Counter(media)
    data = pd.Series(result)
    plt.cla()
    fig, axes = plt.subplots(1, 1)
    data.plot.bar( color='k', alpha=0.7, rot=90, figsize=(15, 8))
    # 参数alpha指定了所绘制图形的透明度，rot指定类别标签偏转的角度

    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # 将matplotlib图片转换为HTML
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

#获取文字云图片
def get_textCloud(reporter):
    sql="SELECT b.category FROM news2019 a LEFT JOIN hisinfo_cx b ON a.`post_id`=b.post_id WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= STR_TO_DATE(b.str_date,'%%Y%%m%%d') AND a.`reporter`='%s'  GROUP BY title" % (reporter)
    v = DoMysql.fetch_chall(sql)
    media = []
    for i in v:
        media.append(i[0][1:].split(" "))
    list(_flatten(media))
    b = str(media)
    b = b.replace('[', '').replace(']', '').replace('\'', '').replace(',','').replace(' ','')
    d=[]
    c={"H":"经理发表的投研观点","@":"主动曝光","Y":"公司运作", "J":"产品绩效", "T":"产品投资" ,"S":"产品规模" ,"A":"产品运作", "N":"社保年金专户","B":"公司业绩" ,"U":"公司总体规模", "V":"公司股东", "F":"评价" ,"Z":"高管", "D":"高管变动" ,"G":"ESG" ,"M":"离职人员", "O":"子公司", "E":"入选组合","P":"经理评价","R":"经理变动","\#":"敏感信息","&":"低权威","*":"业绩盘点","$":"推荐","W":"营销活动","K":"客户"}
    for a in b:
        d.append(c.get(a))
    word_counts = Counter(d)
    # 定义词频背景
    background_image = np.array(Image.open(r"/Flask_Project/timg.jpg"))
    font_path = "E:\project\wordcloud\simfang.ttf"
    plt.cla()
    wd = WordCloud(
        font_path=font_path,  # 设置字体格式，不然会乱码
        background_color="white",  # 设置背景颜色
        mask=background_image  # 设置背景图
    ).generate_from_frequencies(word_counts)

    # 显示词云图
    plt.imshow(wd, interpolation="bilinear")
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return imd

