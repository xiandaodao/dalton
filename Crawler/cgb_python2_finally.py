# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import time
#import traceback 
import os
from multiprocessing import Pool

def main():
	with open('cbg.txt','a+') as cbgtxt:
		#指针回到开头
		cbgtxt.seek(0)
		file = cbgtxt.read()
		#print(file)

		for i in range(830):
			#遍历url
			url1 = "http://recommd.xyq.cbg.163.com/cgi-bin/recommend.py?" \
			  "callback=Request.JSONP.request_map.request_0&_=1517636523775&act=recommd_by_role"
			url2 = "&price_max=120000&kindid=27&price_min=100000&count=100"
			url = url1 +"&server_id=" + str(i) +url2
			
			#伪装成浏览器
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
									 'Chrome/51.0.2704.63 Safari/537.36'}
			
			try:
				req = urllib2.Request(url=url,headers=headers)
				response = urllib2.urlopen(req)
				content = response.read().decode('utf-8')
				target = json.loads(content[36:-1])
				
				#如果equip有数据内容，进行解析
				if target['equips']:
					for temp in range(15):
						try:
							#区
							area_name = target['equips'][temp]['area_name']
							#服务器
							server_name = target['equips'][temp]['server_name']
							# 等级
							equip_level_desc = target['equips'][temp]['equip_level_desc']
							#价格
							price = target['equips'][temp]['price']
							#出售剩余时间
							time_left = target['equips'][temp]['time_left']
							#门派
							school = target['equips'][temp]['school']

							#收藏数
							collect_num = int(target['equips'][temp]['collect_num'])
							#print(type(collect_num))
							
							eid = target['equips'][temp]['eid']
							server_id = target['equips'][temp]['server_id']
							
							buy_url = 'http://xyq.cbg.163.com/equip?s='+str(server_id)+'&'+'eid='+str(eid)
													
							temp = area_name.encode('utf-8') + '\t' + server_name.encode('utf-8') + '\t' + equip_level_desc.encode('utf-8') + '\t' +price.encode('utf-8') + '\t' +time_left.encode('utf-8') + '\t' +str(school) + '\t' +str(buy_url) +'\n'
							#print('----------------------')
							#print area_name + '\t' + server_name + '\t' + equip_level_desc + '\t' +price + '\t' +time_left + '\t' +str(school) + '\t' +str(buy_url) +'\n'
							#print(type(eid))
							#print(type(str(eid)))
							if (server_id<5) and (str(eid) not in file):
								print area_name + '\t' + server_name + '\t' + equip_level_desc + '\t' +price + '\t' +time_left + '\t' +str(school) + '\t' +str(buy_url) +'\n'
								cbgtxt.seek(0, os.SEEK_END)
								cbgtxt.write(temp)
								#print(temp)
						except:
							#traceback.print_exc()
							continue
			except:
				continue


if __name__ =='__main__':
	while True:
		print('--------------------------------------start---------------------------------')
		main()
		print("--------------------------------------ok,good------------------------------")
		
		
