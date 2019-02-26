from flask import Flask, jsonify, Response, render_template
import nsepy
from nsetools import Nse
from pprint import pprint
from operator import itemgetter
import json
import time
from datetime import date
import math
from urllib.parse import quote
from pymongo import MongoClient
app = Flask(__name__)
nse = Nse()



capital = 5000
mongo_client = MongoClient(
    'mongodb+srv://sathya:45Xa8zKRJdEcplrd@cluster0-gvw7z.mongodb.net/test?retryWrites=true')
db = mongo_client['tittu']
@app.route("/")
def hello():
    db_data = db.get_collection('gap_data').find_one({"date": str(date.today())})
    if(db_data != None):
        return jsonify(db_data)
    else:
        return "Trade not Triggered"


@app.route("/get_gapups")
def getf():
    return Response(getgap_up(), content_type='application/json')


def getgap_up():
    startTime = time.time()
    all_data = []
    try:
        all_stock_symbol = [
            "ACC",
            "ADANIENT",
            "ADANIPORTS",
            "ADANIPOWER",
            "AJANTPHARM",
            "ALBK",
            "AMARAJABAT",
            "AMBUJACEM",
            "APOLLOHOSP",
            "APOLLOTYRE",
            "ARVIND",
            "ASHOKLEY",
            "ASIANPAINT",
            "AUROPHARMA",
            "AXISBANK",
            "BAJAJ-AUTO",
            "BAJAJFINSV",
            "BAJFINANCE",
            "BALKRISIND",
            "BANKBARODA",
            "BANKINDIA",
            "BATAINDIA",
            "BEL",
            "BEML",
            "BERGEPAINT",
            "BHARATFIN",
            "BHARATFORG",
            "BHARTIARTL",
            "BHEL",
            "BIOCON",
            "BOSCHLTD",
            "BPCL",
            "BRITANNIA",
            "CADILAHC",
            "CANBK",
            "CANFINHOME",
            "CASTROLIND",
            "CEATLTD",
            "CENTURYTEX",
            "CESC",
            "CGPOWER",
            "CHENNPETRO",
            "CHOLAFIN",
            "CIPLA",
            "COALINDIA",
            "COLPAL",
            "CONCOR",
            "CUMMINSIND",
            "DABUR",
            "DCBBANK",
            "DHFL",
            "DISHTV",
            "DIVISLAB",
            "DLF",
            "DRREDDY",
            "EICHERMOT",
            "ENGINERSIN",
            "EQUITAS",
            "ESCORTS",
            "EXIDEIND",
            "FEDERALBNK",
            "GAIL",
            "GLENMARK",
            "GMRINFRA",
            "GODFRYPHLP",
            "GODREJCP",
            "GODREJIND",
            "GRASIM",
            "GSFC",
            "HAVELLS",
            "HCLTECH",
            "HDFC",
            "HDFCBANK",
            "HEROMOTOCO",
            "HEXAWARE",
            "HINDALCO",
            "HINDPETRO",
            "HINDUNILVR",
            "HINDZINC",
            "IBULHSGFIN",
            "ICICIBANK",
            "ICICIPRULI",
            "IDBI",
            "IDEA",
            "IDFC",
            "IDFCFIRSTB",
            "IFCI",
            "IGL",
            "INDIACEM",
            "INDIANB",
            "INDIGO",
            "INDUSINDBK",
            "INFIBEAM",
            "INFRATEL",
            "INFY",
            "IOC",
            "IRB",
            "ITC",
            "JETAIRWAYS",
            "JINDALSTEL",
            "JISLJALEQS",
            "JPASSOCIAT",
            "JSWSTEEL",
            "JUBLFOOD",
            "JUSTDIAL",
            "KAJARIACER",
            "KOTAKBANK",
            "KPIT",
            "KSCL",
            "KTKBANK",
            "L&TFH",
            "LICHSGFIN",
            "LT",
            "LUPIN",
            "M&M",
            "M&MFIN",
            "MANAPPURAM",
            "MARICO",
            "MARUTI",
            "MCDOWELL-N",
            "MCX",
            "MFSL",
            "MGL",
            "MINDTREE",
            "MOTHERSUMI",
            "MRF",
            "MRPL",
            "MUTHOOTFIN",
            "NATIONALUM",
            "NBCC",
            "NCC",
            "NESTLEIND",
            "NHPC",
            "NIITTECH",
            "NMDC",
            "NTPC",
            "OFSS",
            "OIL",
            "ONGC",
            "ORIENTBANK",
            "PAGEIND",
            "PCJEWELLER",
            "PEL",
            "PETRONET",
            "PFC",
            "PIDILITIND",
            "PNB",
            "POWERGRID",
            "PVR",
            "RAMCOCEM",
            "RAYMOND",
            "RBLBANK",
            "RCOM",
            "RECLTD",
            "RELCAPITAL",
            "RELIANCE",
            "RELINFRA",
            "REPCOHOME",
            "RPOWER",
            "SAIL",
            "SBIN",
            "SHREECEM",
            "SIEMENS",
            "SOUTHBANK",
            "SREINFRA",
            "SRF",
            "SRTRANSFIN",
            "STAR",
            "SUNPHARMA",
            "SUNTV",
            "SUZLON",
            "SYNDIBANK",
            "TATACHEM",
            "TATACOMM",
            "TATAELXSI",
            "TATAGLOBAL",
            "TATAMOTORS",
            "TATAMTRDVR",
            "TATAPOWER",
            "TATASTEEL",
            "TCS",
            "TECHM",
            "TITAN",
            "TORNTPHARM",
            "TORNTPOWER",
            "TV18BRDCST",
            "TVSMOTOR",
            "UBL",
            "UJJIVAN",
            "ULTRACEMCO",
            "UNIONBANK",
            "UPL",
            "VEDL",
            "VGUARD",
            "VOLTAS",
            "WIPRO",
            "WOCKPHARMA",
            "YESBANK",
            "ZEEL"
        ]
        missed_stock = []
        yield '{"stock data": ['
        for symbol in all_stock_symbol:
            print('Fetching Stock ----- ' + symbol)
            try:
                data = nsepy.get_quote(quote(symbol,safe=''))
                json_data = data
                gap_up = round(((json_data.get(
                    'open') - json_data.get('previousClose'))/json_data.get('previousClose'))*100, 2)
                temp_dict = {}
                temp_dict['name'] = symbol
                temp_dict['gap_up_percent'] = gap_up
                temp_dict['close'] = json_data.get('previousClose')
                temp_dict['open'] = json_data.get('open')
                if(temp_dict['close'] >= 30):
                    all_data.append(temp_dict)
                yield json.dumps({symbol: temp_dict}) + ', '
            except Exception as e:
                missed_stock.append(symbol)
                print(e)
                pass
        yield '],'
        tryCount = 0
        missed_stock_copy = missed_stock[0:]
        yield '"retry:['
        while len(missed_stock) > 0 and tryCount <= 10:
            tryCount += 1
            yield str(tryCount) + ','
            print('------Count: ' + str(tryCount))
            for symbol in missed_stock:
                try:
                    time.sleep(1)
                    data = nse.get_quote(symbol)
                    print(data)
                    json_data = data
                    gap_up = round(((json_data.get(
                        'open') - json_data.get('previousClose'))/json_data.get('previousClose'))*100, 2)
                    temp_dict = {}
                    temp_dict['name'] = symbol
                    temp_dict['gap_up_percent'] = gap_up
                    temp_dict['close'] = json_data.get('previousClose')
                    temp_dict['open'] = json_data.get('open')
                    if(temp_dict['close'] >= 30):
                        all_data.append(temp_dict)
                    missed_stock_copy.remove(symbol)
                    print('success: ' + symbol)
                except Exception as e:
                    print(e)
                    print('Missed -----' + symbol)
                    pass
                missed_stock = missed_stock_copy[0:]
        yield '], "missed_stock":' + json.dumps(missed_stock) + ','

        print(missed_stock)

    except Exception as e:
        print(e)
        pass
    endTime = time.time()
    print(endTime - startTime)
    all_data = sorted(all_data, key=itemgetter('gap_up_percent'))
    global top_10, bottom_10,db
    top_10 = all_data[-10:]
    top_10 = list(reversed(top_10))
    bottom_10 = all_data[0:10]
    db.get_collection('gap_data').replace_one({"date": str(date.today())},{ "date": str(date.today()),"top_10": top_10, "bottom_10": bottom_10},upsert=True)
    yield ' "top_10":' + json.dumps(top_10) + ', "bottom_10":' + json.dumps(bottom_10) + '}'


@app.route('/get-range')
def find_range_for_stock():
    global db
    db_data = db.get_collection('gap_data').find_one({"date": str(date.today())})
    top_10=[]
    bottom_10 = []
    if(db_data):
        top_10 = db_data.get('top_10')
        bottom_10 = db_data.get('bottom_10')
    top_error_index = []
    bottom_error_index = []
    for i in range(0, len(top_10)):
        try:
            data = nsepy.get_quote(top_10[i]['name'])
            top_10[i]['orb_low'] = round((data.get('dayLow') - 0.05),2)
            top_10[i]['orb_high'] = round(data.get('dayHigh') + 0.05,2)
            top_10[i]['quantity'] = math.floor((capital * 0.01) /((top_10[i]['orb_high'] + 0.05) - (top_10[i]['orb_low'] - 0.05)))
            top_10[i]['range'] =  round((top_10[i]['orb_high']) - ( top_10[i]['orb_low']),2)
            top_10[i]['orb_ratio'] = round(100 * (
                top_10[i]['orb_high'] - top_10[i]['orb_low']) / top_10[i]['orb_low'], 2)
        except Exception as e:
            top_error_index.append(i)
            pass
    for i in range(0, len(bottom_10)):
        try:
            data = nsepy.get_quote(bottom_10[i]['name'])
            bottom_10[i]['orb_low'] = round((data.get('dayLow') - 0.05),2)
            bottom_10[i]['orb_high'] = round(data.get('dayHigh') + 0.05,2)
            bottom_10[i]['quantity'] = math.floor((capital * 0.01) /((bottom_10[i]['orb_high'] + 0.05) - (bottom_10[i]['orb_low'] - 0.05)))
            bottom_10[i]['range'] =  round((bottom_10[i]['orb_high']) - ( bottom_10[i]['orb_low']),2)
            bottom_10[i]['orb_ratio'] = round(100 * (
                bottom_10[i]['orb_high'] - bottom_10[i]['orb_low']) / bottom_10[i]['orb_low'], 2)
        except Exception as e:
            bottom_error_index.append(i)
            pass
    retry_count = 0
    while(len(top_error_index) > 0 and retry_count < 10):
        retry_count += 1
        for i in top_error_index:
            try:
                data = nsepy.get_quote(top_10[i]['name'])
                top_10[i]['orb_low'] = round((data.get('dayLow') - 0.05),2)
                top_10[i]['orb_high'] = round(data.get('dayHigh') + 0.05,2)
                top_10[i]['range'] =  round((top_10[i]['orb_high']) - ( top_10[i]['orb_low']),2)
                top_10[i]['quantity'] = math.floor((capital * 0.01) /((top_10[i]['orb_high'] + 0.05) - (top_10[i]['orb_low'] - 0.05)))
                top_10[i]['orb_ratio'] = round(100 * (
                    top_10[i]['orb_high'] - top_10[i]['orb_low']) / top_10[i]['orb_low'], 2)
                top_error_index.remove(i)
            except:
                pass
    retry_count = 0
    while(len(bottom_error_index) > 0 and retry_count < 10):
        retry_count += 1
        for i in bottom_error_index:
            try:
                data = nsepy.get_quote(bottom_10[i]['name'])
                bottom_10[i]['orb_low'] = round((data.get('dayLow') - 0.05),2)
                bottom_10[i]['orb_high'] = round(data.get('dayHigh') + 0.05,2)
                bottom_10[i]['range'] =  round((bottom_10[i]['orb_high']) - ( bottom_10[i]['orb_low']),2)
                bottom_10[i]['quantity'] = math.floor((capital * 0.01) /((bottom_10[i]['orb_high'] + 0.05) - (bottom_10[i]['orb_low'] - 0.05)))
                bottom_10[i]['orb_ratio'] = round(100 * (
                    bottom_10[i]['orb_high'] - bottom_10[i]['orb_low']) / bottom_10[i]['orb_low'], 2)
                bottom_error_index.remove(i)
            except:
                pass
    print(bottom_error_index)
    print(bottom_10)
    print(top_error_index)
    print(top_10)
    if(len(bottom_error_index) > 0):
        for i in bottom_error_index:
            bottom_10.remove(bottom_10[i])
    if(len(top_error_index) > 0):
        for i in top_error_index:
            top_10.remove(top_10[i])
    print(bottom_error_index)
    print(bottom_10)
    print(top_error_index)
    print(top_10)
    global best_bottom_5,best_top_5
    best_top_5 = []
    best_bottom_5 = []

    best_top_5 = top_10[:5]
    best_bottom_5 = bottom_10[:5]
    if(len(best_top_5) > 1):
        db.get_collection('gap_data').update_one({"date": str(date.today())}, {"$set":{"top_5": best_top_5, "bottom_5": best_bottom_5}})  
    return json.dumps({"top_5": best_top_5, "bottom_5": best_bottom_5})


@app.route('/place')
def place():
    global db
    db_data = db.get_collection('gap_data').find_one({"date": str(date.today())})
    if(db_data != None and db_data.get('top_5') and db_data.get('bottom_5')):
        return render_template('index.html', top_5=db_data.get('top_5'),bottom_5 = db_data.get('bottom_5'))
    else:
        return "Trade not triggered"


if __name__ == "__main__":
    app.run()
