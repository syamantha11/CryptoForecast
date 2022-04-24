#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install mysql-connector-python


# In[32]:


import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import requests
import mysql.connector
#https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=INR&apikey=XJO4H17WI3PQFKI3

class Connect_Store_Data:
    def __init__(self,stock):
        self.stock = stock
        self.url = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol="+stock+"&market=INR&apikey=XJO4H17WI3PQFKI3"
        self.cryptos = {'BTC':'BitCoin'}
        self.host = "firstdatabase.csdx2ljymbci.ap-south-1.rds.amazonaws.com"
        self.port = "3306"
        self.db = "BitCoin_db"
        self.username = "admin"
        self.password = "Admin#123"
        
        
    def get_data(self):
        #Create a response variable and return the data in dataframe format
        response = requests.get(self.url).json()
#        print(response)
        data = response["Time Series (Digital Currency Daily)"]
        keys = list(data.keys())
        indexes = [i for i in range(len(list(data[keys[0]]))) if 'INR' in list(data[keys[0]])[i]]
        indexes.append(8)
        Open, High, Low, Close, Volume = ([], [], [], [], [])
        list_values = [Open, High, Low, Close, Volume]
        for i in range(len(keys)):
            values = list(data[keys[i]].values())
            for key,index in zip(list_values, indexes):
                key.append(values[index])
                
        df = pd.DataFrame({'Dates':keys,'Open':Open,'High':High,'Low':Low,'Close':Close,'Volume':Volume})
        return df
        
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
    
    def create_table(self,cursor):
        query = """CREATE TABLE IF NOT EXISTS """ + self.cryptos[self.stock] + """ (
                        Dates date PRIMARY KEY,
                        Open FLOAT,
                        High FLOAT,
                        Low FLOAT,
                        Close FLOAT,
                        Volume FLOAT
        )"""
        print(query)
        try:
            cursor.execute(query)
        except(e):
            raise e
        else:
            cursor.execute('SHOW TABLES')
            output = cursor.fetchall()
            print(output)
            
    def convert_df_into_table(self,cursor, df, last_date):
        for i, row in df.iterrows():
            self.insert_into_table(cursor=cursor, date=row['Dates'],open=row['Open'], high=row['High'], low=row['Low'], close=row['Close'], volume=row['Volume'], last_date=last_date)

    def insert_into_table(self,cursor=None, date=None, open=0, high=0, low=0, close=0, volume=0, last_date=None):
        if date == last_date:
            
            self.update_rows(cursor,date,open,high,low,close,volume)
        else:
            print('Inserting',date)
            query = """INSERT INTO  """ + self.cryptos[self.stock] + """  (Dates, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s);"""
            to_insert = (date,open,high,low,close,volume)
            cursor.execute(query, to_insert)

    def update_rows(self,cursor,date,open,high,low,close,volume):
        print('Updating',date)
        query = """UPDATE  """ + self.cryptos[self.stock] + """  SET Open = %s, High = %s, Low = %s, Close = %s, Volume = %s WHERE Dates = %s;"""
        to_update = (open,high,low,close,volume,date)
        cursor.execute(query,to_update)


    def get_last_date_entry(self,cursor):
        query = """SELECT dates FROM  """ + self.cryptos[self.stock] + """  ORDER BY dates DESC LIMIT 1;"""
        cursor.execute(query)
        output = cursor.fetchall()
        return output[0][0].strftime('%Y-%m-%d')
    
    def print_data(self, cursor):
        query = """select count(dates) from  """ + self.cryptos[self.stock] + """ ;"""
        cursor.execute(query)
        output = cursor.fetchall()
        print(output)

    def update_data(self):
        #Update the table of the stock and return successfull if it is done
        #get_data(), connecting to db, filtering dataframe, updating the table
        print('Getting the Data....')
        df = self.get_data()
        print('\nData Obtained',df.shape,'Setting up Connection....')
        conn = self.connect_to_db()
        cursor = conn.cursor()
        print('\nCreating Table....')
        self.create_table(cursor)
        
        last_date = self.get_last_date_entry(cursor)
        print('\nLast Date',last_date)
        df = df[df['Dates']>=last_date]
        print('\nFiltering the data',df.shape)
        print('\nInserting and Updating...')
        self.convert_df_into_table(cursor, df, last_date)
        conn.commit()
        print('\nThe Output....')
        self.print_data(cursor)
        
    
        
obj = Connect_Store_Data('BTC')
obj.update_data()        

