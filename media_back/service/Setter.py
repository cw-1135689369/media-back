import sys
sys.path.append(r"C:\Users\admin\Desktop\Flask_Project\Flask_Project\dao")
import DoMysql
import SetterDao

def setDateById(date , id ):
    u = SetterDao.setDateById(date,id)
    return u

def getDateById(id ):
    u = SetterDao.getDateById(id)
    return u