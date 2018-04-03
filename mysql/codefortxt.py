#coding=utf-8
import MySQLdb
import ConfigParser

class codefortxt(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("test.conf")

        #secs = cf.sections()
        #kvs = cf.items('db')

        self.db_host = cf.get("db","db_host")
        self.db_port = int(cf.get("db","db_port"))
        self.db_user = cf.get("db", "db_user")
        self.db_pass = cf.get("db", "db_pass")
        self.db_name = cf.get("db", "db_name")
        #self.db_table = cf.get("db", "db_table")
        self.db_columnstr = cf.get("db","db_columnstr")

        self.conn = MySQLdb.connect(user=self.db_user,
                               passwd=self.db_pass,
                               host=self.db_host,
                               db=self.db_name,
                               port=self.db_port)

        self.cur = self.conn.cursor()

    def everytable(self,table):
        # 检查列名
        sql = "desc " + table + ';'
        self.cur.execute(sql)
        columns = self.cur.fetchall()
        column_in_table = []
        for column in columns:
            column_in_table.append(column[0])
        # 日志中输出这个表含有所有的列名
        print('all column\'s name:')
        print(column_in_table)

        # 防止有些列数据库中没有，只选择数据库中有的列进行输出
        temp = self.db_columnstr.split(',')
        columnfinal = ''
        for i in column_in_table:
            if i.lower() in temp:
                columnfinal = columnfinal + str(i) + ','
        columnfinal = columnfinal[:-1]
        #print(columnfinal)


        # 输出有多少行
        sql = 'select count(*) from ' + table + ";"
        self.cur.execute(sql)
        count = self.cur.fetchone()[0]
        print('table %s have count: %s' % (table, count))

        if count!= 0 :
            # 开始写数据到txt文件中
            sql = "select " + columnfinal + " from " + table + ";"
            print(sql)
            self.cur.execute(sql)
            rows = self.cur.fetchall()
            outfile = table + ".txt"
            f = open('./sgk_2/'+outfile, 'w')
            for row in rows:
                temp = '\t'.join(row)
                f.write(str(temp) + '\n')
            f.close()
            print("all data has been saved. table's name: %s\n" % str(table))
        else:
            print("count is zero\n")

    def database(self):
        sql = "show tables;"
        self.cur.execute(sql)
        tables = self.cur.fetchall()
        for table in tables:
            #print(table[0])
            self.everytable(table[0])
        self.conn.close()

if __name__ =='__main__':
    print('-------program-start--------')
    txt = codefortxt()
    txt.database()
    print('----------end----------')
