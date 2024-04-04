class Price: 
    def __init__(self, time, ticker, price):
        self.time = time 
        self.ticker = ticker
        self.price = price

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

class Order: 
    def __init__(self, price, quantity, order_type, user_id):
        self.price = price
        self.quantity = quantity
        self.order_type = order_type
        self.user = user_id

class Args: 
    price: float
    quantity: int 
    buy: str
    user: str
    sell: str
    curr_price: str 
    graph_stock: str 
    stream_price: str
    stream_spread: str 
    stream_matches: str 
    no_csvs: bool 
    list_txns: bool 
    portfolio: bool
    price_history: bool 
    graph_portfolio: bool
