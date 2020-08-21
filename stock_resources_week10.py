"""
        Author:         Anuj Patait
        Subject:        ICT 4370 - Python Programming
        Date Created:   08/09/2020
        Functionality:  This module define all the classes related to stock
                        management. This module include Investor, Stock, and 
                        Bond class.                                               
"""
#importing functions from modules
from datetime import datetime

class Investor:
    '''
    The Investor class manages the investor details like its id, name, addres,
    phone number, stock information, and bonds information.
    '''
    def __init__(self, p_investor_id, p_investor_name, p_user_address, p_phone_number, p_stocks = [], p_bonds = [], \
                    p_highest_earning ='', p_highest_loss= '',p_highest_earning_bond = '', p_highest_loss_bond = ''):
        '''
        This is the constructor for the Investor class.
        '''
        self._investor_id = p_investor_id
        self._investor_name = p_investor_name
        self._user_address = p_user_address
        self._phone_number = p_phone_number
        self._stocks = p_stocks
        self._bonds = p_bonds
        self._highest_earning = p_highest_earning
        self._highest_loss = p_highest_loss
        self._highest_earning_bond = p_highest_earning_bond
        self._highest_loss_bond = p_highest_loss_bond
    '''
    All the methods defined below are getter and setter methods for the class 
    data members.
    '''
    @property
    def investor_id (self):
        return self._investor_id

    @investor_id.setter
    def investor_id(self,p_investor_id):
        self._investor_id = p_investor_id

    @property
    def investor_name (self):
        return self._investor_name

    @investor_name.setter
    def investor_name(self,p_investor_name):
        self._investor_name = p_investor_name

    @property
    def user_address (self):
        return self._user_address
    
    @user_address.setter
    def user_address(self,p_user_address):
        self._user_address = p_user_address

    @property
    def phone_number (self):
        return self._phone_number
    
    @phone_number.setter
    def phone_number(self,p_phone_number):
        self._phone_number = p_phone_number
    
    @property
    def stocks(self):
        return self._stocks
    
    @stocks.setter
    def stocks(self,p_stocks):
        self._stocks = p_stocks

    @property
    def bonds(self):
        return self._bonds
    
    @bonds.setter
    def bonds(self,p_bonds):
        self._bonds = p_bonds
    
    @property
    def highest_earning(self):
        return self._highest_earning

    @highest_earning.setter
    def highest_earning(self,p_highest_earning):
        self._highest_earning = p_highest_earning
    
    @property
    def highest_loss(self):
        return self._highest_loss
    
    @highest_loss.setter
    def highest_loss(self,p_highest_loss):
        self._highest_loss = p_highest_loss
    
    @property
    def highest_earning_bond(self):
        return self._highest_earning_bond
    
    @highest_earning_bond.setter
    def highest_earning_bond(self,p_highest_earning_bond):
        self._highest_earning_bond = p_highest_earning_bond
    
    @property
    def highest_loss_bond(self):
        return self._highest_loss_bond

    @highest_loss_bond.setter
    def highest_loss_bond(self,p_highest_loss_bond):
        self._highest_loss_bond = p_highest_loss_bond
    
    def find_highest_lowest_stock(self) :
        '''
        This method identify the highest earning and loss stock for the investor.
        '''
        # Calculating hishest earning and highest loss for each user
        earnings_stock = list(filter(lambda stock:stock.is_earning == True, self._stocks))
        loss_stock = list(filter(lambda stock:stock.is_earning == False, self._stocks))
     
        if len(earnings_stock) > 0:
            highest_earning = max(earnings_stock, key= lambda stock:stock.earning_or_loss)
            self._highest_earning= highest_earning.symbol

        if len(loss_stock) > 0:
            highest_loss = min(loss_stock, key= lambda stock:stock.earning_or_loss)
            self._highest_loss = highest_loss.symbol
    
    def find_hisghes_lowest_bond(self) :
        '''
        This method calculate the loss and gain of each bond for the user.
        This method takes bond details of the investor and perform calculations
        on the investor object.
        '''
        # Calculating hishest earning and highest loss for each user
        earnings_bond = list(filter(lambda bond:bond.is_earning == True, self._bonds))
        loss_bond = list(filter(lambda bond:bond.is_earning == False, self._bonds))
     
        if len(earnings_bond) > 0:
            highest_earning = max(earnings_bond, key= lambda bond:bond.earning_or_loss)
            self._highest_earning_bond = highest_earning.symbol

        if len(loss_bond) > 0:
            highest_loss = min(loss_bond, key= lambda bond:bond.earning_or_loss)
            self._highest_loss_bond = highest_loss.symbol

class Stock:
    '''
    The Stock class manages the stock details like its id, symbol, quantity,
    purchase price, current value, purchase date, yearly percent change, and
    earning or loss details.
    We will use this class to manage investors stock information.
    '''
    def __init__(self,p_purchase_id,p_symbol,p_quantity,p_purchase_price,p_current_value,p_purchase_date, \
                    p_yearly_percent_change = 0.0, p_earning_or_loss = 0.0, p_is_earning = True, p_stock_progress =[]):
        '''
        This is the constructor for the Stock class.
        '''
        self._purchase_id = p_purchase_id
        self._symbol = p_symbol
        self._quantity = p_quantity
        self._purchase_price = p_purchase_price
        self._current_value = p_current_value
        self._purchase_date = p_purchase_date
        self._earning_or_loss = p_earning_or_loss
        self._is_earning = p_is_earning
        self._yearly_percent_change = p_yearly_percent_change
        self._stock_progress = p_stock_progress
    
    '''
    All the methods defined below are getter and setter methods for the class 
    data members.
    '''
    @property
    def purchase_id(self) :
        return self._purchase_id
    
    @purchase_id.setter
    def purchase_id(self, p_purchase_id):
        self._purchase_id = p_purchase_id
    
    @property
    def symbol(self) :
        return self._symbol
    
    @symbol.setter
    def symbol(self, p_symbol):
        self._symbol = p_symbol
    
    @property
    def quantity(self) :
        return self._quantity
    
    @quantity.setter
    def quantity(self, p_quantity):
        self._quantity = p_quantity

    @property
    def purchase_price(self) :
        return self._purchase_price
    
    @purchase_price.setter
    def purchase_price(self, p_purchase_price):
        self._purchase_price = p_purchase_price

    @property
    def current_value(self) :
        return self._current_value
    
    @current_value.setter
    def current_value(self, p_current_value):
        self._current_value = p_current_value
    
    @property
    def purchase_date(self) :
        return self._purchase_date
    
    @purchase_date.setter
    def purchase_date(self, p_purchase_date):
        self._purchase_date = p_purchase_date
    
    @property
    def earning_or_loss(self) :
        return self._earning_or_loss
    
    @earning_or_loss.setter
    def earning_or_loss(self, p_earning_or_loss):
        self._earning_or_loss = p_earning_or_loss
    
    @property
    def is_earning(self) :
        return self._is_earning
    
    @is_earning.setter
    def is_earning(self, p_is_earning):
        self._is_earning = p_is_earning

    @property
    def yearly_percent_change(self) :
        return self._yearly_percent_change
    
    @yearly_percent_change.setter
    def yearly_percent_change(self, p_yearly_percent_change):
        self._yearly_percent_change = p_yearly_percent_change

    @property
    def stock_progress(self) :
        return self._stock_progress
    
    @stock_progress.setter
    def stock_progress(self, p_stock_progress):
        self._stock_progress = p_stock_progress
    
    def calculate_loss_or_gain(self) :
        '''
        This function calculate the loss and gain of each stock using the stock
        details like purchase_price and quanity.
        '''
        total_purchase_cost = round((self._purchase_price * self._quantity) ,2)
        total_current_value = round((self._current_value * self._quantity) ,2)
        self._earning_or_loss = round((total_current_value - total_purchase_cost),2)

        # Setting up earning and loss value and flag according to the calculations.
        if(self._earning_or_loss < 0) :
            self._is_earning = False
        else :
            self._is_earning = True
    
    def calculate_percentage_change(self):
        '''
        This function calculate the percentage change of the stock. using the 
        stock details like purchase_date, current_date, current_value, and 
        purchase_price.
        '''
        purchase_date_obj = datetime.strptime(self._purchase_date, '%m/%d/%Y').date()
        current_date = datetime.now().date()
        date_diff = (current_date - purchase_date_obj).days
        date_diff_years = (current_date.year - purchase_date_obj.year)
        #if the purchase year and current year are same then set the year diff to 1.
        if(date_diff_years == 0) :
            date_diff_years = 1
         
        percent_change = ((self._current_value - self._purchase_price)/self._purchase_price)*100
        yearly_percent_change_abs = ((((self._current_value - self._purchase_price)/self._purchase_price))\
                                        /date_diff_years)*100
          
        self._yearly_percent_change = round(yearly_percent_change_abs,2)
    
    def calculate_close_value(self) :
        '''
        This method will caluclate the close value for each day the stock is
        evaluated.
        '''
        for stock_daily_progress in self._stock_progress:
            close_price = stock_daily_progress['Close']
            stock_close_value = round((close_price * self._quantity) ,2)
            stock_daily_progress['stock_close_value'] = stock_close_value


class Bond(Stock) :
    '''
        The Bond class manages the Bond details. This is the child class of 
        Stock. As a child class it can access all the variables of Stock class.
        This class has its additional class members like bond coupon and its 
        yield percentage. 
        We will use this class to manage investors bond information.
    '''
    def __init__(self, p_purchase_id, p_symbol, p_quantity, p_purchase_price, p_current_value, p_purchase_date, \
                    p_coupon, p_yield_percentage):
        '''
        This is the constructor for the Bond class. Using super.__init__() method
        we are initializing the parent (Stock) class.
        '''
        super().__init__(p_purchase_id, p_symbol, p_quantity, p_purchase_price, p_current_value, p_purchase_date)
        self._coupon = p_coupon
        self._yield_percentage = p_yield_percentage

    '''
    All the methods defined below are getter and setter methods for the class 
    data members.
    '''
    @property
    def coupon(self) :
        return self._coupon
    
    @coupon.setter
    def coupon(self, p_coupon):
        self._coupon = p_coupon

    @property
    def yield_percentage(self) :
        return self._yield_percentage
    
    @yield_percentage.setter
    def yield_percentage(self, p_yield_percentage):
        self._yield_percentage = p_yield_percentage