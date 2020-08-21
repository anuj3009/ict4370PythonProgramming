"""
        Author:         Anuj Patait
        Subject:        ICT 4370 - Python Programming
        Date Created:   08/09/2020
        Functionality:  This module provide the utility functions for 
                        calculating and managing the stock and details 
                        for multiple investors.                                               
"""
#importing functions from modules
from datetime import datetime
from stock_resources_week10 import Stock, Investor, Bond
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def print_stock_file(investors,output_file_name) :
    '''
        This function prints all stock details for all the investors on the file.
        This function also print highest incerease and max decrease stock 
        details. We will print all the information in the tabular format.
        The output file name would be investor_details.txt".
    '''
    try: 
        with open(output_file_name,'a') as output_file:
            for investor in investors.values() :
                output_file.write(("-"*72)+"\n")
                header = ("Stock ownership for "+ investor.investor_name)
                output_file.write("| ".ljust(21)+header+" |".rjust(21))
                output_file.write("\n"+("-"*72)+"\n")
                output_file.write("\n")
                output_file.write(f"|{'Stock':^13} | {'Share #':^13} | {'Earnings/Loss':^13} | "\
                                    f"{'Yearly Earnings/Loss':^13} |")
                output_file.write("\n"+("-"*72)+"\n")
                output_file.write("\n")
                stocks = investor.stocks
                for stock in stocks :
                    output_file.write(f"|{stock.symbol:^13} | {stock.quantity:^13}"+\
                            f" | {stock.earning_or_loss:^13} | {stock.yearly_percent_change:^20} |")
                    output_file.write("\n"+("-"*72)+"\n")
                    output_file.write("\n")
                #Printing the share with highest increase and max decrease
                if (investor.highest_earning):
                    output_file.write("\n"+("-"*90)+"\n")
                    output_file.write("The stock with the highest increase in value in your portfolio on"\
                                        " a per-share basis is: " +investor.highest_earning)
                    output_file.write("\n"+("-"*90)+"\n")
                if(investor.highest_loss):
                    output_file.write("\n"+("-"*90)+"\n")
                    output_file.write("The stock with max decrease in value in your portfolio on"\
                                        " a per-share basis is: " +investor.highest_loss)
                    output_file.write("\n"+("-"*90)+"\n")
            
    except FileNotFoundError as not_found_exception:
        print(output_file_name,'is not present in the current directory')
        print(not_found_exception)
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)
        return None

def print_bond_file(investors,output_file_name) :
    '''
        This function prints all bond details for all the investors on the file.
        This function also print highest incerease and max decrease bond 
        details. We will print all the information in the tabular format.
        The output file name would be "investor_details.txt".
    '''
    
    try: 
        with open(output_file_name,'a') as output_file:
            for investor in investors.values() :
                output_file.write(("-"*138)+"\n")
                header = ("Bond ownership for "+ investor.investor_name)
                output_file.write("| ".ljust(54)+header+" |".rjust(54))
                output_file.write("\n"+("-"*138)+"\n")
                output_file.write("\n")
                output_file.write(f"|{'Bonds':^13} | {'Quantity #':^13} | {'Purchase Price':^13} "+\
                                    f"| {'Current Value':^13} |{'Coupon':^13} | {'Yield %':^13} | "+\
                                        f"{'Earnings/Loss':^13} | {'Yearly Earnings/Loss %':^13} |" )
                output_file.write("\n"+("-"*138)+"\n")
                output_file.write("\n")
                bonds = investor.bonds
                for bond in bonds :
                    output_file.write(f"|{bond.symbol:^13} | {bond.quantity:^13}"+\
                                        f" | {bond.purchase_price:^13} | {bond.current_value:^13} "+\
                                        f" | {bond.coupon:^13} | {bond.yield_percentage:^13} "+\
                                        f" | {bond.earning_or_loss:^13} | {bond.yearly_percent_change:^20} |")
                    output_file.write("\n"+("-"*138)+"\n")
                    output_file.write("\n")
                #Printing the bond with highest increase and max decrease
                if (investor.highest_earning_bond):
                    output_file.write("\n"+("-"*90)+"\n")
                    output_file.write("The bond with the highest increase in value in your portfolio on"\
                                        " a per-bond basis is: " +investor.highest_earning_bond)
                    output_file.write("\n"+("-"*90)+"\n")
                if(investor.highest_loss_bond):
                    output_file.write("\n"+("-"*90)+"\n")
                    output_file.write("The bond with max decrease in value in your portfolio on"\
                                        " a per-bond basis is: " +investor.highest_loss_bond)
                    output_file.write("\n"+("-"*90)+"\n")
            
    except FileNotFoundError as not_found_exception:
        print(output_file_name,'is not present in the current directory')
        print(not_found_exception)
        return None
    except Exception as unknown_exception:
        print('Unkown error occur. Please try again')
        print(unknown_exception)
        return None


def print_stock_output_screen(investors) :
    '''
        This function prints all stock details for all the investors on the screen.
        This function also print highest incerease and max decrease stock 
        details. We will print all the information in the tabular format.
    '''
    for investor in investors.values() :
        print("------------------------------------------------------------------------")
        header = ("Stock ownership for "+ investor.investor_name)
        print("|".ljust(19),header, "|".rjust(21))
        print("------------------------------------------------------------------------")
        print()
        print(f"|{'Stock':^13} | {'Share #':^13} | {'Earnings/Loss':^13} | {'Yearly Earnings/Loss':^13} |")
        print("------------------------------------------------------------------------")
        print()
        stocks = investor.stocks
        for stock in stocks :
            print(f"|{stock.symbol:^13} | {stock.quantity:^13}"+\
            f" | {stock.earning_or_loss:^13} | {stock.yearly_percent_change:^20} |")
            print("------------------------------------------------------------------------")
            print()
        #Printing the share with highest increase and max decrease
        if (investor.highest_earning):
            print("-----------------------------------------------------------------------------------------")
            print("The stock with the highest increase in value in your portfolio on a per-share basis is:" \
                ,investor.highest_earning)
            print("-----------------------------------------------------------------------------------------")
        if(investor.highest_loss):
            print("-----------------------------------------------------------------------------------------")
            print("The stock with max decrease in value in your portfolio on a per-share basis is:" \
                ,investor.highest_loss)
            print("-----------------------------------------------------------------------------------------")


def print_bonds_output_screen(investors) :
    '''
        This function prints all bonds details for all the investors on the screen.

    '''
    for investor in investors.values() :
        print("-"*138)
        header = ("Bond ownership for "+ investor.investor_name)
        print("|".ljust(53),header, "|".rjust(55))
        print("-"*138)
        print()
        print(f"|{'Bonds':^13} | {'Quantity #':^13} | {'Purchase Price':^13} | {'Current Value':^13} "+\
                f"|{'Coupon':^13} | {'Yield %':^13} | "+\
                f"{'Earnings/Loss':^13} | {'Yearly Earnings/Loss %':^13} |"  )
        print("-"*138)
        print()
        bonds = investor.bonds
        for bond in bonds :
            print(f"|{bond.symbol:^13} | {bond.quantity:^13}"+\
            f" | {bond.purchase_price:^13} | {bond.current_value:^13} "+\
            f" | {bond.coupon:^13} | {bond.yield_percentage:^13} "+\
            f" | {bond.earning_or_loss:^13} | {bond.yearly_percent_change:^20} |")
            print("-"*138)
            print()
        #Printing the bond with highest increase and max decrease
        if (investor.highest_earning_bond):
            print("-----------------------------------------------------------------------------------------")
            print("The bond with the highest increase in value in your portfolio on a per-bond basis is:" \
                ,investor.highest_earning_bond)
            print("-----------------------------------------------------------------------------------------")
        if(investor.highest_loss_bond):
            print("-----------------------------------------------------------------------------------------")
            print("The bond with max decrease in value in your portfolio on a per-bond basis is:" \
                ,investor.highest_loss_bond)
            print("-----------------------------------------------------------------------------------------")

def draw_stock_progress_graph(investors):
    '''
    This function will draw the stock progress graph for each investor.
    '''
    stock_color = ['','b','g','r','c','m','y','k','purple']
    for investor in investors.values() :
        stocks = investor.stocks
        #Setting the canvas of the graph width 20 and height 15
        fig = plt.figure(figsize=(20, 15))
        for stock in stocks :
            stock_progress = stock.stock_progress
            stock_id = stock.purchase_id
            stock_name = stock.symbol
            #Generating the list of all the dates for each stock entry
            progress_dates = list(map(lambda progress:progress['Date'], stock_progress))
            #Converting the date to Matplotlib date type
            x_axis_data = mdates.date2num(progress_dates)
            #Generating the list of all the stock_close_value = close * number_of_shares 
            stock_close_values = list(map(lambda progress:progress['stock_close_value'], stock_progress))
            #plotting the graph
            plt.plot_date(x_axis_data,stock_close_values,lw=1,ls='solid',c=stock_color[stock_id],\
                            marker='None',label= stock_name)
        fig.autofmt_xdate()
        plt.legend()
        plt.xlabel('Stock Purchase Date')
        #Rotating the x lables to fit to the screen
        plt.xticks(rotation=25)
        plt.ylabel('Closing Price (Close Price * # Shares) (in Dollars)')
        #Saving the graph in the png image format.
        plt.savefig("Patait.Anuj.StockProgressGraph.png")

def stock_describe(investors):
    '''
    This function will calculate all the basic stats for the given stocks and
    will print the result on the screen.
    '''
    for investor in investors.values() :
        stocks = investor.stocks
        
        all_stocks = []

        for stock in stocks :
            stock_desc = {}
            stocks_progress_df = pd.DataFrame.from_dict(stock.stock_progress)
            stocks_progress_df['Stock']=stock.symbol

            #calculating stock description
            stock_mean = stocks_progress_df['stock_close_value'].mean()
            stock_sd = stocks_progress_df['stock_close_value'].std()
            stock_min = stocks_progress_df['stock_close_value'].min()
            stock_max = stocks_progress_df['stock_close_value'].max()
            #Rounding the values
            stock_desc['Stock'] = stock.symbol
            stock_desc['Average Close Value'] = round(stock_mean,2)
            stock_desc['Standard Deviation'] = round(stock_sd,2)
            stock_desc['Minimum Close Value'] = round(stock_min,2)
            stock_desc['Maximum Close Value'] = round(stock_max,2)
            all_stocks.append(stock_desc)
        #Converting list to pandas dataFrame 
        all_stocks_df = pd.DataFrame(all_stocks)

        #Printing the dataFrame
        print()
        print("-----------------------------------------------------------------------------------------")
        print('Stocks description are presented below:')
        print("-----------------------------------------------------------------------------------------")
        print()
        print(all_stocks_df)
        print()
        print("-----------------------------------------------------------------------------------------")
        #Printing all the calculations to the html file.
        all_stocks_df.to_html('Patait.Anuj.StockDescription.html')


    