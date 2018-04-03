#coding = utf-8
import redis
import re
import os
import threading
import time


def geteachFile(filepath):
    filepathlog = []
    filedirlog = []

    # root为文件夹路径, dirs为文件夹名字,files为文件名
    for root, dirs, files in os.walk(filepath, topdown=False):
        for file in files:
            if os.path.splitext(file)[1] == '.log':
                filepathlog.append(os.path.join(root, file))
                filedirlog.append(root.split('/')[-1])
                #print(filepathlog)
    #代表完整的路径
    #print(filepathlog)
    #代表上一级文件名，日期
    #print(filedirlog)
    return filepathlog ,filedirlog


def redis_control(freadline,date,filepathlog):
    threadstart = time.ctime()
    print('threadend:%s' % filepathlog, threadstart)

    client = redis.Redis(host='localhost', port=6379, db=0)
    for line in freadline:
        temp = line.strip('\n\r')
        temp = re.split(r'\s',temp)
        temp = temp[1] + ' ' +temp[2]+' ' +temp[3] + ' ' +date
        client.sadd(date,temp)
        print(temp)

    threadend = time.ctime()
    print('threadend:%s'%filepathlog,threadend)

#分析文件
def analysis_file(filepathlog,filedirlog):
    with open('file_table.txt','a+') as file:
        file.seek(0)
        fileline = file.readlines()
        print('fileline:%s'%fileline)
        nloops = range(len(filepathlog))
        for i in nloops:
            if filepathlog[i]+'\n' not in fileline:
                with open(filepathlog[i]) as f:
                    freadline = f.readlines()
                    file.write(filepathlog[i] + '\n')
                    threading.Thread(target=redis_control,args=(freadline,filedirlog[i],filepathlog[i])).start()

if __name__ == '__main__':
    filepath = '/home/xiandao/Code/redis_control/data'
    filepathlog,filedirlog = geteachFile(filepath)
    analysis_file(filepathlog,filedirlog)
