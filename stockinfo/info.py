# 导入selenium库和其他需要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import datetime

import sname
import pickle
import os.path as path

# 记录数据的数据结构
class infoClass:
    def __init__(self):
        self.code = 1  # 股票的代码，上证股票以sh开头，深证股票以sz开头
        self.date = 1  # 交易日期
        self.open = 1  # 开盘价
        self.high = 1  # 最高价
        self.low = 1  # 最低价
        self.close = 1  # 收盘价
        self.change = 1  # 涨跌幅，复权之后的真实涨跌幅，保证准确。可以据此计算复权价格。
        self.volume = 1  # 成交量
        self.money = 1  # 成交额
        self.traded_market_value = 1  # 流通市值
        self.market_value = 1  # 总市值
        self.turnover = 1  # 换手率，成交量/流通股本
        self.adjust_price = 1  # 收盘价的后复权价，复权开始时间为股票上市日，精确到小数点后10位
        self.report_date = 1  # 最近一期财务报告实际发布的日期
        self.report_type = 1  # 最近一期财务报告的类型，3-31对应一季报，6-30对应半年报，9-30对应三季报，12-31对应年报
        self.PE_TTM = 1  # 最近12个月市盈率，股价/最近12个月归属母公司的每股收益TTM
        self.PS_TTM = 1  # 最近12个月市销率，股价/最近12个月每股营业收入
        self.PC_TTM = 1   # 最近12个月市现率，股价/最近12个月每股经营现金流
        self.PB = 1  # 市净率，股价/最近期财报每股净资产
        self.adjust_price_f = 1  # 收盘价的前复权价，复权开始时间为股票最近一个交易日，精确到小数点后10位

# 获取数据的函数
def getInfo(driver, id, forward):
    # 返回的数据结构
    infoRecord = infoClass()
    # 同花顺
    url = "http://stockpage.10jqka.com.cn/" + str(id)
    driver.get(url)
    if driver.current_url == "http://stockpage.10jqka.com.cn/":
        return infoRecord
    
    # 等待页面加载完成
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "in_squote")))
    except:
        return infoRecord

    allPlace = driver.find_element(By.CLASS_NAME, "m_header")
    iFrame = allPlace.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iFrame)
    innerHTML = driver.find_element(By.TAG_NAME, "html")

    # 记录结果
    infoRecord.code = forward + str(id) # 股票的代码，上证股票以sh开头，深证股票以sz开头
    infoRecord.date = innerHTML.find_element(By.ID, "timeshow").text # 交易日期
    infoRecord.open = innerHTML.find_element(By.ID, "topenprice").text # 开盘价
    infoRecord.high = innerHTML.find_element(By.ID, "thighprice").text # 最高价
    infoRecord.low = innerHTML.find_element(By.ID, "tlowprice").text # 最低价
    infoRecord.close = innerHTML.find_element(By.ID, "hexm_curPrice").text # 收盘价
    infoRecord.change = innerHTML.find_element(By.ID, "hexm_float_price").text # 涨跌幅，复权之后的真实涨跌幅，保证准确。可以据此计算复权价格。
    infoRecord.volume = innerHTML.find_element(By.ID, "tamount").text # 成交量
    infoRecord.money = innerHTML.find_element(By.ID, "tamounttotal").text # 成交额
    infoRecord.traded_market_value = innerHTML.find_element(By.ID, "flowvalue").text # 流通市值
    infoRecord.market_value = innerHTML.find_element(By.ID, "tvalue").text # 总市值
    infoRecord.turnover = innerHTML.find_element(By.ID, "tchange").text # 换手率，成交量/流通股本
    infoRecord.PB = innerHTML.find_element(By.ID, "tvaluep").text # 市净率，股价/最近期财报每股净资产

    # 东方财富
    dongUrl = "http://quote.eastmoney.com/" + str(infoRecord.code) + ".html"
    driver.get(dongUrl)
    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "container")))

    firstPlace = driver.find_element(By.CLASS_NAME, "container")
    halfPlace = firstPlace.find_element(By.CLASS_NAME, "zsquote3l.zs_brief")
    infoRecord.PE_TTM = halfPlace.find_element(By.CLASS_NAME, "price_draw.blinkblue").text # 最近12个月市盈率，股价/最近12个月归属母公司的每股收益TTM

    # 下载财报数据
    financeUrl = "http://stockpage.10jqka.com.cn/" + str(id) + "/finance/"
    driver.get(financeUrl)
    
    # 等待页面加载完成
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main_content")))
    except:
        return infoRecord

    allPage = driver.find_element(By.CLASS_NAME, "main_content")
    iFrame = allPage.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iFrame)
    innerHTML = driver.find_element(By.TAG_NAME, "html")
    innerTable = innerHTML.find_element(By.ID, "cwzbTable")
    downButton = innerTable.find_element(By.ID, "exportButton")
    downButton.click()

    # 记录分红和转股的情况
    bonusUrl = "http://stockpage.10jqka.com.cn/" + str(id) + "/bonus/"
    driver.get(bonusUrl)
    
    # 等待页面加载完成
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "main_content")))
    except:
        return infoRecord

    allPage = driver.find_element(By.CLASS_NAME, "main_content")
    iFrame = allPage.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iFrame)
    innerHTML = driver.find_element(By.TAG_NAME, "html")
    bonusTable = innerHTML.find_element(By.ID, "bonus_table")
    # 获取表格中的所有行元素
    rows = bonusTable.find_elements(By.TAG_NAME, "tr")
    # 获取行中的所有单元格元素
    cells = rows[0].find_elements(By.TAG_NAME, "th")
    # 遍历每一个单元格元素
    for cell in cells:
        # 打印单元格的文本内容
        print(cell.text, end=" ")
    print()
    # 遍历每一行元素
    for row in rows[1:]:
        # 获取行中的所有单元格元素
        cells = row.find_elements(By.TAG_NAME, "td")
        # 遍历每一个单元格元素
        for cell in cells:
            # 打印单元格的文本内容
            print(cell.text, end=" ")
        # 换行
        print()

    infoRecord.PS_TTM = "0" # 最近12个月市销率，股价/最近12个月每股营业收入
    infoRecord.PC_TTM = "0" # 最近12个月市现率，股价/最近12个月每股经营现金流
    infoRecord.adjust_price_f = "0" # 收盘价的前复权价，复权开始时间为股票最近一个交易日，精确到小数点后10位
    infoRecord.adjust_price = "0" # 收盘价的后复权价，复权开始时间为股票上市日，精确到小数点后10位

    return infoRecord

# 记录数据进表格
def recordFrame(frame, record, allColumns):
    row = [record.code, record.date, record.open, record.high, record.low, record.close,
           record.change, record.volume, record.money, record.traded_market_value,
           record.market_value, record.turnover, record.adjust_price, record.report_date,
           record.report_type, record.PE_TTM, record.PS_TTM, record.PC_TTM, record.PB, record.adjust_price_f]
    lineDict = {}

    for i in range(len(row)):
        lineDict[allColumns[i]] = row[i]

    frame = pd.concat([frame, pd.DataFrame([lineDict])], ignore_index=True)
    return frame

# 把数据组织成表格
def getFrame(driver, hA, hB, sA, sB):
    # 初始化并填入内容
    allColumns = ["code", "date", "open", "high", "low", "close", "change",
                  "volume", "money", "traded_market_value", "market_value",
                  "turnover", "adjust_price", "report_date", "report_type",
                  "PE_TTM", "PS_TTM", "PC_TTM", "PB", "adjust_price_f"] 
    myFrame = pd.DataFrame(data=None, columns=allColumns)
    
    for i in hA:
        record = getInfo(driver, i[0], "sh")
        myFrame = recordFrame(myFrame, record, allColumns)
    for i in hB:
        record = getInfo(driver, i[0], "sh")
        myFrame = recordFrame(myFrame, record, allColumns)
    for i in sA:
        record = getInfo(driver, i[0], "sz")
        myFrame = recordFrame(myFrame, record, allColumns)
    for i in sB:
        record = getInfo(driver, i[0], "sz")
        myFrame = recordFrame(myFrame, record, allColumns)

    return myFrame


# 获取所有的股票代码和名称
hA, hB, sA, sB = sname.get_sname()

# 用pickle.dump()将列表存储到文件
with open(path.dirname(path.abspath(__file__)) + 'hA.pickle', 'wb') as f:
    pickle.dump(hA, f)
with open(path.dirname(path.abspath(__file__)) + 'hB.pickle', 'wb') as f:
    pickle.dump(hB, f)
with open(path.dirname(path.abspath(__file__)) + 'sA.pickle', 'wb') as f:
    pickle.dump(sA, f)
with open(path.dirname(path.abspath(__file__)) + 'sB.pickle', 'wb') as f:
    pickle.dump(sB, f)

print("Get name success and save!")

# # 用pickle.load()从文件读取列表
# with open(path.dirname(path.abspath(__file__)) + 'hA.pickle', 'rb') as f:
#     hA = pickle.load(f)
# with open(path.dirname(path.abspath(__file__)) + 'hB.pickle', 'rb') as f:
#     hB = pickle.load(f)
# with open(path.dirname(path.abspath(__file__)) + 'sA.pickle', 'rb') as f:
#     sA = pickle.load(f)
# with open(path.dirname(path.abspath(__file__)) + 'sB.pickle', 'rb') as f:
#     sB = pickle.load(f)

# 创建一个chrome浏览器对象
options = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : path.dirname(path.abspath(__file__)) + "report/",
#          "download.prompt_for_download": False}
prefs = {"download.prompt_for_download": False}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

result = getFrame(driver, hA, hB, sA, sB)

result.to_csv("./" + str(datetime.datetime.year) + "/" + 
              str(datetime.datetime.year) + "-" + str(datetime.datetime.month) + "-" + str(datetime.datetime.day) + ".csv")

# 关闭浏览器和释放资源
driver.quit()

