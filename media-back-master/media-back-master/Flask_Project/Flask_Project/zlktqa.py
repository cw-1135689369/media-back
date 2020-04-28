#encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import config
import sys
sys.path.append(r"./service")
import BigMediaAnalysis
import ReporterAnalysis
import MediaAnalysis , Setter

sys.path.append(r"./dao")
import BigMediaAnalysisDao
import MediaAnalysisDao
import ReporterAnalysisDao

import DoMysql
from flask import jsonify
import pandas as pd
import numpy as np
import json
import datetime
from flask_cors import *
from flask_script import  Manager
import csv

app=Flask(__name__)
app.config.from_object(config)
CORS(app ,supports_credentials = True)
app.config['JSON_AS_ASCII'] = False


'''
    日志管理
'''

'''
    设置类接口
'''
# 设置查询时间
@app.route("/setDateById")
def setDateById():
    id = request.args.get("id", type=int)
    date = request.args.get("date", type=int)
    u = Setter.setDateById(date,id)
    return jsonify(u)
# 根据id查询设定的时间
@app.route("/getDateById")
def getDateById():
    id = request.args.get("id", type=int)
    u = Setter.getDateById(id)
    return jsonify(u)

'''
    媒体大数据页面
'''
# 查询列表需要数据
@app.route("/getBigMediaFormByDate")
def getBigMediaFormByDate():
    date = request.args.get("date", type=int)
    u = BigMediaAnalysis.getBigMediaFormByDate(date)
    return jsonify(u)

# 查询媒体发文量前十的数据（直方图数据）
@app.route("/getBigMediaChartByDate")
def getBigMediaChartByDate():
    date=request.args.get("date", type=int)
    u=BigMediaAnalysis.getBigMediaChartByDate(date)
    return jsonify(u)

# 获取折线图数据
@app.route("/getBigMediaBrokenlineChartByDate")
def getBigMediaBrokenlineChartByDate():
    date=request.args.get("date", type=int)
    u=BigMediaAnalysis.getBigMediaBrokenlineChartByDate(date)
    return jsonify(u)

# 媒体大数据页解释数据
@cross_origin()
@app.route("/getBigMediaAnalysis")
def getBigMediaAnalyysis():
    date = request.args.get("date", type=int)
    u = BigMediaAnalysis.getDataForBigMediaAnalysis(date)
    return u

'''
    媒体解释页面
'''
# 根据媒体获取该媒体发文量前三的记者   参数  媒体 时间
@app.route('/getReporterBymediaAndDate')
def getReporterBymedia():
    media= request.args.get("media")
    date=request.args.get("date",type=int)
    u = MediaAnalysis.getReporter(media,date)
    return jsonify(u)

# 获取媒体发文量前十的媒体每天发文数（折线图数据）
@app.route("/getBigMedia")
def getBigMedia():
    date = request.args.get("date", type=int)
    media = request.args.get("media")
    u=MediaAnalysis.getNewsDaylyCountForChartBymedia(date,media)
    return jsonify(u)

# 获取媒体对不同基金公司的敌意占比（饼状图数据）
@app.route("/getHostilityRatio")
def getHostilityRatio():
    date = request.args.get("date", type=int)
    media = request.args.get("media")
    u = MediaAnalysis.getHostilityRatio(date, media)
    return jsonify(u)

# 媒体分析页解释所需要的数据
@app.route('/getMediaDate')
def getediaMDate():
    media= request.args.get("media")
    date=request.args.get("date", type=int)
    u = MediaAnalysis.getDataForMediaAnalysis(media, date)
    return jsonify(u)
# 获取媒体正面负面关注的新闻
@app.route('/getMediaPositiveNewsListByMedia')
def getMediaPositiveNewsListByMedia():
    media= request.args.get("media")
    date=request.args.get("date", type=int)
    u = MediaAnalysis.getMediaPositiveNewsListByMedia(media, date)
    return jsonify(u)
# 获取媒体负面关注的新闻列表
@app.route('/getMediaNegativeNewsListByMedia')
def getMediaNegativeNewsListByMedia():
    media= request.args.get("media")
    date=request.args.get("date", type=int)
    u = MediaAnalysis.getMediaNegativeNewsList(media, date)
    return jsonify(u)
# 根据post_id获取分组文章
@app.route('/getAllNewsByPostId')
def getAllNewsByPostId():
    post_id=request.args.get("post_id", type=int)
    u = MediaAnalysis.getAllNewsByPostId(post_id)
    return jsonify(u)


'''
    记者页面相关接口
'''
# 根据记者发文量统计首页显示数据
@app.route('/getReporterBydate')
def getReporterForDate():
    date=request.args.get("date", type=int)
    u =ReporterAnalysis.getData(date)
    return jsonify(u)
# 根据媒体  记者姓名 获取记者关注的基金公司
@app.route('/getReporterConcernCompany')
def getReporterConcernCompany():
    media = request.args.get("media")
    reporter = request.args.get("reporter")
    date=request.args.get("date", type=int)
    u =ReporterAnalysis.getReporterConcernCompany(date,media,reporter)
    return jsonify(u)
# 根据媒体  记者姓名 获取记者敌意基金公司
@app.route('/getReporterHostilityCompany')
def getReporterHostilityCompany():
    media = request.args.get("media")
    reporter = request.args.get("reporter")
    date=request.args.get("date", type=int)
    u =ReporterAnalysis.getReporterHostilityCompany(date,media,reporter)
    return jsonify(u)
# 根据记者名获取该记者的负面关注新闻
@app.route('/getMediaNegativeNewsListByreporter')
def getMediaNegativeNewsListByreporter():
    reporter= request.args.get("reporter")
    date=request.args.get("date", type=int)
    u = ReporterAnalysis.getMediaNegativeNewsListByreporter(media, date)
    return jsonify(u)
# 获取记者正面关注新闻
@app.route('/getMediapositiveNewsListByreporter')
def getMediapositiveNewsListByreporter():
    reporter= request.args.get("reporter")
    date=request.args.get("date", type=int)
    u = ReporterAnalysis.getMediapositiveNewsListByreporter(reporter, date)
    return jsonify(u)
# 根据媒体记者名获取记者关注话题
@app.route('/getConversationtListByreporter')
def getConversationtListByreporter():
    reporter= request.args.get("reporter")
    date=request.args.get("date", type=int)
    u = ReporterAnalysis.getConversationtListByreporter(reporter, date)
    return jsonify(u)
# todo 雷达图需要数据
'''
    每个刻度最多一百分，对每名记者进行打分设置，五个维度发文量 影响力 正面倾向 负面倾向 发文离散程度 
    测试中
'''
# @app.route('/getCharacter')
# def getCharacter():
#     reporter = request.args.get("reporter")
#     media = request.args.get("media", type=int)
#     u = ReporterAnalysis.getCharacter(reporter, media)
#     return "1"









# todo 雷达图需要数据
@app.route('/a')
def a():
    reporter = request.args.get("reporter")
    media = request.args.get("media", type=int)
    u = ReporterAnalysis.getCharacter(reporter, media)
    return jsonify(u)














# todo 定时任务
from flask_apscheduler import APScheduler

#任务配置类
class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'get_data_job', # 任务id
            'func': '__main__:get_data_job', # 任务执行程序
            'args': None, # 执行程序参数
            'trigger': 'cron',  # cron表示定时任务
            'hour': 17,
            'minute': 18
        }
    ]

# 定义任务执行程序
def get_data_job():
    # 读取数据库数据(媒体大数据页面)
    u=BigMediaAnalysisDao.getBigMediaByDateAll()
    # 将数据转化成dataframe
    df_big_media_analysis = pd.DataFrame(u, columns=['media', 'str_date', 'reprint', 'scores'])
    path = "./static/datas/big_media_analysis.csv"
    df_big_media_analysis.to_csv(path_or_buf = path , sep=',', index=False, header=True)

    # 读取数据库数据(媒体分析页面)
    v = MediaAnalysisDao.getMediaAnalysisDataByDateall()
    # 将数据转化成dataframe
    df_media_analysis = pd.DataFrame(v, columns=['post_id','media', 'reporter','str_date','title','link','scores','grp_copy','key1'])
    path_meida = "./static/datas/media_analysis.csv"
    df_media_analysis.to_csv(path_or_buf=path_meida, sep=',', index=False, header=True)

    # 记者画像页面
    s = ReporterAnalysisDao.getReporterAnalysisDataByDateAll()
    # 将数据转化成dataframe
    df_media_analysis = pd.DataFrame(s, columns=['post_id','media', 'reporter','str_date','title','link','scores','grp_copy','key1'])
    path_meida = "./static/datas/reporter_analysis.csv"
    df_media_analysis.to_csv(path_or_buf=path_meida, sep=',', index=False, header=True)
#为实例化的flask引入定时任务配置
app.config.from_object(SchedulerConfig())





@app.route('/job')
def job():
    get_data_job()
    return '1'


if __name__=='__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表载入实例flask
    scheduler.start()  # 启动任务计划
    app.run()


