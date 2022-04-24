#!/usr/bin/env python
# coding: utf-8

# In[1]:


# fig = plt.figure(figsize=(13,6))
# plt.title('Close vs Date')
# plt.xlabel('Dates')
# plt.ylabel('Prices')
# plt.plot(train_data['Close'], color='green', label='training_data')
# plt.plot(test_data['Close'], color='red', label='test_data')


# In[19]:


# !pip install pmdarima


# In[21]:


# from pmdarima.arima import auto_arima
# from pmdarima.arima import ADFTest

# adf_test = ADFTest(alpha=0.05)
# adf_test.should_diff(df['Close'])


# In[58]:


# predictions = []
# for i in range(len(test_data)):
#     model = ARIMA(train_data, order=(4,1,0))
#     model_fit = model.fit()
#     output = model_fit.forecast()
#     predictions.append(output[0])
#     train_data.append(test_data[i])


# In[ ]:


# arima_model = auto_arima(train_data['Close'],start_p=0, start_P=0, start_q=0, start_Q=0, d=0, D=0,max_p=5, max_P=5, max_q=5, max_Q=5, max_d=5, max_D=5, m=12, random_state=17, n_fits=10, error_action='warn')


# In[22]:


# arima_model.summary()


# In[29]:


# test_data.index


# In[26]:


# predicted = pd.DataFrame(arima_model.predict(n_periods=test_data.shape[0]), index=test_data.index)
# predicted.head(5)


# In[33]:


# predicted.columns=['Close']


# In[ ]:


# plt.figure(figsize=(16,9))
# plt.xlabel('dates')
# plt.ylabel('prices')
# plt.title('Plottt')
# plt.plot(df[0:int(df.shape[0]*0.9)]['Close'], color='green', label='training_data')
# plt.plot(test_df['Close'], color='red', label='test_data')
# plt.plot(predictions_df['Close'], color='orange', label='predicted_values')
# plt.legend()


# In[ ]:


# plt.figure(figsize=(10,6))
# plt.xlabel('dates')
# plt.ylabel('prices')
# plt.title('Plottt')
# # plt.plot(df[0:int(df.shape[0]*0.9)]['Close'], color='green', label='training_data')
# plt.plot(test_df['Close'], color='green', label='test_data')
# plt.plot(predictions_df['Close'], color='red', label='predicted_values')
# plt.legend()


# In[56]:


# from sklearn.metrics import mean_absolute_percentage_error


# In[ ]:


# mean_absolute_percentage_error(test_df['Close'],predictions_df['Close'])


# In[9]:

#from Connecting_and_Storing_Data import Connect_Store_Data
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import mysql.connector
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

class Get_Predictions:
    def __init__(self, stock):
        self.host = "firstdatabase.csdx2ljymbci.ap-south-1.rds.amazonaws.com"
        self.port = "3306"
        self.db = "BitCoin_db"
        self.username = "admin"
        self.password = "Admin#123"
        self.stock = stock
        self.cryptos = {'BTC':'BitCoin'}
        

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(host=self.host,
                                                 user=self.username,
                                                 password=self.password,
                                                 database=self.db)
        except(e):
            raise e
        else:
            print("Connection Successfull")
            return connection
        
    def get_last_date_entry(self,cursor,no_of_days):
        query = """SELECT dates FROM  """ + self.cryptos[self.stock] + """  ORDER BY dates DESC LIMIT 1;"""
        cursor.execute(query)
        output = cursor.fetchall()
        next_dates = []
        for i in range(no_of_days):
            next_dates.append((output[0][0] + timedelta(days=i)).strftime('%Y-%m-%d'))
        return next_dates, output[0][0].strftime('%Y-%m-%d')
    
    def get_data(self,cursor):
        query = """SELECT * FROM """+self.cryptos[self.stock]+""";"""
        print('\nQuery executed')
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data,columns=['Date','Open','High','Low','Close','Volume'])
        print(df.head())
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df.set_index('Date',inplace=True)
        return df['Close']
    
    def create_model(self, no_of_days):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        next_dates, last_date = self.get_last_date_entry(cursor,no_of_days)
        print(next_dates)
        train_data = self.get_data(cursor)
        dates = list(train_data.index)
        temp = list(train_data.values)
#         print(len(temp))
        train_data = list(train_data.values)
        x = int(len(temp) - (10*len(temp))/100)
        print(x)
        temp = temp[x:]
        dates = dates[x:]
#         print(test_data.columns)
#         print(test_data.head(3))
        print("Training...")
        predictions = []
        print(type(train_data))
        for i in range(no_of_days):
            model = ARIMA(train_data, order=(10,0,0))
            model_fit = model.fit()   
            pred = model_fit.forecast(1)
            print(pred)
            predictions.append(pred[0])
            train_data.append(pred[0])
#         predictions_df = pd.DataFrame({'Close':predictions})
#         print(test_data)
#         print(predictions_df)
#         err = mean_absolute_percentage_error(test_data.values,predictions_df['Close'])
        train_data = train_data[x:]
        print("Predictions",predictions)
#        predictions = list(predictions.values)
#        print("Predictions",type(predictions))
#        output = " ".join([str(i) for i in predictions])
#        dates = list(training_data.index)
#        x = training_data.shape[0] - 100
#        train_dates = dates[x:]

        for i in next_dates:
            dates.append(i)
#        values = list(training_data.values)
#        train_values = values[x:]
##        test_values = values[x:]
#        for i in predictions:
#            test_values.append(round(i))
#        print(dates, values)
      
        
        
        return (dates, temp, train_data)
# 
#obj = Get_Predictions('BTC')
##obj.create_model(3)
#print(obj.create_model(3))


