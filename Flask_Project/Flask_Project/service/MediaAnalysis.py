#encoding:utf-8
import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project\dao")
import DoMysql
import MediaAnalysisDao
import ReporterAnalysisDao
import pandas as pd
import numpy as np
import time
from collections import Counter
import datetime
import chinese_calendar
from chinese_calendar import is_workday
import json



# 获取全部数据的方法
def getDataByDate(date):
    # 获取数据
    df = pd.read_csv("C:/Users/admin/Desktop/Flask_Project/Flask_Project/static/datas/media_analysis.csv")
    # 新增时间类型的列
    df.loc[:, "date_date"] = pd.to_datetime(df['str_date'], format='%Y%m%d')
    # 获取date天前的时间列表
    date_list = getDateList(date)
    count_index = pd.date_range(start=date_list[1], end=date_list[0])
    # 选取时间列表相等的数据
    data = df.loc[df['date_date'].isin(count_index)]
    return data

# 根据date获取 当天日期和date天之前日期的列表
def getDateList(date):
    before_n_days = []
    before_n_days.append(str(datetime.date.today()))
    before_n_days.append((str(datetime.date.today() - datetime.timedelta(days=date))))
    return before_n_days
# 将dataframe 转化成 json
def to_json(df,orient='split'):
    df_json = df.to_json(orient = "records", force_ascii = False)
    return json.loads(df_json)
# 根据时间查看时周几
def getWeekdays(x):
    return x["date"].weekday()

# 根据媒体查询前三的记者
def getReporter(media, date):
    # 获取数据
    df =getDataByDate(date)
    # 得到媒体数据
    copy = df.query("media == %s" % (media))
    # 删除没有记者的数据
    copy=copy[~copy['reporter'].isin([''])]
    copy = copy[~copy['reporter'].isin(['-1'])]
    # 得到记者数据
    reporters = copy['reporter'].value_counts().head(3)
    # 获取有几个记者
    count = reporters.count()
    # 获取发文量列表
    reporter_data = list(reporters.items())
    # 记者名字列表列表
    reporter_name = reporters.index.tolist()
    # 将数据放入字典中
    data = []
    a= 0
    for i in reporters:
        dict = {}
        dict = {
            "reporter_name": reporter_name[a],
            "reporter_count":str(reporters[a]) ,
        }
        data.append(dict)
        a += 1
    return data

# 获取折线图数据
def getNewsDaylyCountForChartBymedia(date,media):
    # 1.生成完整时间序列
    dateList = getDateList(date)
    count_index = pd.date_range(start=dateList[1], end=dateList[0])
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("media == %s" % (media))
    # 将str_date 转换成 dataframe日期类型
    copy['str_date'] = copy['str_date'].apply(str)
    copy.loc['str_date'] = copy['str_date'][0:8]
    copy['str_date'] = pd.to_datetime(copy['str_date'], format='%Y%m%d')
    # 统计每天发文量
    counnt_data = copy["str_date"].value_counts()
    # 填充数据
    counnt_data = counnt_data.reindex(count_index, fill_value=0)
    # 讲series转化成字典
    sum_data = list(counnt_data.items())
    # 每天负面新闻发文量
    negative_counnt_data = copy.query("scores ==-2")["str_date"].value_counts()
    # 填充数据
    negative_counnt_data = negative_counnt_data.reindex(count_index, fill_value=0)
    # 将series转化成字典
    negative_data = list(negative_counnt_data.items())
    return sum_data , negative_data

# 媒体对基金公司的敌意占比
def getHostilityRatio(date,media):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("media == %s" % (media))
    # 得到-2分的数据
    str = ''
    negative_counnt_data = copy.query("scores ==-2")["key1"].values.tolist()
    # 对字符串进行处理,得到列表中所有字符串
    for negative_counnt in negative_counnt_data :
        str =  str + negative_counnt
    # 去除字符串的开头的空白
    str = str[1:len(str)]
    # 将字符串切割插入列表
    data = str.split(" ")
    # 统计基金公司出现次数
    result = Counter(data)
    dict = result.items()
    data  = []
    for key , value in dict:
        d = {}
        d["name"] = key
        d["value"] = value
        data.append(d)
    return  data

# 媒体页解释需要数据
def getDataForMediaAnalysis(media,date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("media == %s" % (media))
    # 获取该媒体总计发文量
    media_articles_sum = copy["str_date"].count()
    # 获取环比增加/减少了多少篇
    # 1.获取两倍date数据
    df = getDataByDate(2 * date)
    # 2.得到相关媒体的数据
    copy_1 = df.query("media == %s" % (media))
    # 3.获取该媒体总计发文量
    media_articles_sum_1 = copy_1["str_date"].count()
    # 4.计算环比增加/减少量
    diff = media_articles_sum_1 - (2 * media_articles_sum)
    diff_str = ''
    if diff > 0 :
        diff_str = "减少"
    elif   diff < 0 :
        diff_str = "增加"
    else:
        diff_str = "相等"
    # 平均发文量
    average_count = media_articles_sum / date
    # 将str_date 转换成 dataframe日期类型
    copy['str_date'] = copy['str_date'].apply(str)
    copy.loc['str_date'] = copy['str_date'][0:8]
    copy['str_date'] = pd.to_datetime(copy['str_date'], format='%Y%m%d')
    # 统计每天发文量
    count_data = copy['str_date'].value_counts()
    # 时间缺失值处理
    # 1.生成完整时间序列
    dateList = getDateList(date)
    count_index = pd.date_range(start=dateList[1] , end=dateList[0])
    # 2.填充数据
    count_data_new = count_data.reindex(count_index,fill_value= 0 )
    # 求发文量标准差
    media_count_std = count_data_new.std()
    # 发文量离散系数
    dispersion_coefficient = media_count_std / average_count
    # 获得工作日发文量 非工作日发文量
    count_data_new = count_data_new.to_frame()
    count_data_new.insert(0, 'date', list(count_data_new.index))
    # 新增列  显示时间周几
    count_data_new.loc[:,"label"] =count_data_new.apply(getWeekdays , axis = 1  )
    # 按工作日，非工作日进行分组
    s =  count_data_new.groupby("label")["str_date"].mean()
    # 统计工作日与非工作日的平均发文量
    # 工作日日均发文量
    Working_day_average = ( s[0] + s[1] + s[2] + s[3] + s[4] )  / 5
    # 非工作日日均发文量
    non_working_days_average =  ( s[5] + s[6] ) / 2
    # 周几发文量最多
    week_count_most = s.max()
    week_most = s.idxmax()
    str_week_most = ''
    if(week_most == 0):
        str_week_most = '周一'
    if (week_most == 1):
        str_week_most = '周二'
    if (week_most == 2):
        str_week_most = '周三'
    if (week_most == 3):
        str_week_most = '周四'
    if (week_most == 4):
        str_week_most = '周五'
    if (week_most == 5):
        str_week_most = '周六'
    if (week_most == 6):
        str_week_most = '周日'
    # 统计发文正负面率
    # 获取负面文章数据
    negative_counnt_data = copy.query("scores ==-2")["key1"].values.tolist()
    # 负面率
    negative_probabily =  len(negative_counnt_data) / media_articles_sum
    data = {
        "date": str(date),
        "media_articles_sum": str(media_articles_sum),
        "diff_str": diff_str,
        "diff_abs": str(abs(diff)),
        "average_count": str(average_count),
        "media_count_std": media_count_std,
        "dispersion_coefficient": str(dispersion_coefficient),
        "Working_day_average": str(Working_day_average),
        "non_working_days_average": str(non_working_days_average),
        "week_count_most": str(week_count_most),
        "str_week_most": str_week_most,
        "negative_probabily": str(negative_probabily)
    }
    return data

# 根据媒体获取获取正面新闻列表
def getMediaPositiveNewsListByMedia(media, date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("media == %s" % (media))
    # 获取媒体正面新闻  包含字标题，link ，转载数
    news_data_positive = copy.query("scores == 2")
    data = news_data_positive.loc[:, ['post_id','media','title', 'link' , 'grp_copy','str_date']]
    return to_json(data)
# 根据媒体获取获取负面新闻列表
def getMediaNegativeNewsList(media, date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("media == %s" % (media))
    # 获取负面新闻呢
    news_data_negative = copy.query("scores == -2")
    data = news_data_negative.loc[:, ['post_id', 'media', 'title', 'link', 'grp_copy', 'str_date']]
    return to_json(data)
# 根据post_id 查分组文章
# todo
def getAllNewsByPostId(post_id):
    # 根据 post_id 查询所有相关文章

    return "1"

