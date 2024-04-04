PRICE_HISTORY_DB = (
    "PRICE_HISTORY",
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
    "MATCH_HISTORY",
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