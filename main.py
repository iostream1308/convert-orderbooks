import json
from merge import OrderBookMerger
from binance.client import Client

def load_config(filename):
    """
    Load api_key and api_secret from json
    """
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

def get_order_book_from_file(filename):
    with open(filename, 'r') as file:
        orderbook_pair = json.load(file)
    orderbook_pair_bids = [[float(a), float(b)] for a, b in orderbook_pair['bids']]
    orderbook_pair_asks = [[float(a), float(b)] for a, b in orderbook_pair['asks']]
    fee = float(orderbook_pair['fee'])
    orderbook_pair = {
        'bids': orderbook_pair_bids,
        'asks': orderbook_pair_asks
    }
    return (orderbook_pair, fee)


def get_order_book_and_fee(client, symbol):
    orderbook_pair = client.get_order_book(symbol=symbol)
    orderbook_pair_bids = [[float(a), float(b)] for a, b in orderbook_pair['bids']]
    orderbook_pair_asks = [[float(a), float(b)] for a, b in orderbook_pair['asks']]
    orderbook_pair = {
        'bids': orderbook_pair_bids,
        'asks': orderbook_pair_asks
    }
    fee = client.get_trade_fee(symbol=symbol)
    fee = float(fee[0]['takerCommission'])
    return (orderbook_pair, fee)

def main():
    config = load_config('auth.json')
    api_key = config['api_key']
    api_secret = config['api_secret']
    client = Client(api_key, api_secret)
    from_token = "AAVE"
    to_token = "USDT"
    # int_token = intermediate token
    int_token_1 = 'BTC'
    int_token_2 = 'ETH'
    
    # orderbook + fee: from_token + int_token_1
    orderbook_pair_1 = get_order_book_and_fee(client, from_token+int_token_1)
    # orderbook + fee: int_token_1 + to_token
    orderbook_pair_2 = get_order_book_and_fee(client, int_token_1+to_token)
    
    # orderbook + fee: from_token + int_token_2
    orderbook_pair_3 = get_order_book_and_fee(client, from_token+int_token_2)
    # orderbook + fee: int_token_2 + to_token
    orderbook_pair_4 = get_order_book_and_fee(client, int_token_2+to_token)
    
    # orderbook + fee: from_token + to_token
    orderbook_pair_5 = get_order_book_and_fee(client, from_token+to_token)
    
    # -------if get order_book_from_file-------
    # orderbook_pair_1 = get_order_book_from_file("filename")
    # orderbook_pair_2 = get_order_book_from_file("filename")
    # orderbook_pair_3 = get_order_book_from_file("filename")
    # orderbook_pair_4 = get_order_book_from_file("filename")
    # orderbook_pair_5 = get_order_book_from_file("filename")
    # -----------------------------------------

    
    orderbooks_with_fees = [
        orderbook_pair_1,
        orderbook_pair_2,
        orderbook_pair_3,
        orderbook_pair_4,
        orderbook_pair_5
    ]
    
    merger = OrderBookMerger(from_token, to_token, orderbooks_with_fees)
    
    average_price_buy = merger.get_average_price(7, "buy")
    average_price_sell = merger.get_average_price(7, "sell")
    print(average_price_buy)
    print(average_price_sell)

    with open('merged_orderbook.json', 'w') as f:
        json.dump(merger.merged_orderbook, f, indent=4)

if __name__ == "__main__":
    main()
