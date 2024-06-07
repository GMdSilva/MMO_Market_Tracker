"""
Defines constants that will be used for the rest of the file
(Gets them from the config module)
"""

from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%d%m%y")

CHAR_NAME = 'tibia - beff jezius'

COORDS = {
    'item_query': (999, 640),
    'x_button': (1071, 893),
    'send_item_area': (1009, 894),
}

ASSETS = ['rubini coins']

MARKET_COORDS = {
    'ask': {
        'AMOUNT_COORDS': [1223, 493, 1612 - 1555, 615 - 505],
        'PRICE_COORDS': [1283, 493, 83, 615 - 505],
        'DAY_COORDS': [1453, 493, 83, 615 - 505],
        'HOUR_COORDS': [1533, 493, 67, 615 - 505],
    },
    'bid': {
        'AMOUNT_COORDS': [1223, 673, 1612 - 1555, 765 - 653],
        'PRICE_COORDS': [1283, 675, 83, 765 - 653],
        'DAY_COORDS': [1453, 675, 83, 765 - 653],
        'HOUR_COORDS': [1533, 675, 67, 765 - 653],
    }
}
