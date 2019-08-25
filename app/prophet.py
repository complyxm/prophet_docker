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
# 30日後の日付
ds_f = pd.to_datetime(forecast['ds'].tail(1).values[0]).strftime('%Y/%m/%d')
ds_f_unicode = ds_f.decode('unicode-escape') #DB保存用にunicode化

# 30日後の予測価格(ラベルなし)
f = forecast['yhat'].tail(1).values[0]
f_str = '{0:.1f}'.format(f) #str化して桁を調整
f_unicode = str(f_str).decode('unicode-escape') #DB保存用にunicode化

# 計算日当日の価格(ラベルなし)
today = df['y'].tail(1).values[0]
today_unicode = str(today).decode('unicode-escape') #DB保存用にunicode化
today_str = today_unicode.encode() #str化

# 予測価格を格納するためのデータセット
data_f =  { 
           'date' : '%s' % ds_f_unicode, 
           'forecast' : '%s' % f_unicode,
          }

# DBのforecasts collectionを参照する
forecasts_ref = db.collection(u'forecasts')
forecasts_ref.add(data_f)

f_int = int(f)
today_int = int(today)

if f_int >= today_int:
   result = "本日の価格は %s で、１ヶ月後の価格は %s となり価格下落傾向です" % (today_int,f_int)
else:
   result = "本日の価格は %s で、１ヶ月後の価格は %s となり価格下落傾向です" % (today_int,f_int)

def printResult():
   print(result)

printResult()

# Test Set
#print(data_f)
#print(type(f))
#print(type(today))
#print(type(f_str))
#print(type(f_unicode))
#print(type(today_str))
#print(type(today_unicode))
#print(type(f_int))
#print(type(today_int))