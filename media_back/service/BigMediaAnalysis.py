import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project\dao")
import DoMysql
import BigMediaAnalysisDao
import pandas as pd
import numpy as np
import datetime





''' 
    获取列表需要的数据
    参数 int date 
'''
def getBigMediaFormByDate(date):
    # 获取数据
    df = getBigMediaData(date)
    # 获取发文量前十的媒体Series 索引媒体名， 值发文数
    df=df[~df['media'].isin(['同花顺财经'])]
    top_ten=df["media"].value_counts().head(10)
    # 获取发文量列表
    top_ten_counts = top_ten.values.tolist()
    # 获取发文媒体列表
    top_ten_medias = top_ten.index.tolist()
    # 根据媒体获取媒体影响力
    a = 0
    data = []
    for media in top_ten_medias:
        dict = {}
        # 获取单个媒体的全部数据
        meida_data = df.query("media =='%s'" % (media))
        # 获取总转载数
        Total_reprint = meida_data['reprint'].sum()
        # 平均转载数
        average_reprint = Total_reprint / top_ten_counts[a]
        # 最高转载数
        heigh_reprint =meida_data['reprint'].max()
        # 获取影响力 计算方法：传播效果=0.6*文章总转载数+0.2*最高转载数+0.2*篇均转载数
        effecte = 0.6 * Total_reprint + 0.2 * Total_reprint + 0.2 * average_reprint
        effecte = "%.2f" %effecte
        # 将值放入字典
        dict={
            "rank":a+1,
            "top_ten_media" : top_ten_medias[a],
            "top_ten_count" : top_ten_counts[a],
            "effecte" : effecte
        }
        data.append(dict)
        a += 1
    return data


'''
    获取直方图数据
'''
def getBigMediaChartByDate(date):
    # 获取数据
    df = getBigMediaData(date)
    # 获取发文量前十的媒体Series 索引媒体名， 值发文数
    top_ten = df["media"].value_counts().head(10)
    # series转化成字典
    data = list(top_ten.items())
    return data

'''
    获取折线图需要的数据
'''
def getBigMediaBrokenlineChartByDate(date):
    # 获取数据
    df = getBigMediaData(date)
    # 获取发文量前十媒体的列表
    top_ten = df["media"].value_counts().head(10)
    # 获取发文媒体列表
    top_ten_medias = top_ten.index.tolist()
    # 删除不相关的媒体
    df = df[df['media'].isin(top_ten_medias)]
    # 时间缺失值处理
    # 1.生成完整时间序列
    dateList = getDateList(date)
    count_index = pd.date_range(start=dateList[1], end=dateList[0])
    # 循环获取列表中各个媒体每天的发文量
    datas = []
    for top_meida in top_ten_medias :
        # 获取单个媒体的信息
        copy = df.query("media =='%s'" % (top_meida))
        # 将str_date 转换成 dataframe日期类型
        copy['str_date'] = copy['str_date'].apply(str)
        copy.loc['str_date'] = copy['str_date'][0:8]
        copy['str_date'] = pd.to_datetime(copy['str_date'], format='%Y%m%d')
        # 获取每天的发文信息
        media_data = copy["str_date"].value_counts()
        # 2.填充数据
        media_data = media_data.reindex(count_index, fill_value=0)
        # series 转化成字典
        datas.append(top_meida)
        datas.append(list(media_data.items()))
    return datas
'''
    获取媒体大数据页面解释需要的数据
'''
def getDataForBigMediaAnalysis(date):
    # 获取所有媒体的发文量
    pf = getBigMediaData(date)
    pf2 = getBigMediaData(2*date)
    # 监测网站数量
    web_count = pf['media'].nunique()
    print(web_count)
    # 收录文章总数
    article_sum_count = pf['media'].count()
    # 总发文量平均数
    article_sum_count_average = article_sum_count / date
    # article_sum_count_average = '%.2f' % article_sum_count_average
    # 发文量第一的网站
    first_medias = pf['media'].value_counts().head(1)
    first_media = first_medias[first_medias.values == first_medias[0]].index[0]
    # 发文量第一的网站发文量
    first_media_count = first_medias[0]
    # 发文量第一的网站日均发文量
    first_media_verage_count = first_media_count / date
    # 保留两位有效数字
    first_media_verage_count = '%.2f' % first_media_verage_count
    # # 取发文量最多的日期
    first_dates = pf['str_date'].value_counts().head(1)
    first_date = first_dates.index.tolist()[0]
    # 取发文量最多当天的发文量
    first_date_count = first_dates.tolist()[0]
    # 高出均值多少篇
    diff_count = first_date_count - article_sum_count_average
    diff_counts = '%.2f' % diff_count
    # 环比变化量
    web_count2 = pf2['media'].nunique()
    different_count = web_count2 - (2*web_count)
    data = {
        "web_count": str(web_count),
        "article_sum_count": str(article_sum_count),
        "first_media": first_media,
        "first_media_count": str(first_media_count),
        "first_media_average_count": str(first_media_verage_count),
        "first_date": first_date,
        "first_date_count": str(first_date_count),
        "article_sum_count_average": str(article_sum_count_average),
        "diff_count": str(diff_counts),
        "different_count" : str(different_count)
    }
    return data


# 根据date获取 当天日期和date天之前日期的列表
def getDateList(date):
    before_n_days = []
    before_n_days.append(str(datetime.date.today()))
    before_n_days.append((str(datetime.date.today() - datetime.timedelta(days=date))))
    return before_n_days

'''
    从csv中读取数据date天媒体大数据监测页面需要的数据
'''
def getBigMediaData(date):
    # 读取csv数据
    df = pd.read_csv("C:/Users/admin/Desktop/Flask_Project/Flask_Project/static/datas/big_media_analysis.csv")
    # 新增时间类型的列
    df.loc[:,"date_date"] = pd.to_datetime(df['str_date'], format='%Y%m%d')
    # 获取date天前的时间列表
    date_list = getDateList(date)
    count_index = pd.date_range(start=date_list[1], end=date_list[0])
    # 选取时间列表相等的数据
    data = df.loc[df['date_date'].isin(count_index)]
    return data