#-----------------------------------------------
# Script Name: Realtime_Ticker_price.py
# Description: This script will provide the realtime ticker price
#              using python library - wallstreet
# Notes:
#       1. Flask is used to generate the request so that we can call the api in the main page
#       2. wallstreet, flask, venv libaries needs to configure to use this utility
#
# Instrunctions : To run this program, first
#                1. open the command prompt - cd script path
#                    for example - cd C:\Users\Ananta\Desktop\Idea\Program
#                2. set FLASK_APP=Realtime_Ticker_price.py
#                3. start the flask run by python -m flask run
#               4.  To see the realtime price - development mode
#                   http://localhost:5000/rt_stock_price?ticker_name=MSFT
#
#-----------------------------------------------

from flask import Flask
from flask import request,jsonify
from wallstreet import Stock, Call, Put
from flask import Flask, make_response
import yfinance as yf
from yahoofinancials import YahooFinancials 
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/rt_stock_price',methods=['GET', 'POST'])
def rt_stock_price():
    ticker_name=request.args.get('ticker_name')
    s = Stock(ticker_name)
    return '%s' %(s.price)

@app.route('/earning_cal',methods=['GET', 'POST'])
def EarningCal_Call():
    ticker_name=request.args.get('ticker_name')
    yahoo_financials = YahooFinancials(ticker_name)
    earning_cal_data=yahoo_financials.get_stock_earnings_data() 
    return jsonify(results = earning_cal_data)

@app.route('/option_expire',methods=['GET', 'POST'])
def expire_call():
    ticker_name=request.args.get('ticker_name')
    ticker_info = yf.Ticker(ticker_name)
    ticker_expiration_dates = ticker_info.options
    return jsonify(results = ticker_expiration_dates)

@app.route('/option_call',methods=['GET', 'POST'])
def OptionCall_call():
    query_params=request.args
    query_result=query_params.to_dict()
    ticker_name=query_result['ticker_name']
    end_date=query_result['end_date']
    end_date_year=int(end_date.split('-')[0])
    end_date_month=int(end_date.split('-')[1])
    end_date_day=int(end_date.split('-')[2])
    ticker_info = yf.Ticker(ticker_name)
    opt = ticker_info.option_chain(end_date)
    Call_data=opt.calls 
    Call_data_result=Call_data.values.tolist()
    return jsonify(results = Call_data_result)

@app.route('/option_put',methods=['GET', 'POST'])
def OptionPut_call():
    query_params=request.args
    query_result=query_params.to_dict()
    ticker_name=query_result['ticker_name']
    end_date=query_result['end_date']
    end_date_year=int(end_date.split('-')[0])
    end_date_month=int(end_date.split('-')[1])
    end_date_day=int(end_date.split('-')[2])
    ticker_info = yf.Ticker(ticker_name)
    opt = ticker_info.option_chain(end_date)
    Put_data=opt.puts 
    Put_data_result=Put_data.values.tolist()
    return jsonify(results = Put_data_result)

@app.route('/optionCall_detail',methods=['GET', 'POST'])
def OptionCall_Details():
    query_params=request.args
    query_result=query_params.to_dict()
    ticker_name=query_result['ticker_name']
    contractSymbol=query_result['contractSymbol']
    end_date=query_result['end_date']
    end_date_year=int(end_date.split('-')[0])
    end_date_month=int(end_date.split('-')[1])
    end_date_day=int(end_date.split('-')[2])
    ticker_info = yf.Ticker(ticker_name)
    opt = ticker_info.option_chain(end_date)
    Call_data=opt.calls
    x=Call_data[Call_data.contractSymbol == contractSymbol]
    strike_price=x.iloc[0,2]
    x_data=x.values.tolist()
    g=Call(ticker_name, d=end_date_day, m=end_date_month, y=end_date_year, strike=strike_price)
    IV=str(g.implied_volatility())
    x_data.append(IV)
    Delta=str(g.delta())
    x_data.append(Delta)
    vega=str(g.vega())
    x_data.append(vega)
    Theta=str(g.theta())
    x_data.append(Theta)
    Rho=str(g.rho())
    x_data.append(Rho)
    Underlying_P=str(g.underlying.price)
    x_data.append(Underlying_P)
    return jsonify(results = x_data)



@app.route('/Key_Data',methods=['GET', 'POST'])
def KeyData_Call():
    ticker_name=request.args.get('ticker_name')
    keydata=yf.Ticker(ticker_name)
    keydata_set=keydata.info
    key_data=[]

    #Sector
    sector=keydata_set['sector']
    key_data.append(sector)

    # Full-time employees
    fullTimeEmployees=keydata_set['fullTimeEmployees']
    key_data.append(fullTimeEmployees)

    #Summary
    Summary=keydata_set['longBusinessSummary']
    key_data.append(Summary)

    #State 
    state=keydata_set['state']
    key_data.append(state)

    #Country
    country=keydata_set['country']
    key_data.append(country)

    #52 weeks low 
    week_52_low=str(keydata_set['fiftyTwoWeekLow'])
    key_data.append(week_52_low)
  
    #52 weeks high
    week_52_high=str(keydata_set['fiftyTwoWeekHigh'])
    key_data.append(week_52_high)

    #Website
    website=keydata_set['website']
    key_data.append(website)

    # Previous Close
    Prev_close=keydata_set['previousClose']
    key_data.append(Prev_close)

    # Dividend Rate
    Dividend_Rate=keydata_set['dividendRate']
    key_data.append(Dividend_Rate)

    #Market Cap
    Market_Cap=keydata_set['marketCap']
    key_data.append(Market_Cap)

    # Vol 24 hour
    Vol_24_hour=keydata_set['volume24Hr']
    key_data.append(Vol_24_hour)

    # dividendYield
    dividendYield=str(keydata_set['dividendYield'])
    key_data.append(dividendYield)

    # trailingPE
    trailingPE=str(keydata_set['trailingPE'])
    key_data.append(trailingPE)
    return jsonify(results = key_data)

@app.route('/Nasdaq_Data',methods=['GET', 'POST'])
def Nasdaq_RT_Call():
    ticker_name=request.args.get('ticker_name')
    s=Stock(ticker_name)
    Nasdaq_composite_data=[]
    price=s.price
    Nasdaq_composite_data.append(price)
    Last_Trade=s.last_trade
    Nasdaq_composite_data.append(Last_Trade)
    change=s.change
    Nasdaq_composite_data.append(change)
    change_percent=s.cp
    Nasdaq_composite_data.append(change_percent)
    return jsonify(results = Nasdaq_composite_data)

if __name__ == "__main__":
    app.run()
