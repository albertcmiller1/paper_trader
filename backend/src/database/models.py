class Match: 
    def __init__(self, 
        match_id: int,
        buyer_order_id: str,
        seller_order_id: str,
        sale_quantity: int, 
        sale_price: float,
    ):
        self.match_id = match_id
        self.buyer_order_id = buyer_order_id
        self.seller_order_id = seller_order_id
        self.sale_quantity = sale_quantity
        self.sale_price = sale_price

class Price: 
    def __init__(self, time, ticker, price):
        self.time = time 
        self.ticker = ticker
        self.price = price