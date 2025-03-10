
import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('symbol'):  
        continue

    try:
       
        symbol, date, open_price, high_price, low_price, close_price, volume = line.split(',')
        price = float(close_price)  
        volume_float = float(volume)
    except ValueError:
        continue


    price_squared = price * price
    print("{}\t{},{},{},1".format(symbol, price, price_squared, volume_float))
