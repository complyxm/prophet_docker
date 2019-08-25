# coding: UTF-8
from flask import Flask, render_template
from google.cloud import firestore
import json

app = Flask(__name__)

# DB接続〜予測データの呼び出し
db = firestore.Client()
forecasts_ref = db.collection(u'forecasts')
forecasts_data = forecasts_ref.get()
forecasts_data = [i.to_dict() for i in forecasts_data]
forecasts_data_json = json.dumps(forecasts_data)

import pandas as pd
df = pd.read_json(forecasts_data_json)
df = df.sort_values('date')

df_date = df.iloc[-1]['date'].strftime('%Y/%m/%d') #観測日起算で30日後の予測日
df_forecast = df.iloc[-1]['forecast'] #観測日起算で計測した予測データ

# 観測日当日のデータ呼び出し
prices_ref = db.collection(u'prices')
pricelists = prices_ref.get()
pricelists = [i.to_dict() for i in pricelists]
pricelists_json = json.dumps(pricelists)

df_price = pd.read_json(pricelists_json)
df_price = df_price.sort_values('date')
df_today = df_price.iloc[-1]['rate'] #観測日当日のデータ

print(df_today)
print(df_date)
print(df_forecast)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)