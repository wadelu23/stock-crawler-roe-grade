import pandas as pd
import json
from typing import List
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def get_stock_no_by_pandas(page_source) -> List:
    dfs = pd.read_html(page_source)
    df = dfs[0]

    # 這裡只設定大概條件，過濾掉查無資料的證券代號
    fliter = (df["證券代號"] > 1000)
    datas = df[fliter]["證券代號"].astype('int').tolist()
    return datas


def get_stock_no_by_bs4(page_source) -> List:
    soup = BeautifulSoup(page_source, 'html.parser')

    table = soup.find('table', attrs={'id': 'report-table'})

    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    del rows[0]
    datas = []
    for row in rows:
        no = int(row.find_all('td')[0].text)
        if no > 1000:
            datas.append(no)

    return datas


def create_json_file(datas: List):
    stock_no_json = []
    for stock_no in datas:
        stock_no_json.append({'stock_no': stock_no})

    with open("./stock_no.json", "w+") as jsonFile:
        json.dump(stock_no_json, jsonFile)


if __name__ == '__main__':
    url = 'https://www.twse.com.tw/zh/page/trading/exchange/TWT53U.html'

    view_data_length = "25"
    target_th_str = '成交股數'

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options,)
    driver.implicitly_wait(3)
    driver.get(url)

    table_length_opt = Select(
        driver.find_element_by_name("report-table_length"))
    # 選擇一頁顯示25筆
    table_length_opt.select_by_value(view_data_length)

    tr_path = "//table[@id='report-table']/thead/tr"

    tr = driver.find_element_by_xpath(tr_path)

    # 點 '成交股數' 改變排序
    target = tr.find_element_by_xpath(
        f"th[contains(text(), '{target_th_str}')]")

    action = ActionChains(driver)
    action.double_click(target).perform()

    # 取得股票代號的2種方式
    # 1. pandas
    datas = get_stock_no_by_pandas(driver.page_source)
    # 2. BeautifulSoup
    # datas = get_stock_no_by_bs4(driver.page_source)

    driver.quit()

    create_json_file(datas)
