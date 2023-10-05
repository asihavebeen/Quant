# 导入selenium和其他需要的库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 定义一个函数，用于获取当前页面的所有股票的股票代码，并添加到列表中
def get_stock_codes(driver, button, id, stock_code_list):
    # 切换页面
    button = driver.find_element(By.ID, button)
    button.click()
    # 定位到股票列表的表格元素
    table = driver.find_element(By.ID, id)
    # 定位到表格中的所有行元素
    rows = table.find_elements(By.TAG_NAME, "li")
    # 遍历每一行元素
    for row in rows:
        # 定位到行中的第一列元素，即股票代码元素
        code = row.text.split('\n')[0]
        called = row.text.split('\n')[1]
        # code = re.findall(pattern_num, row.text)
        # called = re.findall(pattern_name, row.text)
        # 添加到列表
        stock_code_list.append((code, called))

def get_sname():
    # 创建一个chrome浏览器对象
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # 设置为无界面模式
    options.add_argument("--disable-images") # 设置不加载图片
    driver = webdriver.Chrome(options=options)

    # 打开网站
    driver.get("https://quote.stockstar.com/stock/stock_index.htm")

    # 等待页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "seo_keywordsCon")))

    # 定义四个空列表，用于存储所有股票的股票代码，沪A、沪B、深A、深B
    stock_codes_hA = []
    stock_codes_hB = []
    stock_codes_sA = []
    stock_codes_sB = []

    # 定义匹配正则表达式
    # pattern_num = r"<a herf*>*</a></span>"
    # pattern_name = r"</span><a herf*>*</a>"

    # 调用函数，获取当前页面的所有股票的股票代码
    get_stock_codes(driver, "index_parent_0", "index_data_0", stock_codes_hA)
    print("Get Stock Codes hA Complete")
    get_stock_codes(driver, "index_parent_1", "index_data_1", stock_codes_hB)
    print("Get Stock Codes hB Complete")
    get_stock_codes(driver, "index_parent_2", "index_data_2", stock_codes_sA)
    print("Get Stock Codes sA Complete")
    get_stock_codes(driver, "index_parent_3", "index_data_3", stock_codes_sB)
    print("Get Stock Codes sB Complete")

    # 打印列表中的所有股票代码，以逗号分隔
    print(len(stock_codes_hA))
    print(len(stock_codes_hB))
    print(len(stock_codes_sA))
    print(len(stock_codes_sB))

    # 关闭浏览器对象
    driver.quit()

    return stock_codes_hA, stock_codes_hB, stock_codes_sA, stock_codes_sB
