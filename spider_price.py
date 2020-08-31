# -*- coding: utf-8 -*-
import requests
from lxml import etree
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
import json
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

# API 地址+文档：https://pro.coinmarketcap.com/account


# 与excel表中顺序对应,与 接口 parameters 对应（顺序不对应）
TOKENS = [
    'BTC',
    'ETH',
    'XRP',
    'BCH',
    'LTC',
    'EOS',
    'BNB',
    'ADA',
    'XLM',
    'TRX',
    'ETC',
    'HT',
    'NEO',
    'MIOTA',
    'ZEC',
    'OKB',
    'QTUM',
    'DX',
    'ELF',
    'WICC',
    'GXC',
    'PAI',
    'CTXC',
    'STORJ',
    'CMT',
    'MFT',
    'RUFF',
    'TNB',
    'MDS',
]

# 全局数组，保存抓取 token 信息
RESULT = []


def getPriceInfo():
    ''' 获取 token 价格 '''
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC,ETH,XRP,BCH,LTC,EOS,BNB,ADA,XLM,NEO,MIOTA,ZEC,QTUM,HT,GXC,PAI,STORJ,CTXC,CMT,TNB,MFT,DX,DACC,RUFF,MDS,ELF,WICC,OKB,ETC,TRX',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'af108ddb-cc3a-429e-b408-087dc8a71a11',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        print(response.text)
        data = json.loads(response.text)

        for obj in TOKENS:
            dic = {'tokenName': obj, 'usdtPrice': data['data'][obj]['quote']['USD']['price'],
                   'rank': data['data'][obj]['cmc_rank'], 'marketCap': data['data'][obj]['quote']['USD']['market_cap']}
            print(dic)
            RESULT.append(dic)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def getUSDRate():
    ''' 获取美元汇率 '''
    # 新浪财经
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=96683251_hao_pg&wd=%E7%BE%8E%E5%85%83%E6%B1%87%E7%8E%87&oq=%25E7%25BE%258E%25E5%2585%2583%25E6%25B1%2587%25E7%258E%2587%2520python%2520%25E6%258E%25A5%25E5%258F%25A3&rsv_pq=849622a40002b0a2&rsv_t=3c97aODwSAtR9tXCNOIUwwMxmD4KkKOIKMP6XkUfkYHX16WZ8o7ql3pF8Jp2OEcOzsEROyMy&rqlang=cn&rsv_enter=1&inputT=564&rsv_sug3=19&rsv_sug1=10&rsv_sug7=100&rsv_sug2=0&rsv_sug4=815&rsv_sug=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    res = requests.get(url, headers=headers, verify=False)
    res_status = res.status_code
    if res_status == 200:
        selector = etree.HTML(res.text)
        arr = selector.xpath(
            '//*[@id="2"]/div[1]/div[1]/div[1]/div[1]/span[1]/text()')
        usdPrice = arr[0]
        print('美元价格' + usdPrice)
        return usdPrice


def getHuobiUSDTPrice():
    ''' 获取火币USDT买入价格 '''
    url = 'https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=1&coinId=2&tradeType=sell&blockType=general&online=1'
    res = requests.get(url, verify=False)
    res_status = res.status_code
    if res_status == 200:
        # 将json转为python对象
        obj = json.loads(res.text)
        huobiUsdtPrice = obj['data'][0]['price']
        print('USDT价格' + str(huobiUsdtPrice))
        return huobiUsdtPrice


def getFearAndGreedIndex():
    ''' 获取恐惧贪婪指数对象 '''
    url = 'https://api.alternative.me/fng/'
    res = requests.get(url, verify=False)
    res_status = res.status_code
    if res_status == 200:
        resData = json.loads(res.text)
        resData = resData['data'][0]

        name = resData['value_classification']
        value = resData['value']
        # 默认绿色，在恐惧的时候显示绿色
        color = '3cb371'

        if name == 'Fear':
            name = '恐惧'
        elif name == 'Greed':
            name = '贪婪'
            color = 'CC0000'

        currentTime = int(resData['timestamp'])
        timeArray = time.localtime(currentTime)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        dic = {'name': name, 'value': value,
               'time': formatTime, 'color': color}
        return dic


def write2Excel():
    ''' 写入 excel '''
    workBook = load_workbook('/Users/dolin999/Desktop/out.xlsx')
    workSheet = workBook['record']
    for i, obj in enumerate(RESULT):
        usdtPrice = obj['usdtPrice']
        rank = obj['rank']
        marketCap = obj['marketCap']

        workSheet['F{}'.format(i + 3)] = float(usdtPrice)
        workSheet['I{}'.format(i + 3)] = float(rank)
        workSheet['J{}'.format(i + 3)] = float(marketCap)

    # 恐惧贪婪 cell 填写
    fearGreedDic = getFearAndGreedIndex()
    print(fearGreedDic)
    name = fearGreedDic['name']
    value = fearGreedDic['value']
    cellColor = fearGreedDic['color']
    fearGreedCell = workSheet['A1']
    fearGreedCell.fill = PatternFill(
        start_color=cellColor, end_color=cellColor, fill_type="solid")
    fearGreedCell.value = "{0} : {1}".format(name, value)

    # 美元价格
    workSheet['K3'] = str(getUSDRate())

    # 火币usdt价格
    workSheet['K5'] = getHuobiUSDTPrice()

    workBook.save('/Users/dolin999/Desktop/out.xlsx')


def main():
    getPriceInfo()
    write2Excel()


if __name__ == '__main__':
    main()
