PRICE_HISTORY_DB = (
    "price_history.db",
    '''
        CREATE TABLE IF NOT EXISTS PRICE_HISTORY
        (
            TIME INT PRIMARY KEY   NOT NULL,
            TICKER           TEXT  NOT NULL,
            PRICE            INT   NOT NULL
        );
    '''
)

MATCH_HISTORY_DB = (
    "match_history.db",
    '''
        CREATE TABLE IF NOT EXISTS MATCH_HISTORY
        (
            MATCH_ID INT PRIMARY KEY     NOT NULL,
            BUYER_ORDER_ID               TEXT    NOT NULL,
            SELLER_ORDER_ID              TEXT    NOT NULL,
            SALE_QUANTITY                INT     NOT NULL,
            SALE_PRICE                   INT     NOT NULL
        );
    '''
)


'''

{'match_id': 2122026730, 'buying_order_id': '02ed979a1f', 'selling_order_id': '1f08f10fe6', 'sale_quantity': '1', 'sale_price': '100.140000'}
match_history.db INSERT INTO MATCH_HISTORY (MATCH_ID,BUYER_ORDER_ID,SELLER_ORDER_ID,SALE_QUANTITY,SALE_PRICE) VALUES (2122026730, 02ed979a1f, 1f08f10fe6, 1, 100.14)
Unable to create new record. error: unrecognized token: "02ed979a1f"

{'match_id': 1133495475, 'buying_order_id': 'afe693d025', 'selling_order_id': 'e85211ac1c', 'sale_quantity': '1', 'sale_price': '100.140000'}
match_history.db INSERT INTO MATCH_HISTORY (MATCH_ID,BUYER_ORDER_ID,SELLER_ORDER_ID,SALE_QUANTITY,SALE_PRICE) VALUES (1133495475, afe693d025, e85211ac1c, 1, 100.14)
Unable to create new record. error: no such column: afe693d025
'''