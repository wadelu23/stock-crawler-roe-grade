import pandas as pd
import re


def get_table(url):
    dfs = pd.read_html(url)
    df = dfs[2]
    return df


def get_sum(df, op_title):
    # '[\u0041-\u005a|\u0061-\u007a]+' 大小寫英文字母
    # '[\u4e00-\u9fa5]+' 中文字符
    reg = '[\u0041-\u005a|\u0061-\u007a|\u4e00-\u9fa5]+'
    conform_string = re.findall(reg, op_title)

    conform_title = [title for title in df[0]
                     if re.findall(reg, title) == conform_string][0]
    datas = df[df[0] == conform_title].iloc[0][1:5].astype(float)

    sum = datas.sum()
    return round(sum, 1)


def get_roe(stock_no):
    url = f"http://jsjustweb.jihsun.com.tw/z/zc/zcr/zcr0.djhtm?b=Q&a={stock_no}"
    df = get_table(url)

    title = 'ROE(A)─稅後'
    roe = get_sum(df, title)
    return roe


def get_free_cashflow(stock_no):
    url = f"http://jsjustweb.jihsun.com.tw/z/zc/zc30.djhtm?b=Q&a={stock_no}"

    df = get_table(url)
    op_cashflow_sum = get_sum(df, '來自營運之現金流量')

    inv_cashflow_sum = get_sum(df, '投資活動之現金流量')

    free_cashflow = op_cashflow_sum+inv_cashflow_sum
    return free_cashflow


if __name__ == '__main__':
    stock_no = 2330
    print(get_roe(stock_no))
    print(get_free_cashflow(stock_no))
