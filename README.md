> 參考影片練習
>
> [用 Python 爬蟲與 Flask 實作懶人版個股基本面指標工具](https://www.youtube.com/watch?v=S9mc3CLKzXA&t=2862s)
>
> 補充 create_test_json_file.py
>
> 使用 selenium 操作網頁抓取股票代號，改變顯示資料數量與排序
>
> 利用股票代號來建立 json 檔案供 Postman 跑測試用

- [流程概覽](#流程概覽)
- [使用工具](#使用工具)
- [小記](#小記)
  - [pandas](#pandas)
  - [docker](#docker)
  - [selenium](#selenium)
  - [pytest 參數化測試](#pytest-參數化測試)
  - [Postman](#postman)

---

# 流程概覽
![ima](https://github.com/wadelu23/MarkdownPicture/blob/main/stock_crawler/mermaid-flowchart-main.png?raw=true)

---

# 使用工具
  * [flask](https://flask.palletsprojects.com/en/2.0.x/)
  * [pandas](https://pandas.pydata.org/)
  * [docker](https://www.docker.com/)
  * [selenium](https://www.selenium.dev/)
  * [Postman](https://www.postman.com/)


# 小記
## pandas
```python
# Read HTML tables into a list of DataFrame objects.
dfs = pd.read_html(url)

# <tr>標籤會是列(row)，<td>標籤則是欄(column)
```
```python
datas = df[df[0] == conform_title].iloc[0][1:5].astype(float)
# df[df[0] == conform_title] -> 過濾出符合標題的資料
# .iloc[][1:5] 以 index 位置來取資料，接著取該資料的指定位置資料
```
![image](https://github.com/wadelu23/MarkdownPicture/blob/main/stock_crawler/iloc-example.png?raw=true)

---

## docker
Dockerfile說明
```Dockerfile
# initializes a new build stage
# and sets the Base Image for subsequent instructions.
FROM python:3.8-slim-buster

# sets the working directory for any RUN, CMD, ENTRYPOINT,
# COPY and ADD instructions that follow it in the Dockerfile.
WORKDIR /app

# sets the environment variable <key> to the value <value>.
ENV MY_NAME="John Doe"

# copies new files or directories from <src>
# and adds them to the filesystem of the container at the path <dest>.
# COPY <src> <dest>
COPY requirements.txt requirements.txt

# execute any commands in a new layer on top of the current image and commit the results.
RUN pip3 install -r requirements.txt

COPY . .

# informs Docker that the container listens on the specified network ports at runtime.
EXPOSE 5000

# The main purpose of a CMD is to provide defaults for an executing container.
# 啟動此app的指令
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

```Dockerfile
# creates a mount point with the specified name
# and marks it as holding externally mounted volumes from native host or other containers.
# 一般 Container 重啟時，上次在Container中修改的部分會消失
# 例如資料庫等
# 而將實體主機的指定路徑 映射 到 Container 的指定路徑
# 等於把那資料庫映射一份放在本機，也就是保存操作結果
# 下次Container重啟時，則經由映射取得有保存結果的資料庫
VOLUME /var/log /var/db
```
---
## selenium

[等待頁面加載](https://selenium-python.readthedocs.io/waits.html#waits)

[查找元素](https://selenium-python.readthedocs.io/locating-elements.html#locating-elements)

```python
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select


options = webdriver.ChromeOptions()
options.headless = True # 相當於背景作業，不會跳出瀏覽器視窗
driver = webdriver.Chrome(options=options,)
driver.implicitly_wait(3) # 此處用隱式等待

url = 'https://www.twse.com.tw/zh/page/trading/exchange/TWT53U.html'
driver.get(url)

# 取得 Select
table_length_opt = Select(driver.find_element_by_name("report-table_length"))

view_data_length = "25"
# 選擇每頁幾筆
table_length_opt.select_by_value(view_data_length)

target_th_str = '成交股數'

tr_path = "//table[@id='report-table']/thead/tr"

# 查找元素
tr = driver.find_element_by_xpath(tr_path)

# 找包含指定字串的th
target = tr.find_element_by_xpath(f"th[contains(text(), '{target_th_str}')]")

# 點兩下指定的th，使排序規則為 成交股數(大至小)
action = ActionChains(driver)
action.double_click(target).perform()
```

---
## pytest 參數化測試
```python
import pytest


@pytest.mark.parametrize("test_input,expected", [
                            ("3+5", 8),
                            ("2+4", 6),
                            ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

---
## Postman
[可引入檔案提供變數來迴圈測試](https://learning.postman.com/docs/running-collections/working-with-data-files/)
```
//get the 'value' field from the data file for this request run
pm.iterationData.get("value")
```