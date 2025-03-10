# Auto trader for Mini QMT

功能说明: 本程序在用户选定的股票池中，利用Mini QMT推送数据，实时监控股价，在股票上板的一瞬间，进行排单。

## 1. 安装python

下载地址: <https://www.python.org/downloads/>

## 2. 下载

下载地址: <https://dict.thinktrader.net/packages/xtquant_240613.rar>

## 3. 安装xtquant

将xtquant_240613.rar解开后复制到 <python安装目录>/Lib/site-packags/ 目录下

## 4. 安装其它依赖包

打开windows控制台，输入: pip install pandas terminaltables3 simple_chalk colorama apscheduler pytz

## 5. 运行Mini QMT

记得登录界面，勾选 "独立交易", 登录QMT

## 5. 修改配置文件 `config.py`

```py
# QMT安装路径 - 根据实际情况自行修改
QMT_PATH = "C:\\gj_trader\\userdata_mini"
# 资金账号 - 根据实际情况自行修改
QMT_ACCOUNT_ID = "XXXXXXX"
# 这个不要修改，固定是STOCK
QMT_ACCOUNT_TYPE = "STOCK"
```

## 6. 运行auto-trader

在运行打板程序之前，先把`候选标的`维护到`stocks.csv`文件中, 栏位 `证券代码` 是必须要有的

```csv
证券代码,证券名称,5涨,10涨,20涨,30涨,45涨,60涨
603918.SH,金桥信息,-0.66,-14.5,13.6,50,32.6,21.8
000536.SZ,华映科技,3.79,11.1,11.7,34.7,26.7,-1.63
```

打开windows控制台，输入: python app.py

[![alt](./images/2025-03-10_18-24-52.jpg)]

## 6. 策略定制

打开 `strategy.py`, 在 buy 函数里面添加 你自己的逻辑

Made with ♥ by 满仓干
