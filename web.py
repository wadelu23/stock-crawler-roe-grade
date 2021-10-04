from flask import Flask, request, render_template
import crawler
from stock_info import Stock, metric

app = Flask(__name__)


@app.route('/stock_grade', methods=['POST'])
def stock_grade():
    para = request.get_json()
    stock_no = para["stock_no"]
    stock = Stock(stock_no, 0, 0, 'NG')
    try:
        stock.roe = crawler.get_roe(stock.no)
        stock.fcf = crawler.get_free_cashflow(stock.no)
        stock.grade = metric(stock.roe, stock.fcf)
    except IndexError:
        return {'message': 'Sorry! The stock info not found.'}, 404

    return stock.__dict__, 200
