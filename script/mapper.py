#!/usr/bin/env python3
import sys
import json

# Read each line from standard input
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        record = json.loads(line)
    except json.JSONDecodeError:
        continue

    coin_id = record.get('id')
    current_price = record.get('current_price')
    volume = record.get('total_volume')

    # Skip records if any required field is missing
    if not coin_id or current_price is None or volume is None:
        continue

    try:
        price_float = float(current_price)
        volume_float = float(volume)
    except ValueError:
        continue

    price_squared = price_float * price_float
    # Emit key-value pair: coin_id \t price,price^2,volume,1
    print(f"{coin_id}\t{price_float},{price_squared},{volume_float},1")
