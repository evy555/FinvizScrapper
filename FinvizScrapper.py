import pandas as pd
import requests
from collections import Counter

df = pd.read_csv("SCHV_Fund_Holdings_Market_Open.csv")

### Fix common ticker issues. I.E. BRK.A and BRK.B and GOOG and GOOGL
df['Symbol'][0] = 'BRK.A'
df['Symbol'] = df['Symbol'].str.replace(".","-")

### First Finviz Scrape to set the Dataframe
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}
reg_url = "https://finviz.com/quote.ashx?t={}".format(df['Symbol'][0].replace(".","-"))
r = requests.get(reg_url, headers=header)
test = pd.read_html(r.text)
test[6]

### Get Metric names in a list

metrics = test[6][0]
for i in [2,4,6,8,10]:
    metrics = metrics.append(test[6][i])

### Clean dataframe
metrics.reset_index(drop=True, inplace=True)
metrics[28] = "EPS next Y (%)"

### Set Column Header for DataFrame
count = 0
for i in metrics:
    df.loc[:,i] = ''

### Get Metric Values in a list
metric_values = test[6][1]
for i in [3,5,7,9,11]:
    metric_values = metric_values.append(test[6][i])

### Create list of tuples to add to Dataframe
metric_value_list = list(zip(metrics,metric_values))

### Add values to DataFrame
for x,y in metric_value_list:
    df.loc[0,x] = y

### Pull data from Finviz
for symbol in range(1,len(df.index.values)):
    try:
        reg_url = "https://finviz.com/quote.ashx?t={}".format(df['Symbol'][symbol].replace(".","-"))
        r = requests.get(reg_url, headers=header)
        test = pd.read_html(r.text)

        metric_values = test[6][1]
        for i in [3,5,7,9,11]:
            metric_values = metric_values.append(test[6][i])

        metric_value_list = list(zip(metrics,metric_values))

        for x,y in metric_value_list:
            df.loc[symbol,x] = y
    except:
        print("Symbol {} did not work".format(df['Symbol'][symbol]))
        pass

### Write DataFrame to CSV
df.to_csv('SCHV.csv')
