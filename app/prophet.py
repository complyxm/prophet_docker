# coding: UTF-8
import requests
import json
from datetime import datetime

# 現在価格を取得する
def getPrice():
    response = requests.get('https://coincheck.com/api/rate/btc_jpy',)
    rate_json = response.json()
    rate = rate_json["rate"]
    return rate

# 現在時刻を取得しunixtimeに変換
# Bitcoin現在価格を取得
currentTime = datetime.now().strftime('%Y/%m/%d').decode('unicode-escape')
currentPrice = getPrice()

data =  {
          'date' : '%s' % currentTime, 
          'rate' : '%s' % currentPrice
        }

# Firestoreの参照
from google.cloud import firestore
db = firestore.Client()

# DBのprice collectionを参照する
prices_ref = db.collection(u'prices')

# pricesにデータを格納する
prices_ref.add(data)

# DBのprice collectionをjsonに変換する
pricelists = prices_ref.get()
pricelists = [i.to_dict() for i in pricelists]
enc = json.dumps(pricelists)

# jsonデータをpandasに渡す
import pandas as pd
df = pd.read_json(enc)

# jsonデータのcolumnをprophetの指定名称に書き換え、時系列でソートする
df = df.rename(columns={'date': 'ds', 'rate': 'y'})
df['ds'] = pd.to_datetime(df['ds']) 
df = df.sort_values('ds')

# 予測モデルの指定
from fbprophet import Prophet
model = Prophet(yearly_seasonality = True, weekly_seasonality = True, daily_seasonality = True)

# 予測モデルへのdf読み込み
model.fit(df)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# 30日後の予測値と今日の価格を出力
f = forecast['yhat'].tail(1).values[0]
today = df['y'].tail(1).values[0]


if f >= today:
   result = "本日の価格は %d で、１ヶ月後の価格は %d となり価格上昇傾向です" % (today,f)
else:
   result = "本日の価格は %d で、１ヶ月後の価格は %d となり価格下落傾向です" % (today,f)

def printResult():
   print(result)

printResult()