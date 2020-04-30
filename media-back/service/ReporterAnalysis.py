import sys
sys.path.append(r"./dao")
from datetime import datetime
import json
import pandas as pd
from collections import Counter
import datetime

# 根据date获取 当天日期和date天之前日期的列表
def getDateList(date):
    before_n_days = []
    before_n_days.append(str(datetime.date.today()))
    before_n_days.append((str(datetime.date.today() - datetime.timedelta(days=date))))
    return before_n_days

# 获取全部数据的方法
def getDataByDate(date):
    # 获取数据
    df = pd.read_csv("./static/datas/reporter_analysis.csv")
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
    print(news_data_negative)
    data = news_data_negative.loc[:, ['post_id', 'media', 'title', 'link', 'grp_copy', 'str_date']]
    return to_json(data)
# 获取记者正面新闻
def getMediapositiveNewsListByreporter(reporter , date):
    # 获取全部数据
    df = getDataByDate(date)
    # 得到相关媒体的数据
    copy = df.query("reporter == %s" % (reporter))
    # 获取负面新闻呢
    news_data_negative = copy.query("scores == 2")
    data = news_data_negative.loc[:, ['post_id', 'media', 'title', 'link', 'grp_copy', 'str_date']]
    return to_json(data)
# 获取记者关注话题
def getConversationtListByreporter(reporter, date):
    # 获取全部数据
    df = getDataByDate(date)
    copy = df.query("reporter == %s" % (reporter))
    data = copy['category']
    list = data.values.tolist()
    b = str(list)
    b = b.replace('[', '').replace(']', '').replace('\'', '').replace(',', '').replace(' ', '').replace('nan', '')
    d = []
    c = {"H": "经理发表的投研观点", "@": "主动曝光", "Y": "公司运作", "J": "产品绩效", "T": "产品投资", "S": "产品规模", "A": "产品运作", "N": "社保年金专户",
         "B": "公司业绩", "U": "公司总体规模", "V": "公司股东", "F": "评价", "Z": "高管", "D": "高管变动", "G": "ESG", "M": "离职人员",
         "O": "子公司", "E": "入选组合", "P": "经理评价", "R": "经理变动", "\#": "敏感信息", "&": "低权威", "*": "业绩盘点", "$": "推荐",
         "W": "营销活动", "K": "客户"}
    for a in b:
        d.append(c.get(a))
    word_counts = Counter(d)
    dict = word_counts.items()
    l = []
    for key, value in dict:
        d = {}
        d["name"] = key
        d["value"] = value
        l.append(d)
    return l


# 获取记者发文性格
    import time
def getCharacter(reporter):
    # 获取180天的数据
    df = getDataByDate(180)
    # 选取记者数据
    copy = df.query("reporter == %s" % (reporter))
    # 记者日均发文量
    reporter_average_count = len(copy) / 180
    # 记者评分
    num_score = 0
    if reporter_average_count>=1 :
        num_score =100
    else:
        reporter_average_count < 1
        num_score =int(reporter_average_count * 100)
    # 记者影响力分析
    # 获取总转载数
    Total_reprint = copy['grp_copy'].sum()
    # 平均转载数
    average_reprint = Total_reprint / len(copy)
    # 最高转载数
    heigh_reprint = copy['grp_copy'].max()
    # 获取影响力 计算方法：传播效果=0.6*文章总转载数+0.2*最高转载数+0.2*篇均转载数
    effecte = 0.6 * Total_reprint + 0.2 * heigh_reprint + 0.2 * average_reprint
    effecte = int (effecte)
    # 评分逻辑
    effecte_scores = 0
    if effecte >= 100:
        effecte_scores = 100
    else:
        effecte_scores = effecte

    # 正面关注的文章数量
    positive_count = len(copy.query("scores == 2")) + len(copy.query("scores == 1")) + len(copy.query("scores == 3"))
    # 负面面关注的文章数量
    negative_count = len(copy.query("scores == -2")) + len(copy.query("scores == -1")) + len(copy.query("scores == -3"))
    # 中性文章
    positive = positive_count / len(copy)
    negative = negative_count / len(copy)
    positive_scores = 0
    negative_scores = 0
    # 正面评分规则
    if positive >= 0.2:
        positive_scores = 100
    elif 0 < positive < 0.2:
        positive_scores = (positive * 200) + 60
    # 负面评分规则
    if negative >= 0.2:
        negative_scores = 100
    elif 0 < negative < 0.2:
        negative_scores = (negative * 200) + 60

    # 将str_date 转换成 dataframe日期类型
    copy = df.query("reporter == %s" % (reporter))
    copy['str_date'] = copy['str_date'].apply(str)
    copy.loc['str_date'] = copy['str_date'][0:8]
    copy['str_date'] = pd.to_datetime(copy['str_date'], format='%Y%m%d')
    # 统计每天发文量
    count_data = copy['str_date'].value_counts()
    # 1.生成完整时间序列
    dateList = getDateList(180)
    count_index = pd.date_range(start=dateList[1], end=dateList[0])
    # 2.填充数据
    count_data_new = count_data.reindex(count_index, fill_value=0)

    # 如果总数小于50
    stable_score = 0
    if Total_reprint <= 10:
        stable_score = 50
    else:
        # 如果日均发文量大于1
        if reporter_average_count >= 1:
            # 求发文量标准差
            media_count_std = count_data_new.std()
            # 发文量离散系数
            dispersion_coefficient = media_count_std / reporter_average_count
            # 稳定性打分
            if dispersion_coefficient <= 1.3:
                stable_score = 100
            elif 1.3 < dispersion_coefficient <= 1.4:
                stable_score = 90
            elif 1.4 < dispersion_coefficient <= 1.5:
                stable_score = 80
            elif 1.5 < dispersion_coefficient <= 1.6:
                stable_score = 70
            elif 1.6 < dispersion_coefficient <= 1.7:
                stable_score = 60
            elif 1.7 < dispersion_coefficient <= 1.8:
                stable_score = 50
            elif 1.8 < dispersion_coefficient:
                stable_score = 40
        else:
            if count_data_new.max() - count_data_new.min() <= 3:
                stable_score = 100
            elif count_data_new.max() - count_data_new.min() == 4:
                stable_score = 90
            elif count_data_new.max() - count_data_new.min() == 5 or count_data_new.max() - count_data_new.min() == 6:
                stable_score = 80
            elif count_data_new.max() - count_data_new.min() == 7 or count_data_new.max() - count_data_new.min() == 8:
                stable_score = 70
            elif count_data_new.max() - count_data_new.min() == 9 or count_data_new.max() - count_data_new.min() == 10:
                stable_score = 60
            elif count_data_new.max() - count_data_new.min() > 10:
                stable_score = 50
    dict = {
        "num_score":str(num_score),
        "effecte_scores":str(effecte_scores),
        "positive_scores":str(positive_scores),
        "negative_scores":str(negative_scores),
        "stable_score":str(stable_score)
    }
    return dict

# 根据date获取 当天日期和date天之前日期的列表
def getDateList(date):
    before_n_days = []
    before_n_days.append(str(datetime.date.today()))
    before_n_days.append((str(datetime.date.today() - datetime.timedelta(days=date))))
    return before_n_days











def a ():
    # 获取180天的数据
    df = getDataByDate(180)
    # 获取记者列表
    rep = pd.read_csv("./static/datas/reporter_list.csv")
    data = rep.iloc[:,0]
    data = data.values.tolist()
    a = []
    for reporter in data:
        copy = df[df['reporter'].isin([reporter])]
        # print(copy['reporter'])
        p = len(copy.query("scores == 2")) + len(copy.query("scores == 1")) + len(copy.query("scores == 3"))
        n = len(copy.query("scores == -2")) + len(copy.query("scores == -1")) + len(copy.query("scores == -3"))
        z = len(copy.query("scores == 0"))
        b = [reporter,p,n,z,len(copy)]
        a.append(b)
    c = pd.DataFrame(a)
    c.to_csv(path_or_buf="./static/datas/reporter_list.csv", sep=',', index=False, header=True)
    print(c)
    return "qqq"




