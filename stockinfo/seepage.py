# 导入selenium库和其他需要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import datetime

import sname
import time
import pickle
import os.path as path

# 用pickle.load()从文件读取列表
with open(path.dirname(path.abspath(__file__)) + 'hA.pickle', 'rb') as f:
    hA = pickle.load(f)
with open(path.dirname(path.abspath(__file__)) + 'hB.pickle', 'rb') as f:
    hB = pickle.load(f)
with open(path.dirname(path.abspath(__file__)) + 'sA.pickle', 'rb') as f:
    sA = pickle.load(f)
with open(path.dirname(path.abspath(__file__)) + 'sB.pickle', 'rb') as f:
    sB = pickle.load(f)

print("Get name success and save!")

# 创建一个chrome浏览器对象
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : path.dirname(path.abspath(__file__)) + "report/"}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

for i in hA:
    driver.get("http://stockpage.10jqka.com.cn/" + str(i[0]) + "/bonus/")
    if driver.current_url == "http://stockpage.10jqka.com.cn/":
        continue
    time.sleep(10)

# 关闭浏览器和释放资源
driver.quit()
