import sys
from initdata import db

dbfilename = 'pepole-file'
ENDDB = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'


def storeDbase(db, dbfilename=dbfilename):
    '''将数据库格式化保存为普通文件'''
    dbfile = open(dbfilename, 'w')
    for key in db:
        # 因为数据库是字典的字典，所以需要两层遍历，第一层是对数据库中的人员字典进行遍历
        print(key, file=dbfile)
        # 第二层的遍历是对人员字典中的各个信息进行遍历
        # items方法以列表的形式返回字典中的所有项，键值对之间则是医院组为单位
        for(name, value) in db[key].items():
            print(name + RECSEP + repr(value), file=dbfile)
        print(ENDDB, file=dbfile)
        dbfile.close()


def loadDbase(dbfilename=dbfilename):
    "解析数据，重新构建数据库"
    dbfile = open(dbfilename)
    # stdin是标准输入方法
    sys.stdin = dbfile
    db = {}
    key = input()
    while key != ENDDB:
        rec = {}
        filed = input()
        while filed != ENDREC:
            name, value = filed.split(RECSEP)
            rec[name] = eval(value)
            filed = input()
    db[key] = rec
    key = input()
    return db


if __name__ == '__main__':
    storeDbase(db)
