# pip install python-kucoin
import time
from kucoin.client import Client
print('>>: Welcome To KuKoin BTC-ETN Trader! Written By Skrypt Please Feel Free To Donate In KCS!')
print('>>: Skrypt [KCS] Donation Address: [0x358914f9b0774833ab09e68afa353629c8acc395]')

####### OBJECT GUTS BELOW ######
def set_trade_amount():
 global ETN
 global Etn_Set
 balance_etn = client.get_coin_balance('ETN')
 balance_btc = client.get_coin_balance('BTC')
 tick = client.get_tick('ETN-BTC')
 Sell = tick['sell']
 print('Current ETN Balance: [{}].'.format(balance_etn['balance']))
 print('Current BTC Balance: [{}].'.format(balance_btc['balance']))
 print('You May Trade Current BTC: [{}] For [{}] ETN At [{}] Satoshi Per ETN'.format(balance_btc['balance'],balance_btc['balance']//Sell,Sell*1e8))
 print('How Much ETN Are You Trading? [FLOAT/#.#]')
 ETN = input('>>: ')
 try:
  squishy = '0.1'
  Test = float(ETN) + float(squishy)
  print('ETN To Be Traded: [{}].'.format(ETN))
  Etn_Set = True
 except Exception as Float_Error:
  print('You Must Enter A Float Here.')
  set_trade_amount()
  
def set_call_timer():
 global TIMER
 global Timer_Set
 print('How Much Time (In Seconds) Between Calls? [FLOAT/#.#]')
 TIMER = input('>>: ')
 try:
  Test = float(TIMER) + 0.1
  print('Time In Seconds Before Each Call: [{}].'.format(TIMER))
  Timer_Set = True
 except Exception as Float_Error:
  print('You Must Enter A Float Here.')
  set_call_timer()

def set_buy_max():
 global BUY_MAX
 global Buy_Max_Set
 tick = client.get_tick('ETN-BTC')
 Sell = tick['sell'] * 1e8
 print('Last ETN Sale Price Satoshi Per ETN [{}].'.format(Sell))
 print('How Much Max Do You Want To Spend Per ETN In Satoshi? [FLOAT/#.#]')
 BUY_MAX = input('>>: ')
 try:
  Test = float(BUY_MAX) + 0.1
  print('Spending: [{}] Max Satoshi Per ETN.'.format(BUY_MAX))
  Buy_Max_Set = True
 except Exception as Float_Error:
  print('You Must Enter A Float Here.')
  set_buy_max()

def set_sell_min():
 global SELL_MIN
 global Sell_Min_Set
 tick = client.get_tick('ETN-BTC')
 Buy = tick['buy'] * 1e8
 print('Last ETN Buy Price Satoshi Per ETN [{}].'.format(Buy))
 print('How Much Min Do You Want To Sell Per ETN In Satoshi? [FLOAT/#.#]')
 SELL_MIN = input('>>: ')
 try:
  Test = float(SELL_MIN) + 0.1
  print('Selling Each ETN For [{}] Min Satoshi Per ETN.'.format(SELL_MIN))
  Sell_Min_Set = True
 except Exception as Float_Error:
  print('You Must Enter A Float Here.')
  set_sell_min()

def set_api_key():
 global API_KEY
 global Api_Key_Set
 print('Please Enter Kucoin API Key [KEY]')
 API_KEY = input('>>: ')
 try:
  print('Current API Key: [{}].'.format(API_KEY))
  Api_Key_Set = True
 except Exception as Api_Key_Error:
  print('You Must Enter A Kucoin API Key.')
  set_api_key()

def set_api_secret():
 global API_SECRET
 global Api_Secret_Set
 print('Please Enter Kucoin API Secret [SECRET]')
 API_SECRET = input('>>: ')
 try:
  print('Current API Secret: [{}].'.format(API_SECRET))
  Api_Secret_Set = True
 except Exception as Api_Secret_Error:
  print('You Must Enter A Kucoin API Secret.')
  set_api_secret()

def calc_sell():
 tick = client.get_tick('ETN-BTC')
 if float(tick['sell']) * 1e8 >= float(SELL_MIN):
  return [True, tick['sell'] * 1e8]
 else:
  return [False, tick['sell'] * 1e8]

def calc_buy():
 tick = client.get_tick('ETN-BTC')
 if float(tick['buy']) * 1e8 <= float(BUY_MAX):
  return [True, tick['buy'] * 1e8]
 else:
  return [False, tick['buy'] * 1e8]

def get_etn_balance():
 balance = client.get_coin_balance('ETN')
 if balance['balance'] > 0:
  return 'Sell'
 elif balance['balance'] <= 0:
  return 'Buy'

def sell_etn():
 tick = client.get_tick('ETN-BTC')
 balance = client.get_coin_balance('ETN')
 if float(balance['balance']) >= float(ETN):
  print('Selling {} ETN For {} Satoshi Each'.format(ETN,tick['sell']*1e8))
  sold = client.create_sell_order('ETN-BTC', tick['sell'], ETN)
  print(sold)
 elif float(balance['balance']) < float(ETN) and float(balance['balance']) > 0:
  print('Selling {} ETN For {} Satoshi Each'.format(balance['balance'],tick['sell']*1e8))
  sold = client.create_sell_order('ETN-BTC', tick['sell'], balance['balance'])
  print(sold)
 else:
  print('Not Enough Balance For Trading Routine.')

def buy_etn():
 tick = client.get_tick('ETN-BTC')
 balance = client.get_coin_balance('BTC')
 balance_etn = client.get_coin_balance('ETN')
 if float(tick['buy'])*float(ETN) <= float(balance['balance']):
  print('Buying {} ETN For {} Satoshi Each'.format(ETN,tick['buy']*1e8))
  bought = client.create_buy_order('ETN-BTC', tick['buy'], str(float(tick['buy'])*float(ETN)))
  print(bought)
 elif float(tick['buy'])*(float(ETN)-float(balance_etn['balance'])) <= balance['balance']:
  print('Buying {} ETN For {} Satoshi Each'.format((float(ETN)-float(balance_etn['balance'])),tick['buy']*1e8))
  bought = client.create_buy_order('ETN-BTC', tick['buy'], str(float(tick['buy'])*(float(ETN)-float(balance_etn['balance']))))
  print(bought)
 else:
  print('Not Enough Balance For Trading Routine.')

def Activate_Client():
 global client
 try:
  client = Client(API_KEY, API_SECRET)
  print('Client Activated With API Key [{}].'.format(API_KEY))
 except Exception as Client_Error:
  print('There Was A Client Activation Error Trying Again.')
  Activate_Client()

def set_globals():
 global Timer_Set
 global Api_Key_Set
 global Api_Secret_Set
 global Buy_Max_Set
 global Sell_Min_Set
 global Etn_Set
 Timer_Set = None
 Api_Key_Set = None
 Api_Secret_Set = None
 Buy_Max_Set = None
 Sell_Min_Set = None
 Etn_Set = None
 print('All Global Controls Reset To [NONE]')

print('Setting Global Controls Now.')
set_globals()
while True:
 if Timer_Set == None or Timer_Set == False:
  set_call_timer()
 if Api_Key_Set == None or Api_Key_Set == False:
  set_api_key()
 if Api_Secret_Set == None or Api_Key_Set == False:
  set_api_secret()
  Activate_Client()
 if Etn_Set == None or Etn_Set == False:
  set_trade_amount()
 if Buy_Max_Set == None or Buy_Max_Set == False:
  set_buy_max()
 if Sell_Min_Set == None or Sell_Min_Set == False:
  set_sell_min()
 else:
  try:
   trade = get_etn_balance()
   if trade == 'Sell':
    should_sell = calc_sell()
    if should_sell[0] == True:
     print('Selling ETN At {} Satoshi'.format(should_sell[1]))
     transaction = sell_etn()
     time.sleep(float(TIMER))
    else:
     print('>>: [SELL] Waiting For Price Flux')
     time.sleep(float(TIMER))
   elif trade == 'Buy':
    should_buy = calc_buy()
    if should_buy[0] == True:
     print('Buying ETN At {} Satoshi'.format(should_buy[1]))
     transaction = buy_etn()
     time.sleep(float(TIMER))
    else:
     print('>>: [BUY] Waiting For Price Flux')
     time.sleep(float(TIMER))
   else:
    print('>>: Something Has Fucked Up, Waiting Timer Then Trying Again')
    time.sleep(float(TIMER))
  except Exception as Run_Time_Error:
   print('We Have Had The Following Run Time Error: [{}]'.format(Run_Time_Error))
   print('Going To Continue Please Escape With CTRL+C Or Exit The Program If You Notice Something Other Then AUTH Error Message And Contact Skrypt With Plenty Of Information.')

