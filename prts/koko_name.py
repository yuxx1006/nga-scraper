# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os

from selenium.webdriver import Chrome, Firefox, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import pdb

from datetime import datetime
from time import sleep
from lxml import etree
import pandas as pd
import re
# from html.parser import HTMLParser
import html

# url = "https://bbs.nga.cn/read.php?tid=24043503"

browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()

# HEADERS = ['stage', 'image_urls', 'extra_image_urls', 'map_url']
HEADERS = ['name','url']
my_table = pd.DataFrame(columns=HEADERS)
BASE_URL = 'https://kokodayo.fun/'
# WEB_BASE_URL = 'http://prts.wiki/w/'



# stage_table = pd.read_csv('wiki_names.csv', names= ['stage'])

# stages = ['1-11_遗忘', 'S2-1_迟缓-1', 'S2-2_迟缓-2', 'S2-3_封锁-1', 'S2-4_封锁-2', 'S2-5_术师-1', 'S2-6_术师-2', 'S2-7_术师-3', 'S2-8_陷阱-1', 'S2-9_陷阱-2', 'S2-10_窒息-1', 'S2-11_窒息-2', 'S2-12_窒息-3', 'S3-1_潜伏-1', 'S3-2_潜伏-2', 'S3-3_侦察-1', 'S3-4_侦察-2', 'S3-5_侦察-3', 'S3-6_集火-1', 'S3-7_隐匿-1', 'S4-1_晶簇-1', 'S4-2_晶簇-2', 'S4-3_晶簇-3', 'S4-4_多足-1', 'S4-5_多足-2', 'S4-6_多足-3', 'S4-7_狂怒-1', 'S4-8_狂怒-2', 'S4-9_狂怒-3', 'S4-10_坚守-1', 'S5-1_盘踞-1', 'S5-2_盘踞-2', 'S5-3_恶寒-1', 'S5-4_恶寒-2', 'S5-5_恐慌-1', 'S5-6_恐慌-2', 'S5-7_盘旋-1', 'S5-8_盘旋-2', 'S5-9_异状-1', 'H5-1_炼狱行动-1', 'H5-2_炼狱行动-2', 'H5-3_炼狱行动-3', 'H5-4_炼狱行动-4', 'S6-1_凝结-1', 'S6-2_凝结-2', '6-12_冰原之雪', 'S6-3_霜冻-1', 'S6-4_霜冻-2', 'H6-1_冰狱行动-1', 'H6-2_冰狱行动-2', 'H6-3_冰狱行动-3', 'H6-4_冰狱行动-4', 'S7-1_埋伏-1', 'S7-2_埋伏-2', 'H7-1_星火行动-1', 'H7-2_星火行动-2', 'H7-3_星火行动-3', 'H7-4_星火行动-4', 'M8-6_再见，只为再见', 'H8-1_狂夜行动-1', 'H8-2_狂夜行动-2', 'H8-3_狂夜行动-3', 'H8-4_狂夜行动-4', 'LS-1_遭遇战演习', 'LS-2_游击战演习', 'LS-3_阵地战演习', 'LS-4_特种战演习', 'LS-5_歼灭战演习', 'AP-1_源石开采保全', 'AP-2_源石运输保全', 'AP-3_精炼器材保全', 'AP-4_矿材仓库保全', 'AP-5_精炼工厂保全', 'CE-1_私人家具押运', 'CE-2_工业设备押运', 'CE-3_珍贵原料押运', 'CE-4_国际重犯押运', 'CE-5_机密情报押运', 'CA-1_疗养用地净空', 'CA-2_勘探基点净空', 'CA-3_巡逻路线净空', 'CA-4_任务区域净空', 'CA-5_战略要道净空', 'SK-1_废墟清剿', 'SK-2_窝点清剿', 'SK-3_哨所清剿', 'SK-4_据地清剿', 'SK-5_要塞清剿', 'PR-A-1_防守', 'PR-A-2_据守', 'PR-B-1_干涉', 'PR-B-2_打击', 'PR-C-1_急行', 'PR-C-2_冲锋', 'PR-D-1_突破', 'PR-D-2_猛攻', '乌萨斯_切尔诺伯格', '炎国_龙门外环', '炎国_龙门市区', '卡西米尔_大骑士领郊外', 'MB-1_密会', 'MB-2_另一个视角', 'MB-4_勇敢，莽撞', 'MB-5_危险交易', 'MB-6_制定计划', 'MB-7_背叛', 'MB-8_激战之末'];
# stages = ['龙门_中转站', '切尔诺伯格_6区废墟', '切尔诺伯格_破碎大道', '切尔诺伯格_荒废工厂', '哥伦比亚_闭锁监狱', '荒野_风蚀高地','荒野_黄铁峡谷','龙门_军械库东', '荒野_无序矿区']
# stages.end()
# for stage in stages:


# for i, row in stage_table.iterrows():
try:
	# if i == 0: continue
	# stage = row['stage']
	# print(stage)
	browser.get(BASE_URL)
	sleep(5)
	parser = etree.HTML(browser.page_source)
	names = []
	if parser.xpath('//div[@class="swiper-wrapper"]//span[@class="profile-container"]'):
		try: 
			name_list = parser.xpath('//div[@class="swiper-wrapper"]//span[@class="profile-container"]//div[@class="profile-item"]//div[@class="image-inner"]')


			# for item in name_list:
			# 	item_json = json.loads(item)
			# 	print(item_json)
			
			for name in name_list:
				each_str = etree.tostring(name, pretty_print=True).decode('utf-8')
				print(each_str)
				start = each_str.find('alt')
				end = each_str.find('/>')
				img_name =html.unescape( each_str[start+5:end - 1])
				print(img_name)
				# name = re.search(r'alt',each_str).group(1)
				# name = name.group(0)
				# print(name)
				# pattern = re.compile(r'''(?:[^>"']|"[^"]*"|'[^']*')+?\sclass\s*=\s*("[^"]*"|'[^']*')''')
				# mylist = []
				# for outermatch in re.finditer(r'''<(?:[^>"']|"[^"]*"|'[^']*')+>''', each_str):
				#     mylist.extend(pattern.findall(outermatch.group(0)))
				# print(mylist)
				# tags =  re.findall(pattern,each_str,re.S|re.M)  

				match = re.search(r'\(([^\)]+)\)', each_str)
				match = match.group(0).replace('(','').replace(')','')
				match = match.replace('?x-oss-process=style/webp', '').replace('.png','_1.png').replace('portrait','halfPic')
				match = match.replace('&quot;','')
				print(match)

				
				data = {
					"name": img_name,
					"url": match
				}
			
				my_table = my_table.append(data, ignore_index=True)
		except Exception as e:
			print(e)
	else:
		print(names)
		pass
	# print(parser.xpath('//table[@class="wikitable"]'))
	# try:
	# 	# number of enemies
	# 	# enemy_box = table_normal.xpath('.//td[@colspan="4"]')[6]
	# 	# enemy = enemy_box.xpath('./text()')[0]
	# 	# for i, each in enumerate(enemy):
	# 	# 	print(each.xpath('./text()')[0])
	# 	# imgs

	# 	if table_normal.xpath('.//td[@colspan="2"]//div[@class="nomobile"]//img'):
	# 		imgs = table_normal.xpath('.//td[@colspan="2"]//div[@class="nomobile"]//img')
	# 	# elif table_normal.xpath('.//td[@colspan="5"]//div[@class="nomobile"]//img'):
	# 	# 	imgs = table_normal.xpath('.//td[@colspan="5"]//div[@class="nomobile"]//img')
	# 	# elif table_normal.xpath('.//td[@colspan="3"]//div[@class="nomobile"]//img'):
	# 	# 	imgs = table_normal.xpath('.//td[@colspan="3"]//div[@class="nomobile"]//img')
	# 		print(imgs)
	# 	if imgs:
	# 		images = []
	# 		for img in imgs:
	# 			img_dic = {}
	# 			if img.xpath('./@src'):
	# 				img_name = img.xpath('./@alt')[0]
	# 				arr = img.xpath('./@src')[0].split('/')
	# 				img_url = os.path.join(IMG_BASE_URL, arr[3], arr[4], arr[5])
	# 				img_dic[img_name] = img_url

	# 			images.append(dict(img_dic))
	# 	print(images)

	# 	# small imgs
	# 	extra_imgs = table_normal.xpath('.//td[@colspan="5"]//div[@class="nomobile"]//img')
	# 	if extra_imgs:
	# 		extra_images = []
	# 		for each in extra_imgs:
	# 			extra_img_dic = {}
	# 			if each.xpath('./@src'):
	# 				extra_img_name = each.xpath('./@alt')[0]
	# 				extra_arr = each.xpath('./@src')[0].split('/')
	# 				extra_img_url = os.path.join(IMG_BASE_URL, extra_arr[3], extra_arr[4], extra_arr[5])
	# 				extra_img_dic[extra_img_name] = extra_img_url

	# 			extra_images.append(dict(extra_img_dic))

	# 	# map
	# 	if table_normal.xpath('.//td[@colspan="6"]//a[@class="image"]//img'):
	# 		map_img = table_normal.xpath('.//td[@colspan="6"]//a[@class="image"]//img')[0]
	# 	elif table_normal.xpath('.//td[@colspan="10"]//a[@class="image"]//img'):
	# 		map_img = table_normal.xpath('.//td[@colspan="10"]//a[@class="image"]//img')[0]
	# 	if map_img.xpath('./@src'):
	# 		my_list = []
	# 		map_dic = {}
	# 		map_name = map_img.xpath('./@alt')[0]
	# 		map_arr = map_img.xpath('./@src')[0].split('/')
	# 		map_url = os.path.join(IMG_BASE_URL, map_arr[3], map_arr[4], map_arr[5])
	# 		map_dic[map_name] = map_url

	# 		my_list.append(dict(map_dic)) 




	# except Exception as e:
	# 	print(e)
	# 	pass


	# e_imgs = parser.xpath('//table[@class="wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible"]//tbody//div[@class="enemyicon"]//img')
	# # e_imgs = parser.xpath('//table[@class="wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible"]/tbody/tr/td/div/a/img')
	# images = []
	# for j in range(len(e_imgs)):
	# 	# pdb.set_trace()
	# 	img_dic = {}
	# 	image_name = parser.xpath('//table[@class="wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible"]/tbody/tr[{}]/td[1]/div/a/img/@alt'.format(str(j+1)))[0]
	# 	image_str = parser.xpath('//table[@class="wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible"]/tbody/tr[{}]/td[1]/div/a/img/@data-src'.format(str(j+1)))[0]
	# 	image_arr = image_str.split('/')
	# 	image_url = os.path.join(IMG_BASE_URL, image_arr[3], image_arr[4], image_arr[5])
	# 	img_dic[image_name] = image_url
	# 	images.append(dict(img_dic))
	# print(images)

except Exception as e:
	print(e)
	pass


# data = {
# 		"name":name,
# 		"url": url 
# 		# "stage": stage, 
# 		# # "enemy": enemy, 
# 		# "image_urls": images, 
# 		# "extra_image_urls": extra_images,
# 		# "map_url": my_list
# 		# "enemy_img_url": images
# 		}
# my_table = my_table.append(data, ignore_index=True)
# 	# print(my_table.head())

browser.close()
my_table.to_csv(r'./data/koko_imgs.csv', header=HEADERS, index=None, sep=',', mode='a')
