#-*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import bs4
from bs4 import BeautifulSoup
import string
a=1
writer=list()
content=list()
info=list()
inputurl=raw_input('请输入你想抓取的某个贴吧得的首页地址：')
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
request_init=urllib2.Request(inputurl,headers=headers)
response_init=urllib2.urlopen(request_init)
soup_init=BeautifulSoup(response_init)
b=soup_init.find('li',class_='l_reply_num').span.find_next('span').get_text().encode('utf-8')
print '共有',b,'页帖子'
title=soup_init.title.get_text().encode('utf-8')+'.doc'
f=open(title,'w')
print '开始抓取……\n'
sum=0
for a in range(1,int(b)):
	print '开始抓取第',a,'页的帖子\n'
	url=inputurl+'?pn='+str(a)
	request=urllib2.Request(url,headers=headers)
	response=urllib2.urlopen(request)
	soup=BeautifulSoup(response)
#抓取帖子作者'''
	for x in soup.find_all('li',class_='d_name'): 
		if x.a.get_text()!='': 
			writer.append(x.a.get_text())
		else:
#VIP超级用户格式有点不一样
			writer.append(x.a.find_next('a').get_text())
	print len(writer)
#抓取帖子内容
	if soup.find('div',class_='d_post_content j_d_post_content '):
		for y in soup.find_all('div',class_='d_post_content j_d_post_content '):
#如果帖子含文字的话  
			if y.get_text(): 
#既含文字又含图片的帖子'''			
				if y.img:   	
					text=y.get_text()+"---内含图片---"
					content.append(text)
#仅含文字的帖子
				else:  	
					content.append(y.get_text())
#仅有图片而无文字的帖子
			else:	
	 			content.append("图片")
	if soup.find('div',class_='d_post_content j_d_post_content  clearfix'):
		for y in soup.find_all('div',class_='d_post_content j_d_post_content  clearfix'):
#如果帖子含文字的话  
			if y.get_text(): 
#既含文字又含图片的帖子'''			
				if y.img:   	
					text=y.get_text()+"---内含图片---"
					content.append(text)
#仅含文字的帖子
				else:  	
					content.append(y.get_text())
#仅有图片而无文字的帖子
			else:	
	 			content.append("图片")
		
	print len(content)
	if soup.find('div',class_="post-tail-wrap"):
		for z in soup.find_all('div',class_="post-tail-wrap"):
#抓取发帖者终端设备信息 
			if z.span.find_next('span').find_next('span').a:
				d={'Terminal':z.span.find_next('span').find_next('span').get_text(),'Louceng':z.span.find_next('span').find_next('span').find_next('span').get_text(),'Time':z.span.find_next('span').find_next('span').find_next('span').find_next('span').get_text()}			
			else:
				d={'Terminal':'来自PC','Louceng':z.span.find_next('span').find_next('span').get_text(),'Time':z.span.find_next('span').find_next('span').find_next('span').get_text()}
			sum=sum+1		
			info.append(d)
			print '累计已抓取',sum,'个帖子\n'
	else:
		for e in range(len(info),len(writer)):
			d={'Terminal':'Unkonwn','Louceng':str(e+1),'Time':'Unknown'}
			info.append(d)
		print '此话题下的帖子与程序设计不一致'	
	print len(info)
#发现每个帖子第二楼总是“百度沸点尖叫榜”，故在此处删除		
del writer[1] 
print soup.title.get_text()
for i in range(len(writer)):
	f.write('\n************************************************\n')
	f.write(writer[i].encode('utf-8'))
	f.write('\n')
	tieziinfo='发帖终端:'+info[i]['Terminal'].decode('utf-8')+'	'+'楼层：'+info[i]['Louceng'].decode('utf-8')+'	'+'发帖时间：'+info[i]['Time'].decode('utf-8')
	f.write(tieziinfo.encode('utf-8'))
	f.write('\n')
	f.write(content[i].encode('utf-8'))
	print '已写入',i,'个帖子到doc文件中\n'
f.close()
print "已抓取完毕"
	
