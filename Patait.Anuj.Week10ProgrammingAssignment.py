"""
        Author:         Anuj Patait
        Subject:        ICT 4370 - Python Programming
        Date Created:   08/09/2020
        Functionality:  The goal of this program is to calcuate the earnings and
                        loss of each share the investor owns. This program 
                        will also show which share has made the most earning 
                        and which share has suffered the biggest loss. 
                        This program will use the default values for the 
                        calculations. 
                        This program will take default input from the csv file
                        and stores it in database. Then It will read all the data
                        from the database and print file output on screen 
                        as well as on the file.
                        This program will also plot the graph of the change in
                        stock value as per the purchase dates.                                              
"""
#importing functions from modules
from stock_resources_week10 import Bond, Investor, Stock
from stock_util_week10 import print_bonds_output_screen,print_stock_output_screen
from stock_util_week10 import print_bond_file, print_stock_file,draw_stock_progress_graph,stock_describe
import pandas_datareader as pdr
from yahoofinancials import YahooFinancials
import csv, os
import sqlite3
from datetime import datetime
import json
import sys
import matplotlib.pyplot as plt



def main():
    """
        This is the main function. This will be the first 
        function which will be called.
    """
    #setting input variable
    flag = True
    #Creating the database tables
    drop_and_create_tables()
    create_investor_db()
    write_stocks_file_db('Lesson10_Data_Stocks.csv')
    write_bonds_file_db('Lesson10_Data_Bonds.csv')

    #Reading user choice on fixed or real time feed.
    screen_read = input("Do you want to use realtime feeds? Yes or No: ")
    # Updating manual user input flags according to the user response
    flag = screen_read.lower() == "yes"
    
    if flag:
        
        while True:
            try :
                input_start_date = input("Enter the Start Date in (YYY-MM-DD format): ")
                start_date_obj = datetime.strptime(input_start_date, '%Y-%m-%d')
            except :
                print('Date is not in correct format (YYY-MM-DD). Please retry')
            else:
                break
        while True:
            try :
                input_end_date = input("Enter the End Date in (YYY-MM-DD format): ")
                end_end_obj = datetime.strptime(input_end_date, '%Y-%m-%d')
            except :
                print('Date is not in correct format (YYY-MM-DD). Please retry')
            else:
                break
        
        #Getting real time data
        real_time_Stock_json = download_real_time_data(start_date='2019-08-18', end_date='2020-08-20')
        #reading the stock progress from JSON and writing it to DB.
        write_stocks_progress_db(real_time_Stock_json, 'JSON')
    else:
        #reading the stock progress from JSON and writing it to DB.
        write_stocks_progress_db('AllStocks_week10.json','FILE')
    
    #setting default investor
    default_investor = set_user_data_from_db()

    #Checking if data is created correctly
    if default_investor is None :
        print("Exiting the program because of the data error.")
        return None

    #Calculations
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()

        #query to update investor calculations
        query_investor_update = '''
        UPDATE INVESTOR
        SET HIGHEST_EARNING_STOCK = ?, HIGHEST_LOSS_STOCK = ?,
        HIGHEST_EARNING_BOND = ?, HIGHEST_LOSS_BOND = ?
        WHERE INVESTOR_ID = ?
        '''

        if(default_investor.stocks is not None ):
            default_investor.find_highest_lowest_stock()
        if(default_investor.bonds is not None ):
            default_investor.find_hisghes_lowest_bond()
        #Updating database
        cursor.execute(query_investor_update,(default_investor.highest_earning,default_investor.highest_loss, \
                        default_investor.highest_earning_bond,default_investor.highest_loss_bond,\
                            default_investor.investor_id))
        conn.commit()


    except Exception as unwanted_exception:
        print(unwanted_exception)
        conn.close()
    else :
        conn.close()

    #creating investors dictionary to support multiple users
    investors = {}
    investors[default_investor.investor_id] = default_investor

    # Set up Output on Screen.
    
    if(default_investor.stocks is not None ):
        print_stock_output_screen(investors)
    if(default_investor.bonds is not None ):
        print_bonds_output_screen(investors)

    #Print output to file
    output_file_name = 'investor_details.txt'
    #Removing the old output file only if file exist.
    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    #Printing output to the same file.
    if(default_investor.stocks is not None ):
        print_stock_file(investors,output_file_name)
    if(default_investor.bonds is not None ):
        print_bond_file(investors,output_file_name)
    
    #plot the graph
    draw_stock_progress_graph(investors)
    #draw_stock_progress_graph_new(investors)
    #draw_stock_progress_graph_pygal(investors)
    stock_describe(investors)

def download_real_time_data(start_date,end_date):
    '''
    This function will download the real time daaily stock data for the given date range.
    '''
    #list of stocks that we want to follow.
    tickers = ['GOOG','MSFT','RDS-A','AIG','FB','M','F','IBM']
    #Below call will pull the realtime data for the given tickers.
    yahoo_financials_stocks = YahooFinancials(tickers)
    #This call will pull the historical price data for the given stocks 
    real_time_stocks = yahoo_financials_stocks.get_historical_price_data(start_date, end_date, 'daily')
  
    real_stock_records = []
    for ticker in tickers:
        #Converting the YahooFinancials object into Dict.
        stock_prices = real_time_stocks[ticker]['prices']
        for stock_price in stock_prices:
            real_record = {}
            real_record['Symbol'] = ticker
            formatted_date = datetime.strptime(stock_price['formatted_date'], '%Y-%m-%d').date()
            real_record['Date'] = str(formatted_date.strftime('%d-%b-%y'))
            real_record['High'] = round(stock_price['high'],2)
            real_record['Open'] = round(stock_price['open'],2)
            real_record['Close'] = round(stock_price['close'],2)
            real_record['Low'] = round(stock_price['low'],2)
            real_record['Volume'] = stock_price['volume']
            #Appending stock record to the overall list.
            real_stock_records.append(real_record)
    #Converting List to JSON.
    real_stock_records_json = json.dumps(real_stock_records)
    #print(real_stock_records_json)
    return real_stock_records_json
    
def set_user_data_from_db():
    '''
    This function will read the data from the files and write it into the 
    SQLite database.
    '''
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()

        #Read Investor, stock and Bond data to create Stock and Bond object
        
        #creating stocks array
        query_get_stocks = '''
        select  STOCK_ID, SYMBOL,
                QUANTITY, PURCHASE_PRICE, CURRENT_VALUE,
                PURCHASE_DATE
        from STOCK
        where INVESTOR_ID = 01
        '''
        query_update_stock =  '''
        UPDATE STOCK
        SET EARNING_LOSS_VAL = ?, YEARLY_CHANGE = ?, IS_EARNING = ?
        WHERE STOCK_ID = ?
        '''
        query_get_stock_progress = '''
        select PROGRESS_DATE, OPEN, HIGH, LOW, CLOSE, VOLUME, STOCK_ID 
        from STOCK_PROGRESS
        where STOCK_ID = ?
        '''
        cursor.execute(query_get_stocks)
        stocks_data = cursor.fetchall()
        stocks = []
        for stock_val in stocks_data:
            #Creating Stock object from the database
            stock = Stock(stock_val[0],stock_val[1],stock_val[2],stock_val[3],stock_val[4],stock_val[5])
            #Performing calculations on the stock
            stock.calculate_loss_or_gain()
            stock.calculate_percentage_change()
            #Updating DB with stock calculations.
            cursor.execute(query_update_stock,(stock.earning_or_loss,stock.yearly_percent_change, \
                            stock.is_earning,stock.purchase_id))
            conn.commit()
            #storing stock progress
            cursor.execute(query_get_stock_progress,(stock_val[0],))
            stock_progress_rows = cursor.fetchall()
            #Stock progress list for each stock
            all_stock_progress = []
            for stock_progress_row in stock_progress_rows:
                daily_stock_progress = {}
                #Converting to the data object before storing it to the dict
                daily_stock_progress['Date'] = datetime.strptime(stock_progress_row[0], '%Y-%m-%d').date()
                daily_stock_progress['Open'] = stock_progress_row[1] 
                daily_stock_progress['High'] = stock_progress_row[2]
                daily_stock_progress['Low'] = stock_progress_row[3]   
                daily_stock_progress['Close'] = stock_progress_row[4]
                daily_stock_progress['Volume'] = stock_progress_row[5]
                all_stock_progress.append(daily_stock_progress)

            #stetting the stock progress details  
            stock.stock_progress = all_stock_progress
            #calculating the close value for plotting the graph
            stock.calculate_close_value()
            #print('for Stock id',stock.purchase_id,'progress is ',stock.stock_progress)
            #Appending stock to stocks array.
            stocks.append(stock)
        
        #Creating bonds array
        query_get_bonds = '''
        select  BOND_ID, SYMBOL,
                QUANTITY, PURCHASE_PRICE, CURRENT_VALUE,
                PURCHASE_DATE, COUPON, YIELD_PERCENTAGE
        from BOND
        where INVESTOR_ID = 01
        '''
        query_update_bonds =  '''
        UPDATE BOND
        SET EARNING_LOSS_VAL = ?, YEARLY_CHANGE = ?, IS_EARNING = ?
        WHERE BOND_ID = ?
        '''
        cursor.execute(query_get_bonds)
        bonds_data = cursor.fetchall()
        bonds = []
        for bond_val in bonds_data:
            bond = Bond(bond_val[0],bond_val[1],bond_val[2],bond_val[3],bond_val[4],bond_val[5],bond_val[6],bond_val[7])
            bond.calculate_loss_or_gain()
            bond.calculate_percentage_change()
            #Updating DB with bond calculations.
            cursor.execute(query_update_bonds,(bond.earning_or_loss,bond.yearly_percent_change,\
                         bond.is_earning,bond.purchase_id))
            conn.commit()
            #Appending stock to stocks array.
            bonds.append(bond)
        #fetching investor data from Db
        query_get_investor = '''
                select INVESTOR_ID, INVESTOR_NAME, INVESTOR_ADDRESS,
                INVESTOR_PHONE_NUMBER 
                from INVESTOR
                where INVESTOR_ID = 01
        '''
        cursor.execute(query_get_investor)
        row = cursor.fetchone()
        #creating investor object
        investor = Investor(row[0], row[1], row[2], row[3], stocks, bonds)

    except Exception as unwanted_exception:
        print(unwanted_exception)
        conn.close()
        return None
    else :
        conn.close()

    return investor
    

def drop_and_create_tables():
    '''
    This function will tables. If tables exist it will drop and create new.
    '''
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()

        #Drop the existing tables
        conn.execute("DROP TABLE IF EXISTS INVESTOR")
        conn.execute("DROP TABLE IF EXISTS STOCK")
        conn.execute("DROP TABLE IF EXISTS BOND")
        conn.execute("DROP TABLE IF EXISTS STOCK_PROGRESS")

        #Creating Investor, Stock, and Bond tables
        sql_create_investor = ''' 
                    CREATE TABLE INVESTOR (INVESTOR_ID INTEGER PRIMARY KEY, 
                    INVESTOR_NAME VARCHAR(20), INVESTOR_ADDRESS VARCHAR(250),
                    INVESTOR_PHONE_NUMBER VARCHAR(12),
                    HIGHEST_EARNING_STOCK VARCHAR(30), 
                    HIGHEST_LOSS_STOCK VARCHAR(30), 
                    HIGHEST_EARNING_BOND VARCHAR(30), 
                    HIGHEST_LOSS_BOND VARCHAR(30)
                    )
        '''

        cursor.execute(sql_create_investor)

        sql_create_stock = ''' 
                    CREATE TABLE STOCK (STOCK_ID INTEGER PRIMARY KEY,
                    SYMBOL VARCHAR(10), QUANTITY INTEGER, 
                    PURCHASE_PRICE REAL, CURRENT_VALUE REAL,
                    PURCHASE_DATE DATE, YEARLY_CHANGE REAL,
                    EARNING_LOSS_VAL REAL, IS_EARNING VARCHAR(1),
                    INVESTOR_ID INTEGER,
                    FOREIGN KEY (INVESTOR_ID) REFERENCES INVESTOR(INVESTOR_ID)
                    )
        '''
        cursor.execute(sql_create_stock)

        sql_create_bond = '''
                    CREATE TABLE BOND (BOND_ID INTEGER PRIMARY KEY,
                    SYMBOL VARCHAR(10), QUANTITY INTEGER, 
                    PURCHASE_PRICE REAL, CURRENT_VALUE REAL,
                    PURCHASE_DATE DATE, YEARLY_CHANGE DREAL,
                    EARNING_LOSS_VAL REAL, IS_EARNING VARCHAR(1),
                    COUPON REAL, YIELD_PERCENTAGE REAL,
                    INVESTOR_ID INTEGER,
                    FOREIGN KEY (INVESTOR_ID) REFERENCES INVESTOR(INVESTOR_ID)
                    )
        '''
        cursor.execute(sql_create_bond)

        sql_create_stock_progress = '''
                    CREATE TABLE STOCK_PROGRESS (
                    PROGRESS_DATE DATE, OPEN REAL, HIGH REAL, LOW REAL,CLOSE REAL,
                    VOLUME INTEGER, STOCK_ID INTEGER,
                    FOREIGN KEY (STOCK_ID) REFERENCES STOCK(STOCK_ID)
                    )
        '''
        cursor.execute(sql_create_stock_progress)

        conn.commit()
        
    except Exception as unwanted_exception:
        print(unwanted_exception)
        conn.close()
        return None
    else :
        conn.close()

def write_stocks_file_db(file_name):
    '''
    This function will read the csv file and write to the database
    '''
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()

        with open(file_name,'r') as stock_data:
            #parsing the file content
            content = csv.reader(stock_data,delimiter=',')
            #featching the header row
            header = next(content, None)
            index_symbol = header.index('SYMBOL')
            index_number_shares = header.index('NO_SHARES')
            index_purchase_price = header.index('PURCHASE_PRICE')
            index_current_value = header.index('CURRENT_VALUE')
            index_purchase_date = header.index('PURCHASE_DATE')
            
            #StockId Counter
            stock_id = 1
            #Iterating rest of the file
            for row in content:
                symbol = str(row[index_symbol])
                try:
                    quantity = int(row[index_number_shares])
                except Exception:
                    print('The value for quantity is not integer. Exiting the stock processing')
                    return None
                try:
                    purchase_price = float(row[index_purchase_price])
                except Exception:
                    print('Purchase price is not float. Exiting the stock processing')
                    return None
                try:
                    current_value = float(row[index_current_value])
                except Exception:
                    print('Current Value is not float. Exiting the stock processing')
                    return None
                try :
                        purchase_date = row[index_purchase_date]
                        purchase_date_obj = datetime.strptime(purchase_date, '%m/%d/%Y')
                except :
                        print('Date is not in correct format (m/dd/YYYY). Exiting the stock processing')
                        return None

                query_insert_stock = '''
                                INSERT INTO STOCK(STOCK_ID, SYMBOL,
                                QUANTITY, PURCHASE_PRICE, CURRENT_VALUE,
                                PURCHASE_DATE, INVESTOR_ID)
                                VALUES(?,?,?,?,?,?,?)
                            '''
                cursor.execute(query_insert_stock,\
                    (stock_id,symbol,quantity,purchase_price,current_value,purchase_date,'01'))
                conn.commit()
                #Incrementing stock id
                stock_id = stock_id +1
   

    except FileNotFoundError as not_found_exception:
        print(file_name,'is not present in the current directory')
        print(not_found_exception)
        conn.close()
        return None
    except IndexError as index_exception:
        print(file_name,'has incorrect data format')
        print(index_exception)
        conn.close()
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)
        conn.close()
        return None
    else:
        conn.close()

def write_bonds_file_db(file_name):
    '''
    This function will read the csv file and write to the database
    '''
    try: 
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()

        with open(file_name,'r') as bonds_data:
            #parsing the file content
            content = csv.reader(bonds_data,delimiter=',')
            #featching the header row
            header = next(content, None)
            index_symbol = header.index('SYMBOL')
            index_quantity = header.index('NO_SHARES')
            index_purchase_price = header.index('PURCHASE_PRICE')
            index_current_value = header.index('CURRENT_VALUE')
            index_purchase_date = header.index('PURCHASE_DATE')
            index_coupon = header.index('Coupon')
            index_yield = header.index('Yield')
            
            #BondId Counter
            bond_id = 1
            #Iterating rest of the file
            for row in content:
                symbol = str(row[index_symbol])
                try:
                    quantity = int(row[index_quantity])
                except Exception:
                    print('The value for quantity is not integer. Exiting the bond processing')
                    return None
                try:
                    purchase_price = float(row[index_purchase_price])
                except Exception:
                    print('Purchase price is not float. Exiting the bond processing')
                    return None
                try:
                    current_value = float(row[index_current_value])
                except Exception:
                    print('Current Value is not float. Exiting the bond processing')
                    return None
                try :
                        purchase_date = row[index_purchase_date]
                        purchase_date_obj = datetime.strptime(purchase_date, '%m/%d/%Y')
                except :
                        print('Date is not in correct format (m/dd/YYYY). Exiting the bond processing')
                        return None
                try:
                    coupon = float(row[index_coupon])
                except Exception:
                    print('Coupon is not float. Exiting the bond processing')
                    return None
                try:
                    yield_percentage = float(row[index_yield])
                except Exception:
                    print('Yield is not float. Exiting the bond processing')
                    return None

                query_insert_bond = '''
                                INSERT INTO BOND(BOND_ID, SYMBOL,
                                QUANTITY, PURCHASE_PRICE,
                                CURRENT_VALUE,PURCHASE_DATE,
                                COUPON, YIELD_PERCENTAGE, INVESTOR_ID)
                                VALUES(?,?,?,?,?,?,?,?,?)
                            '''
                cursor.execute(query_insert_bond,\
                    (bond_id,symbol,quantity,purchase_price,current_value,purchase_date,coupon,yield_percentage,'01'))
                conn.commit()

                #Incrementing bond id
                bond_id = bond_id +1

    except FileNotFoundError as not_found_exception:
        print(file_name,'is not present in the current directory')
        print(not_found_exception)
        conn.close()
        return None
    except IndexError as index_exception:
        print(file_name,'has incorrect data format')
        print(index_exception)
        conn.close()
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)
        conn.close()
        return None
    else:
        conn.close()

def write_stocks_progress_db(source_all_stock_progress_json,source):
    '''
    This function will read the JSON file containing the stock progress and 
    will insert the data into the STOCK_PROGRESS table.
    '''
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')
        #creating cursor
        cursor = conn.cursor()

        #find stock_id query
        find_stock_id = '''
                        SELECT STOCK_ID FROM STOCK WHERE SYMBOL = ?
        '''
        #query to insert stock progress
        insert_stock_progress = '''
                                INSERT INTO STOCK_PROGRESS (PROGRESS_DATE,
                                OPEN, HIGH, LOW, CLOSE, VOLUME, STOCK_ID)
                                VALUES(?,?,?,?,?,?,?)
         '''
        if source.lower() == 'file':
            #Reading the Json file
            with open(source_all_stock_progress_json, 'r') as all_stock_progress_json:
                    all_stock_progress = json.load(all_stock_progress_json)
        else:
            all_stock_progress = json.loads(source_all_stock_progress_json)
        
        for stock_progress in all_stock_progress:
            #adding ',' to make it a tuple
            query_args = (stock_progress['Symbol'],)
            cursor.execute(find_stock_id,query_args)
            stock_record = cursor.fetchone()
            stock_id = stock_record[0]

            try:
                progress_date = stock_progress['Date']
                progress_date_obj = datetime.strptime(progress_date, '%d-%b-%y').date()
            except Exception as e:
                print(e)
                print('Date is not in correct format (d-MON-YY). Exiting the stock processing')
                return None
            
            try:
                if (stock_progress['Open'] == '-') :
                    open_price = 0.0
                else:
                    open_price = float(stock_progress['Open'])
            except Exception:
                print(stock_progress['Open'], 'for symbol',stock_progress['Symbol'])
                print('Open price is not float. Exiting the stock processing')
                return None
            try:
                if (stock_progress['High'] == '-') :
                    high_price = 0.0
                else:
                    high_price = float(stock_progress['High'])
            except Exception:
                print('high price is not float. Exiting the stock processing')
                return None
            try:
                if (stock_progress['Low'] == '-') :
                    low_price = 0.0
                else:
                    low_price = float(stock_progress['Low'])
            except Exception:
                print('Low price is not float. Exiting the stock processing')
                return None
            try:
                close_price = float(stock_progress['Close'])
            except Exception:
                print('Close price is not float. Exiting the stock processing')
                return None
            try:
                volume = int(stock_progress['Volume'])
            except Exception:
                print('The value for volume is not integer. Exiting the stock processing')
                return None
            
            #Inserting the stock progress into the database
            cursor.execute(insert_stock_progress,\
                    (progress_date_obj,open_price,high_price,low_price,close_price,volume,stock_id))
            conn.commit()

    except FileNotFoundError:
        print(source_all_stock_progress_json,'is not present in the current directory')
        #stopping the further process
        return None
    except Exception as e:
        #Print the line number of the exception
        print('unknown exception at ',e,sys.exc_info()[-1].tb_lineno)
        conn.close()
        #stopping the further process
        return None 
    else :
        conn.close()


def create_investor_db():
    '''
    This function will create an investor entry in DB
    '''
    try:
        #connecting to the database
        conn = sqlite3.connect('investors.db')

        #creating cursor
        cursor = conn.cursor()
        query_insert_investor = '''
                                INSERT INTO INVESTOR(INVESTOR_ID, INVESTOR_NAME,
                                INVESTOR_ADDRESS,INVESTOR_PHONE_NUMBER)
                                VALUES(01,'Bob Smith','Hello St, CO-80134', '303-000-1111')
        '''
        cursor.execute(query_insert_investor)
        conn.commit()
       

    except Exception as unwanted_exception:
        print(unwanted_exception)
        conn.close()
    else :
        conn.close()


@DeprecationWarning
def set_user_data_from_csv():
    '''
        This function will create a default data for the investors using the
        csv files. 
        This function is now deprecated. We are using the DB version of this 
        functionality.
    '''
    #initalizing variables
    stocks_data_file = "Lesson6_Data_Stocks.csv"
    bonds_data_file = "Lesson6_Data_Bonds.csv"
    #Reading the file containing the stock information
    stocks = read_stocks_file(stocks_data_file)
    bonds = read_bonds_file(bonds_data_file)

    if(stocks == None and bonds == None) :
        print("Both Stock and Bond details are not present")
        return None
    
    #Creating instance of the Investor class
    investor = Investor(1, 'Bob Smith', '', '303-000-1111', stocks, bonds)

    return investor



def read_stocks_file(file_name):
    '''
    This function reads csv file and create the stock data using Stock class.
    This function will store all the stock object in a list and will return 
    that list after creating instance of all stocks.
    '''
    stocks = []
    try: 
        with open(file_name,'r') as stock_data:
            #parsing the file content
            content = csv.reader(stock_data,delimiter=',')
            #featching the header row
            header = next(content, None)
            index_symbol = header.index('SYMBOL')
            index_number_shares = header.index('NO_SHARES')
            index_purchase_price = header.index('PURCHASE_PRICE')
            index_current_value = header.index('CURRENT_VALUE')
            index_purchase_date = header.index('PURCHASE_DATE')
            
            #StockId Counter
            stock_id = 1
            #Iterating rest of the file
            for row in content:
                symbol = str(row[index_symbol])
                try:
                    quantity = int(row[index_number_shares])
                except Exception:
                    print('The value for quantity is not integer. Exiting the stock processing')
                    return None
                try:
                    purchase_price = float(row[index_purchase_price])
                except Exception:
                    print('Purchase price is not float. Exiting the stock processing')
                    return None
                try:
                    current_value = float(row[index_current_value])
                except Exception:
                    print('Current Value is not float. Exiting the stock processing')
                    return None
                try :
                        purchase_date = row[index_purchase_date]
                        purchase_date_obj = datetime.strptime(purchase_date, '%m/%d/%Y')
                except :
                        print('Date is not in correct format (m/dd/YYYY). Exiting the stock processing')
                        return None

                stock = Stock(stock_id,symbol,quantity,purchase_price,current_value,purchase_date)
                stock.calculate_loss_or_gain()
                stock.calculate_percentage_change()
                stocks.append(stock)
                #Incrementing stock id
                stock_id = stock_id +1

    except FileNotFoundError as not_found_exception:
        print(file_name,'is not present in the current directory')
        print(not_found_exception)
        return None
    except IndexError as index_exception:
        print(file_name,'has incorrect data format')
        print(index_exception)
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)

    return stocks

def read_bonds_file(file_name):
    '''
    This function reads csv file and create the bond data using Bond class.
    This function will store all the bond object in a list and will return 
    that list after creating instance of all bonds.
    '''
    bonds = []
    try: 
        with open(file_name,'r') as bonds_data:
            #parsing the file content
            content = csv.reader(bonds_data,delimiter=',')
            #featching the header row
            header = next(content, None)
            index_symbol = header.index('SYMBOL')
            index_quantity = header.index('NO_SHARES')
            index_purchase_price = header.index('PURCHASE_PRICE')
            index_current_value = header.index('CURRENT_VALUE')
            index_purchase_date = header.index('PURCHASE_DATE')
            index_coupon = header.index('Coupon')
            index_yield = header.index('Yield')
            
            #BondId Counter
            bond_id = 1
            #Iterating rest of the file
            for row in content:
                symbol = str(row[index_symbol])
                try:
                    quantity = int(row[index_quantity])
                except Exception:
                    print('The value for quantity is not integer. Exiting the bond processing')
                    return None
                try:
                    purchase_price = float(row[index_purchase_price])
                except Exception:
                    print('Purchase price is not float. Exiting the bond processing')
                    return None
                try:
                    current_value = float(row[index_current_value])
                except Exception:
                    print('Current Value is not float. Exiting the bond processing')
                    return None
                try :
                        purchase_date = row[index_purchase_date]
                        purchase_date_obj = datetime.strptime(purchase_date, '%m/%d/%Y')
                except :
                        print('Date is not in correct format (m/dd/YYYY). Exiting the bond processing')
                        return None
                try:
                    coupon = float(row[index_coupon])
                except Exception:
                    print('Coupon is not float. Exiting the bond processing')
                    return None
                try:
                    yield_percentage = float(row[index_yield])
                except Exception:
                    print('Yield is not float. Exiting the bond processing')
                    return None

                bond = Bond(bond_id,symbol,quantity,purchase_price,current_value,purchase_date,coupon,yield_percentage)
                bond.calculate_loss_or_gain()
                bond.calculate_percentage_change()
                bonds.append(bond)
                #Incrementing bond id
                bond_id = bond_id +1

    except FileNotFoundError as not_found_exception:
        print(file_name,'is not present in the current directory')
        print(not_found_exception)
        return None
    except IndexError as index_exception:
        print(file_name,'has incorrect data format')
        print(index_exception)
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)
        return None

    return bonds

# From here the acutal flow will start.
if __name__ == "__main__":
        main()
