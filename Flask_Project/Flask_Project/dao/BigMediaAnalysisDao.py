import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project\dao")
import DoMysql

# 查询一段时间内所有新闻
def getBigMediaByDate(date):
    sql="SELECT a.`media`,a.`str_date`,a.`grp_copy`,b.`scores` FROM news2019 a left join news2019_dyn b on a.post_id =b.post_id WHERE DATE_SUB(CURDATE(), INTERVAL %s DAY) <= STR_TO_DATE(a.str_date,'%%Y%%m%%d') and a.platform = 01 " %(date)
    u = DoMysql.fetch_chall(sql)
    return u
# 查询一段时间内所有新闻
def getBigMediaByDateAll():
    sql="SELECT a.`media`,a.`str_date`,a.`grp_copy`,b.`scores` FROM news2019 a left join news2019_dyn b on a.post_id =b.post_id WHERE DATE_SUB(CURDATE(), INTERVAL 180 DAY) <= STR_TO_DATE(a.str_date,'%Y%m%d') and a.platform = 01 "
    u = DoMysql.fetch_chall(sql)
    return u