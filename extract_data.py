import os
import json
import pandas as pd

def extract_transaction_data(base_path):
    data = []

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                with open(os.path.join(year_path, file), 'r') as f:
                    try:
                        content = json.load(f)
                        quarter = int(file.strip('.json'))
                        for item in content['data']['transactionData']:
                            data.append({
                                'State': state.title().replace('-', ' '),
                                'Year': int(year),
                                'Quarter': quarter,
                                'Transaction_type': item['name'],
                                'Count': item['paymentInstruments'][0]['count'],
                                'Amount': item['paymentInstruments'][0]['amount']
                            })
                    except:
                        continue
    return pd.DataFrame(data)

if __name__ == '__main__':
    base_path = 'pulse/data/aggregated/transaction/country/india/state/'
    df = extract_transaction_data(base_path)
    df.to_csv('transactions.csv', index=False)
    print("✅ CSV saved as transactions.csv")