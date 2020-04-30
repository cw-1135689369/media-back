import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project\dao")
import DoMysql


# 查询date
def getDateById(id):
    sql = "select a.date from user_test_cw a  WHERE id = 1 " 
    u = DoMysql.fetch_chall_test(sql)
    return u
# 修改date
def setDateById(date,id):
    sql = "UPDATE user_test_cw SET DATE = %s WHERE id = %s" %(date,id)
    u = DoMysql.commit_chall_test(sql)
    return u

