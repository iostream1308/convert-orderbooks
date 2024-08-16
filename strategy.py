class ConvertStrategy:
    def __init__(self, from_token, to_token):
        """
        :param from_token: Ex: 'aave'
        :param to_token: Ex: 'usdt'
        """
        self.from_token = from_token
        self.to_token = to_token

    def convert_bids(self, bids_from, bids_to):
        """
        :param bids_from: First orderbook bids(include fee)
        :param bids_to: Second orderbook bids (include fee)
        :return: list of bids converted.
        """
        bids_from, fee_from = bids_from
        bids_to, fee_to = bids_to
        
        new_order_book_bids = []
        id = 0
        # ftoken: from-token
        # itoken: intermediate-token
        # ttoken: to-token
        for order in bids_from:
            amount_ftoken = order[1] 
            price_ftoken = order[0]
            amount_itoken = (amount_ftoken * price_ftoken) * (1-fee_from)
            amount_ttoken = 0.0
            while amount_itoken > 0:
                if id >= len(bids_to):
                    break
                if amount_itoken <= bids_to[id][1]:  
                    amount_ttoken = amount_ttoken + (amount_itoken * bids_to[id][0]) * (1 - fee_to)
                    price = amount_ttoken / amount_ftoken
                    new_order_book_bids.append([price, amount_ftoken])
                    bids_to[id][1] = bids_to[id][1] - amount_itoken
                    if bids_to[id][1] == 0:
                        id = id + 1
                    break
                else:
                    amount_ttoken = amount_ttoken + (bids_to[id][0] * bids_to[id][1]) * (1 - fee_to)
                    amount_itoken = amount_itoken - bids_to[id][1]
                    bids_to[id][1] = 0
                    id = id + 1
        return new_order_book_bids

    def convert_asks(self, asks_from, asks_to):
        """
        :param asks_from: First orderbook asks(include fee)
        :param asks_to: Second orderbook asks (include fee)
        :return: list of asks converted.
        """
        asks_from, fee_from = asks_from
        asks_to, fee_to = asks_to
        
        new_order_book_asks = []
        id = 0
        for order in asks_from:
            amount_ftoken = order[1] 
            price_ftoken = order[0]
            amount_itoken = (amount_ftoken * price_ftoken) * (1-fee_from)
            amount_ttoken = 0.0
            while amount_itoken > 0:
                if id >= len(asks_to):
                    break
                if amount_itoken <= asks_to[id][1]:  
                    amount_ttoken = amount_ttoken + (amount_itoken * asks_to[id][0]) * (1 - fee_to)
                    price = amount_ttoken / amount_ftoken
                    new_order_book_asks.append([price, amount_ftoken])
                    asks_to[id][1] = asks_to[id][1] - amount_itoken
                    if asks_to[id][1] == 0:
                        id = id + 1
                    break
                else:
                    amount_ttoken = amount_ttoken + (asks_to[id][0] * asks_to[id][1]) * (1 - fee_to)
                    amount_itoken = amount_itoken - asks_to[id][1]
                    asks_to[id][1] = 0
                    id = id + 1
        return new_order_book_asks
