import json
import csv
import datetime
from pycoingecko import CoinGeckoAPI

def import_csv(csvFile):
    data = {}
    with open(csvFile) as csvFile:
        csvReader = csv.DictReader(csvFile)
        i = 0
        for rows in csvReader:
            #id = rows['CRYPTO']
            id = i
            i = i + 1
            data[id] = {'CRYPTO':rows['CRYPTO'], 'BALANCE':rows['BALANCE'],'PRICE':rows['PRICE']}

    return data
        
cg = CoinGeckoAPI()

old_dollar_price_huf = 295

# Import file
csvFile = r'portfolio.txt'
jsonFile = r'portfolio.json'

# portfolio variable container imported CSV data
portfolio = import_csv(csvFile)

# res variable contains fresh coin data from CoinGecko
res = cg.get_price(ids=['bitcoin',
                        'ethereum',
                        'qanplatform',
                        'zelcash',
                        'binancecoin'
                        ],
                        vs_currencies=['usd','huf'], include_24hr_change='true')

data = {}
all_oldPriceHUF = all_oldPriceUSD = all_newPriceUSD = all_newPriceHUF = all_balance = 0
total_inc = 0
i = 0

for c in portfolio:
    print("Crypto: ", c)
    crypto = portfolio[i]['CRYPTO']
    print("Crypto: ", crypto)
    balance = float(portfolio[i]['BALANCE'])
    all_balance += balance
    print("Balance: ", balance)

    oldPriceUSD = float(portfolio[i]['PRICE'])
    oldPriceHUF = float(portfolio[i]['PRICE']) * old_dollar_price_huf
    all_oldPriceHUF += float(oldPriceHUF) * balance
    all_oldPriceUSD += float(oldPriceUSD) * balance
    print("Old Price: ", oldPriceUSD)
    newPriceUSD = float(res[crypto]['usd'])
    all_newPriceUSD += newPriceUSD * balance

    newPriceHUF = float(res[crypto]['huf'])
    all_newPriceHUF += newPriceHUF * balance

    old_solo_total_USD = round(oldPriceUSD * balance, 0)
    old_solo_total_HUF = round(oldPriceHUF * balance, 0)
    new_solo_total_USD = round(newPriceUSD * balance, 0)
    new_solo_total_HUF = round(newPriceHUF * balance, 0)

    print("New Price: ", newPriceUSD)

    if newPriceUSD > oldPriceUSD:
        change = "UP"
    else:
        change = "DOWN"

    inc = round((newPriceUSD / oldPriceUSD) * 100 - 100, 2)
    total_inc += inc

    method = "RETAIN"
    if inc > 100:
        method = "SELL"

    print(inc)        
    print("")

    data[i] = {'ID': crypto, 'CRYPTO': portfolio[i]['CRYPTO'], 'BALANCE': portfolio[i]['BALANCE'], 'OLDPRICE-USD': oldPriceUSD, 'OLDPRICE-HUF': oldPriceHUF, 'NEWPRICE-USD': newPriceUSD, 'NEWPRICE-HUF': newPriceHUF, 'OLD-SOLO-TOTAL-USD': old_solo_total_USD, 'NEW-SOLO-TOTAL-USD': new_solo_total_USD, 'OLD-SOLO-TOTAL-HUF': old_solo_total_HUF, 'NEW-SOLO-TOTAL-HUF': new_solo_total_HUF, 'CHANGE': change, 'PERCENTAGE': inc, 'METHOD': method}
    i = i + 1


avg_inc = (total_inc / i)

all = ",TOTAL," + str(all_balance) + ",,,,," + str(all_oldPriceUSD) + "," + str(all_newPriceUSD) + "," + str(all_oldPriceHUF) + "," + str(all_newPriceHUF) + "," + str(all_newPriceUSD - all_oldPriceUSD) + "," + str(avg_inc)

print(data)
print(type(data))

x = datetime.datetime.now()
resultFile = "result_" + x.strftime("%Y_%m_%d_%H_%M") + ".csv"

with open(resultFile,'w') as f:
    header = "ROWID,CRYPTO,BALANCE,OLDPRICE-USD,OLDPRICE-HUF,NEWPRICE-USD,NEWPRICE-HUF,OLD-SOLO-TOTAL-USD,NEW-SOLO-TOTAL-USD,OLD-SOLO-TOTAL-HUF,NEW-SOLO-TOTAL-HUF,CHANGE,PERCENTAGE,METHOD\n"
    f.write(header)
    f.close()

for d in data:
    row = ""
    row += str(d) + "," + str(data[d]['CRYPTO']) + "," + str(data[d]['BALANCE']) + "," + str(data[d]['OLDPRICE-USD']) + "," + str(data[d]['OLDPRICE-HUF']) + "," + str(data[d]['NEWPRICE-USD']) + "," + str(data[d]['NEWPRICE-HUF']) + "," + str(data[d]['OLD-SOLO-TOTAL-USD']) + "," + str(data[d]['NEW-SOLO-TOTAL-USD']) + "," + str(data[d]['OLD-SOLO-TOTAL-HUF']) + "," + str(data[d]['NEW-SOLO-TOTAL-HUF']) + "," + str(data[d]['CHANGE']) + "," + str(data[d]['PERCENTAGE']) + "," + str(data[d]['METHOD']) + "\n"
    print(row)
    with open(resultFile,'a') as f:
        f.write(row)
f.close()



with open(resultFile,'a') as f:
    f.write(all)
    f.close()

