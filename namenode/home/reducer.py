#!/usr/bin/env python3
import sys
import math

current_coin = None
sum_price = 0.0
sum_price_sq = 0.0
sum_volume = 0.0
min_price = float('inf')
max_price = float('-inf')
total_count = 0

def emit_result(coin_id):
    if total_count == 0:
        return

    avg_price = sum_price / total_count
    variance = (sum_price_sq / total_count) - (avg_price ** 2)
    std_dev = math.sqrt(variance) if variance > 0 else 0.0

    print("{}\t{},{},{},{},{},{}".format(
    coin_id, min_price, max_price, avg_price, std_dev, sum_volume, total_count
))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, values = line.split("\t", 1)
    try:
        price_str, price_sq_str, vol_str, count_str = values.split(",")
        price = float(price_str)
        price_sq = float(price_sq_str)
        volume = float(vol_str)
        count = int(count_str)
    except ValueError:
        continue

    if current_coin and key != current_coin:
        emit_result(current_coin)
        sum_price = 0.0
        sum_price_sq = 0.0
        sum_volume = 0.0
        min_price = float('inf')
        max_price = float('-inf')
        total_count = 0

    current_coin = key
    sum_price += price
    sum_price_sq += price_sq
    sum_volume += volume
    min_price = min(min_price, price)
    max_price = max(max_price, price)
    total_count += count

if current_coin:
    emit_result(current_coin)