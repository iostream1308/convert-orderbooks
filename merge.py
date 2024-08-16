from strategy import ConvertStrategy

class OrderBookMerger:
    def __init__(self, base_currency, quote_currency, orderbooks_with_fees):
        """
        :param base_currency: Ex: 'aave'
        :param quote_currency: Ex: 'usdt'
        :param orderbooks_with_fees: list orderbooks (bids and asks) of pairs
        """
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.orderbooks_with_fees = orderbooks_with_fees
        self.strategy = ConvertStrategy(base_currency, quote_currency)
        self.merged_orderbook = self.merge_all_orderbooks()

    
    def merge_all_orderbooks(self):
        """
        :return: orderbook merged (bids & asks).
        """
        all_bids = []
        all_asks = []

        id = 0
        while id < 4:
            orderbook_1, fee_1 = self.orderbooks_with_fees[id]
            orderbook_2, fee_2 = self.orderbooks_with_fees[id+1]
            bids_1_with_fee = [orderbook_1['bids'], fee_1]
            bids_2_with_fee = [orderbook_2['bids'], fee_2]
            
            asks_1_with_fee = [orderbook_1['asks'], fee_1]
            asks_2_with_fee = [orderbook_2['asks'], fee_2]
            
            converted_bids = self.strategy.convert_bids(bids_1_with_fee, bids_2_with_fee)
            converted_asks = self.strategy.convert_asks(asks_1_with_fee, asks_2_with_fee)
            
            all_bids.extend(converted_bids)
            all_asks.extend(converted_asks)
            
            id = id + 2
            
        orderbook, fee = self.orderbooks_with_fees[4]
        bids = orderbook['bids']
        asks = orderbook['asks']
        for order in bids:
            order[0] = order[0] * (1-fee)
        for order in asks:
            order[0] = order[0] * (1-fee)
        all_bids.extend(bids)
        all_asks.extend(asks)

        all_bids.sort(key=lambda x: x[0], reverse=True) 
        all_asks.sort(key=lambda x: x[0])              

        merged_orderbook = {
            'bids': all_bids,
            'asks': all_asks
        }
        return merged_orderbook
    
    
    def get_average_price(self, amount, side):
        """
        Calculate the average price base on amount and side (buy or sell).
        :param amount: amount token.
        :param side: "buy" or "sell".
        :return: average price.
        """
        if side == "buy":
            order_side = self.merged_orderbook['asks']
        elif side == "sell":
            order_side = self.merged_orderbook['bids']
        else:
            raise ValueError("Wrong side")
        
        tmp_amount = amount 
        amount_out = 0.0
        for price, size in order_side:
            if tmp_amount <= size:
                amount_out = amount_out + tmp_amount * price
                tmp_amount = 0
                break
            else:
                amount_out = amount_out + size * price
                tmp_amount = tmp_amount - size
        
        if tmp_amount > 0:
            raise ValueError("Amount too large")

        average_price = amount_out / amount
        return average_price
