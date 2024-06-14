"""
Defines constants that will be used for the rest of the file
(Gets them from the config module)
"""

from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%d%m%y")

CHAR_NAME = 'tibia - beff jezus'

COORDS = {
    'item_query': (999, 640),
    'x_button': (1071, 893),
    'send_item_area': (1009, 894),
    'ask_last_offer': (1223,603),
    'bid_last_offer': (1223,785)
}

ASSETS = ['rubini coins', 'gold token']

MARKET_COORDS = {
    'ask': {
        'AMOUNT_COORDS': [1223, 490, 57, 113],
        'PRICE_COORDS': [1283, 490, 80, 113],
        'DAY_COORDS': [1453, 490, 83, 113],
        'HOUR_COORDS': [1533, 490, 67, 113],
    },
    'bid': {
        'AMOUNT_COORDS': [1223, 672, 57, 113],
        'PRICE_COORDS': [1283, 672, 80, 113],
        'DAY_COORDS': [1453, 672, 83, 113],
        'HOUR_COORDS': [1533, 672, 67, 113],
    }
}
