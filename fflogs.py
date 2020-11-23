from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os

from selenium.webdriver import Chrome, Firefox, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

from time import sleep
from lxml import etree
import pandas as pd



url = "https://cn.fflogs.com/character/cn"

browser = Firefox()
browser.implicitly_wait(10)
browser.maximize_window()


headers = ['boss', 'best_percent', 'highest_dps', 'kills',
			'fastest','rank_percent','allstar', 'rank']


my_table = pd.DataFrame(columns=headers)

browser.get(url+"/{}/{}".format(紫水栈桥, 落花微塵))
sleep(3)

parser = etree.HTML(browser.page_source)
# result = etree.tostring(parser)
# print(result.decode('utf-8'))

#collecting all container into a list and going through each one
rows = parser.xpath('//table[@id="boss-table-33"]/tbody/tr')


for tr in list(rows):
	try:
		columns = []
		boss = tr.xpath('.//a[@class="Boss zone-boss-cell"]/text()')[0]
		columns.append(boss);

		cols = [col.text.replace('\n','').replace('\t','') for col in list(tr)]
		columns.extend(cols)
		while '' in columns:
			columns.remove('')
		data = dict(zip(headers, columns))
		my_table = my_table.append(data, ignore_index=True)

	except:
		print('error')



# #closing the browser window
browser.close()
print(my_table.head())


my_table.to_csv(r'./fflogs.csv', index=None, sep=',', mode='a')





