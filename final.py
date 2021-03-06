# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C7I3SfP8yM0I-ticAdzYqaeBwhIp1YWe
"""

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

from google.colab import drive
drive.mount('/content/drive')

import datetime
import numpy as np
import pandas as pd
import datetime
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import datasets, linear_model, metrics
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns



# fields = ['timestamp', 'text','likes','replies','retweets']
field = ['timestamp','text']
df = pd.read_csv('/content/drive/MyDrive/tweets.csv', delimiter=';', usecols=field,nrows=12000000)

def dt(x):
    t = pd.Timestamp(x)
    return pd.Timestamp.date(t)

df.timestamp = df.timestamp.apply(dt)

df['timestamp'].value_counts()
sdf=pd.DataFrame(df['timestamp'].value_counts())
sdf = sdf.reset_index()
sdf.columns = ['timestamp','tweets_number']
sdf

df.dropna(inplace=True)

df['scores'] = df['text'].apply(lambda review: sid.polarity_scores(review))
df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])
drop = ['text','scores']
df = df.drop(drop,axis = 1)

cumulative_compound = df.groupby(['timestamp'])['compound'].sum()
cumulative_compound = cumulative_compound.to_frame().reset_index()

##bitcoin
fields = ['Date', 'Close']
bitcoin = pd.read_csv('/content/drive/MyDrive/coin_Bitcoin.csv', delimiter=',', usecols=fields)
bitcoin.Date = bitcoin.Date.apply(dt)
bitcoin = bitcoin.rename(columns={'Date' : 'timestamp'})

#df1 merging
df1 = pd.merge(bitcoin,cumulative_compound,how='inner',on='timestamp')
df1 = pd.merge(df1,sdf,how='inner',on='timestamp')
#df1 = pd.merge(df,df1,how='inner',on='timestamp')

df1.head()

import datetime
df1 = df1[df1['timestamp'] > datetime.date(2018, 11, 23)]
df1 = df1.sort_values(by=['timestamp'], ascending=True)

label = ['timestamp','Close']
X = df1.drop(label, axis = 1)
Y = df1['Close']
reg = linear_model.LinearRegression()
reg.fit(X,Y)
# Print out the R^2 for the model against the full dataset
print(reg.score(X,Y))
print(reg.intercept_)
print(reg.coef_)

Y_pred = reg.predict(X)

residuals = Y - Y_pred

sns.distplot(residuals);
plt.ylabel("Frequency",fontsize=12)
plt.xlabel("Residual",fontsize=12)
plt.title('Residual Histogram',fontsize=14)
plt.show()

from sklearn.model_selection import train_test_split

n = 1
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size = 0.2,random_state=n)

reg.fit(X_train, Y_train)

  
# Fit the model against the training data
# Evaluate the model against the testing data
print(reg.score(X_train, Y_train)*100)
print(reg.score(X_test, Y_test)*100)

ax = sns.regplot(x=Y_test,y=reg.predict(X_test), data=df1)
ax.set(xlabel='Actual (log)', ylabel='Predicted (log)', title = 'Bitcoin Price: Predicted vs. Actual (log)')

ax = sns.regplot(x=Y_train,y=reg.predict(X_train), data=df1)
ax.set(xlabel='Actual, US$', ylabel='Predicted, US$', title = 'Bitcoin Price: Predicted vs. Actual')

y1 = pd.Series(df1['Close'])
y2 = pd.Series(df1['compound'])
x = pd.Series(df1['timestamp'])

fig, _ = plt.subplots()

ax = plt.gca()
ax2 = ax.twinx()

ax.plot(x,y1,'b')
ax2.plot(x,y2,'g')
ax.set_ylabel("Bitcoin Price",color='b',fontsize=12)
ax2.set_ylabel("Number of Tweets",color='g',fontsize=12)
# ax.grid(True)
plt.title("Bitcoin Price vs. Compound", fontsize=14)
ax.set_xlabel('Date', fontsize=12)
fig.autofmt_xdate()
# ax.yaxis.set_major_formatter(tick.FuncFormatter(y_fmt))
plt.show()

y1 = pd.Series(df1['Close'])
y2 = pd.Series(df1['tweets_number'])
x = pd.Series(df1['timestamp'])

fig, _ = plt.subplots()

ax = plt.gca()
ax2 = ax.twinx()

ax.plot(x,y1,'b')
ax2.plot(x,y2,'g')
ax.set_ylabel("Bitcoin Price",color='b',fontsize=12)
ax2.set_ylabel("Number of Tweets",color='g',fontsize=12)
# ax.grid(True)
plt.title("Bitcoin Price vs. Number of tweets", fontsize=14)
ax.set_xlabel('Date', fontsize=12)
fig.autofmt_xdate()
# ax.yaxis.set_major_formatter(tick.FuncFormatter(y_fmt))
plt.show()

# from sklearn import datasets, linear_model, metrics

# # regression coefficients
# print('Coefficients: ', reg.coef_)
 
# # variance score: 1 means perfect prediction
# print('Variance score: {}'.format(reg.score(X_test, Y_test)))
 
# # plot for residual error
 
# ## setting plot style
# plt.style.use('fivethirtyeight')
 
# ## plotting residual errors in training data
# plt.scatter(reg.predict(X_train), reg.predict(X_train) - Y_train,
#             color = "green", s = 10, label = 'Train data')
 
# ## plotting residual errors in test data
# plt.scatter(reg.predict(X_test), reg.predict(X_test) - Y_test,
#             color = "blue", s = 10, label = 'Test data')
 
# ## plotting line for zero residual error
# plt.hlines(y = 0, xmin = 0, xmax = 50, linewidth = 50)
 
# ## plotting legend
# plt.legend(loc = 'upper right')
 
# ## plot title
# plt.title("Residual errors")
 
# ## method call for showing the plot
# plt.show()

from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt



# cross_val_predict returns an array of the same size as `y` where each entry
# is a prediction obtained by cross validation:
predicted = cross_val_predict(reg, X, Y, cv=10)

fig, ax = plt.subplots()
ax.scatter(Y, predicted, edgecolors=(0, 0, 0))
ax.plot([Y.min(), Y.max()], [Y.min(), Y.max()], "k--", lw=4)
ax.set_xlabel("Measured")
ax.set_ylabel("Predicted")
plt.show()