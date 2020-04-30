import sys
sys.path.append(r"./dao")
import DoMysql

#  根据时间查询媒体分析页需要的数据a.`media`,a.`reporter`,a.`str_date`,a.`title`,a.`link`,b.`scores`
def getMediaAnalysisDataByDate(date):
    sql = "SELECT a.post_id,a.`media`,a.`reporter`,a.`str_date`,a.`title`,a.`link`,b.`scores`,a.`grp_copy`,a.`key1` FROM news2019 a LEFT JOIN news2019_dyn b ON a.post_id = b.post_id Where DATE_SUB(CURDATE(), INTERVAL  %s DAY) <= STR_TO_DATE(a.str_date,'%%Y%%m%%d') and a.platform = 01" %(date)
    u = DoMysql.fetch_chall(sql)
    return u


def getMediaAnalysisDataByDateall():
    sql = "SELECT a.post_id,a.`media`,a.`reporter`,a.`str_date`,a.`title`,a.`link`,b.`scores`,a.`grp_copy`,a.`key1` FROM news2019 a LEFT JOIN news2019_dyn b ON a.post_id = b.post_id Where DATE_SUB(CURDATE(), INTERVAL 180 DAY) <= STR_TO_DATE(a.str_date,'%Y%m%d') and a.platform = 01"
    u = DoMysql.fetch_chall(sql)
    return u
#  根据post_id 查询同组文章
