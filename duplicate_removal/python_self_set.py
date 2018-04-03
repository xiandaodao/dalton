'''
该程序功能为：
	将zip压缩文件逐个解压，用python自带的去重机制进行去重，最后输出至txt文件
'''

#coding = utf-8
import re
import os
import datetime
import zipfile

def geteachFile(filepath):
    filename = []
    for root, dirs, files in os.walk(filepath, topdown=False):
        for file in files:
            if os.path.splitext(file)[1] == '.log' or os.path.splitext(file)[1] == '.zip':
                filename.append(file)
    print(filename)
    return filename

def yesterday():
    nowtime = datetime.date.today()
    oldtime = datetime.timedelta(days=1)
    yesterday = str(nowtime - oldtime).replace('-','_')
    return yesterday

def analysis_file(filepath,filename,date_yesterday) :
    data = set()
    for file in filename:
        filesonpath = filepath + file
        if os.path.splitext(file)[1] == '.log':
            with open(filesonpath) as f:
                    freadline = f.readlines()
                    for line in freadline:
                        temp = line.strip('\n\r')
                        temp = re.split(r'\s', temp)
                        temp = temp[1] + '\t' + temp[2] + '\t' + temp[3] + '\t' + date_yesterday
                        data.add(temp)
        elif os.path.splitext(file)[1] == '.zip':
            z = zipfile.ZipFile(filesonpath)
            z.extractall(filepath)
            filesonpath = filepath + os.path.splitext(file)[0] + '.log'
            with open(filesonpath) as f:
                    freadline = f.readlines()
                    for line in freadline:
                        temp = line.strip('\n\r')
                        temp = re.split(r'\s', temp)
                        temp = temp[1] + '\t' + temp[2] + '\t' + temp[3] + '\t' + date_yesterday
                        data.add(temp)
            os.remove(filesonpath)
    print(data)
    outfile = open('/home/xiandao/Code/redis_control/data/'+date_yesterday+'.txt','w')
    for i in data:
        outfile.write(i+'\n')
    outfile.close()


if __name__ == '__main__':
    date_yesterday = yesterday()
    filepath = '/home/xiandao/Code/redis_control/data/'+date_yesterday+'/'
    #print(filepath)
    filename = geteachFile(filepath)
    if filename:
        analysis_file(filepath,filename,date_yesterday)
