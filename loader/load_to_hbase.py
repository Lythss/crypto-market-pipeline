#!/usr/bin/env python3
import happybase, subprocess

def load_processed_data(ds):
    """
    Load processed data from HDFS into HBase.
    ds: Execution date in 'YYYY-MM-DD' format.
    """
    year, month, day = ds.split('-')
    # Define the HDFS directory for processed data
    hdfs_dir = f"/user/quixil/crypto/processed/YYYY={year}/MM={month}/DD={day}/"
    local_file = "/tmp/crypto_agg.csv"
    
    # Retrieve the processed output file from HDFS (assumed to be named part-00000)
    subprocess.run(["hdfs", "dfs", "-get", hdfs_dir + "part-00000", local_file], check=True)
    
    # Connect to HBase using HappyBase
    connection = happybase.Connection('localhost')
    table = connection.table('crypto_prices')
    
    with open(local_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Expect line format: coin_id \t minP,maxP,avgP,stdDev,sumVolume,total_count
            coin_id, agg_str = line.split("\t")
            min_p, max_p, avg_p, std_p, vol_sum, count = agg_str.split(",")
            row_key = f"{coin_id}_{ds}"
            table.put(row_key.encode(), {
                b'stats:price_min': min_p.encode(),
                b'stats:price_max': max_p.encode(),
                b'stats:price_avg': avg_p.encode(),
                b'stats:price_std_dev': std_p.encode(),
                b'stats:volume_sum': vol_sum.encode(),
                b'stats:count': count.encode()
            })
    connection.close()

if __name__ == '__main__':
    # For testing, change the date as needed.
    load_processed_data('2025-01-01')
