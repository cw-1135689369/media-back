import sys
sys.path.append(r"./dao")
import SetterDao

def setDateById(date , id ):
    u = SetterDao.setDateById(date,id)
    return u

def getDateById(id ):
    u = SetterDao.getDateById(id)
    return u