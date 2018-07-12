# pip install python-kucoin
import time
import pickle
from kucoin.client import Client
##### Pickle Database Upload Section ##########
try:
 ETN = pickle.load(open('Etn.vnm','rb'))
 print('ETN To Be Traded: [{}].'.format(ETN))
except Exception as Pickle_Error:
 if 'Etn.vnm' in Pickle_Error:
  print('We Need A New File That Tells Us How Much ETN To Trade.')
  print('Enter The Total ETN To Trade Please As A Number Only! Seriously Or This Will Break.')
  ETN_TOTAL = input('>>: ')
  ETN = int(ETN_TOTAL)
  pickle.dump(ETN,open('Etn.vnm','wb'))
  print('File Saved, Thank You.')
 else:
  print('Fuck Something Might Be Wrong With Pickle Contact Skrypt With This Error: [{}]'.format(Pickle_Error))

###### USER SETUP BELOW ##########
TIMER = 0.0 # Total Seconds Recommended 2.0
API_KEY = '' # INPUT API KEY
API_SECRET = '' # INPUT API SECRET
Sell = 175.0
Buy = 174.0

####### OBJECT GUTS BELOW ######
client = Client(API_KEY, API_SECRET)
print('>>: Welcome To KuKoin BTC-ETN Trader! Written By Skrypt Please Feel Free To Donate In KCS!')
print('>>: Skrypt [KCS] Donation Address: [0x358914f9b0774833ab09e68afa353629c8acc395]')


def calc_sell():
 tick = client.get_tick('ETN-BTC')
 if tick['sell'] * 1e8 >= Sell:
  return [True, tick['sell'] * 1e8]
 else:
  return [False, tick['sell'] * 1e8]

def calc_buy():
 tick = client.get_tick('ETN-BTC')
 if tick['buy'] * 1e8 <= Buy:
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
 ETN = pickle.load(open('Etn.vnm','rb'))
 balance = client.get_coin_balance('ETN')
 if balance >= ETN:
  print('Selling {} ETN For {} Satoshi Each'.format(ETN,tick['sell']*1e8))
  sold = client.create_sell_order('ETN-BTC', tick['sell'], ETN)
  print(sold)
 elif balance < ETN and balance > 0:
  print('Selling {} ETN For {} Satoshi Each'.format(balance,tick['sell']*1e8))
  sold = client.create_sell_order('ETN-BTC', tick['sell'], balance)
  print(sold)
 else:
  print('Not Enough Balance For Trading Routine. Instructing Program To Exit')
  exit()

def buy_etn():
 tick = client.get_tick('ETN-BTC')
 balance = client.get_coin_balance('BTC')
 balance_etn = client.get_coin_balance('ETN')
 ETN = pickle.load(open('Etn.vnm','rb'))
 if tick['buy']*ETN <= balance:
  print('Buying {} ETN For {} Satoshi Each'.format(ETN,tick['buy']*1e8))
  bought = client.create_buy_order('ETN-BTC', tick['buy'], tick['buy']*ETN)
  print(bought)
 elif ticktick['buy']*(ETN-balance_etn) <= balance:
  print('Buying {} ETN For {} Satoshi Each'.format((ETN-balance_etn),tick['buy']*1e8))
  bought = client.create_buy_order('ETN-BTC', tick['buy'], tick['buy']*(ETN-balance_etn))
  print(bought)
 else:
  print('Not Enough Balance For Trading Routine. Instructing Program To Exit')
  exit()


while True:
 trade = get_etn_balance()
 if trade == 'Sell':
  should_sell = calc_sell()
  if should_sell[0] == True:
   print('Selling ETN At {} Satoshi'.format(should_sell[1]))
   transaction = sell_etn()
   time.sleep(TIMER)
  else:
   print('>>: [SELL] Waiting For Price Flux')
   time.sleep(TIMER)
 elif trade == 'Buy':
  should_buy = calc_buy()
  if should_buy[0] == True:
   print('Buying ETN At {} Satoshi'.format(should_buy[1]))
   transaction = buy_etn()
   time.sleep(TIMER)
  else:
   print('>>: [BUY] Waiting For Price Flux')
   time.sleep(TIMER)
 else:
  print('>>: Something Has Fucked Up, Waiting Timer Then Trying Again')
  time.sleep(TIMER)


